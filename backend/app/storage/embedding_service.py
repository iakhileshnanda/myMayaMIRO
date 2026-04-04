"""
EmbeddingService — Embedding via OpenAI-compatible API (NVIDIA NIM / Ollama)

Supports both NVIDIA NIM (/v1/embeddings) and Ollama (/api/embed) endpoints.
Auto-detects the correct format based on the configured base URL.
"""

import os
import time
import logging
from typing import List, Optional

import requests

from ..config import Config

logger = logging.getLogger('mirofish.embedding')


class EmbeddingService:
    """Generate embeddings using OpenAI-compatible API (NVIDIA NIM or Ollama)."""

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        timeout: int = 30,
    ):
        self.model = model or Config.EMBEDDING_MODEL
        self.base_url = (base_url or Config.EMBEDDING_BASE_URL).rstrip('/')
        self.api_key = api_key or getattr(Config, 'EMBEDDING_API_KEY', None) or os.environ.get('EMBEDDING_API_KEY', '')
        self.max_retries = max_retries
        self.timeout = timeout

        # Auto-detect API format based on URL
        # NVIDIA NIM / OpenAI uses /v1/embeddings
        # Ollama uses /api/embed
        if 'nvidia' in self.base_url or 'openai' in self.base_url or '/v1' in self.base_url:
            self._embed_url = f"{self.base_url}/embeddings"
            self._api_format = "openai"
        else:
            self._embed_url = f"{self.base_url}/api/embed"
            self._api_format = "ollama"

        logger.info(f"EmbeddingService initialized: model={self.model}, format={self._api_format}, url={self._embed_url}")

        # Simple in-memory cache (text -> embedding vector)
        self._cache: dict[str, List[float]] = {}
        self._cache_max_size = 2000

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            Embedding float vector

        Raises:
            EmbeddingError: If request fails after retries
        """
        if not text or not text.strip():
            raise EmbeddingError("Cannot embed empty text")

        text = text.strip()

        # Check cache
        if text in self._cache:
            return self._cache[text]

        vectors = self._request_embeddings([text])
        vector = vectors[0]

        # Cache result
        self._cache_put(text, vector)

        return vector

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Processes in batches to avoid overwhelming the API.

        Args:
            texts: List of input texts
            batch_size: Number of texts per request

        Returns:
            List of embedding vectors (same order as input)
        """
        if not texts:
            return []

        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_indices: List[int] = []
        uncached_texts: List[str] = []

        # Check cache first
        for i, text in enumerate(texts):
            text = text.strip() if text else ""
            if text in self._cache:
                results[i] = self._cache[text]
            elif text:
                uncached_indices.append(i)
                uncached_texts.append(text)
            else:
                # Empty text — zero vector
                results[i] = [0.0] * 1024

        # Batch-embed uncached texts
        if uncached_texts:
            all_vectors: List[List[float]] = []
            for start in range(0, len(uncached_texts), batch_size):
                batch = uncached_texts[start:start + batch_size]
                vectors = self._request_embeddings(batch)
                all_vectors.extend(vectors)

            # Place results and cache
            for idx, vec, text in zip(uncached_indices, all_vectors, uncached_texts):
                results[idx] = vec
                self._cache_put(text, vec)

        return results  # type: ignore

    def _request_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Make HTTP request to embedding endpoint with retry.
        Supports both OpenAI-compatible and Ollama formats.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        # Build request based on API format
        if self._api_format == "openai":
            payload = {
                "model": self.model,
                "input": texts,
                "encoding_format": "float",
                "input_type": "query",
            }
            headers = {
                "Content-Type": "application/json",
            }
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
        else:
            # Ollama format
            payload = {
                "model": self.model,
                "input": texts,
            }
            headers = {
                "Content-Type": "application/json",
            }

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self._embed_url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                data = response.json()

                # Parse response based on format
                if self._api_format == "openai":
                    # OpenAI/NVIDIA format: {"data": [{"embedding": [...], "index": 0}, ...]}
                    embedding_data = data.get("data", [])
                    # Sort by index to preserve order
                    embedding_data.sort(key=lambda x: x.get("index", 0))
                    embeddings = [item["embedding"] for item in embedding_data]
                else:
                    # Ollama format: {"embeddings": [[...], [...]]}
                    embeddings = data.get("embeddings", [])

                if len(embeddings) != len(texts):
                    raise EmbeddingError(
                        f"Expected {len(texts)} embeddings, got {len(embeddings)}"
                    )

                return embeddings

            except requests.exceptions.ConnectionError as e:
                last_error = e
                logger.warning(
                    f"Embedding connection failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
            except requests.exceptions.Timeout as e:
                last_error = e
                logger.warning(
                    f"Embedding request timed out (attempt {attempt + 1}/{self.max_retries})"
                )
            except requests.exceptions.HTTPError as e:
                last_error = e
                status = e.response.status_code
                logger.error(f"Embedding HTTP error: {status} - {e.response.text}")
                if status == 429:
                    # Rate limited — wait longer
                    wait = 5 * (attempt + 1)
                    logger.warning(f"Rate limited, waiting {wait}s before retry...")
                    time.sleep(wait)
                    continue
                elif status >= 500:
                    # Server error — retry
                    pass
                else:
                    # Client error (4xx except 429) — don't retry
                    raise EmbeddingError(f"Embedding failed: {e}") from e
            except (KeyError, ValueError) as e:
                raise EmbeddingError(f"Invalid embedding response: {e}") from e

            # Exponential backoff
            if attempt < self.max_retries - 1:
                wait = 2 ** attempt
                logger.info(f"Retrying in {wait}s...")
                time.sleep(wait)

        raise EmbeddingError(
            f"Embedding failed after {self.max_retries} retries: {last_error}"
        )

    def _cache_put(self, text: str, vector: List[float]) -> None:
        """Add to cache, evicting oldest entries if full."""
        if len(self._cache) >= self._cache_max_size:
            # Remove ~10% of oldest entries
            keys_to_remove = list(self._cache.keys())[:self._cache_max_size // 10]
            for key in keys_to_remove:
                del self._cache[key]
        self._cache[text] = vector

    def health_check(self) -> bool:
        """Check if embedding endpoint is reachable."""
        try:
            vec = self.embed("health check")
            return len(vec) > 0
        except Exception:
            return False


class EmbeddingError(Exception):
    """Raised when embedding generation fails."""
    pass
