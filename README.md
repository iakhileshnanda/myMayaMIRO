# 🐟 Maya MIRO — AI-Powered Stock Sentiment Simulator

> **What if you could simulate how the entire market reacts to a news article — before you trade?**

Maya MIRO uploads a financial document, creates hundreds of AI investor personas, and lets them debate on simulated social media — giving you a real-time sentiment verdict you can cross-check with your charts.

---

## 🧠 What Is This?

Maya MIRO is a **stock sentiment analysis tool** that goes far beyond simple "positive/negative" text analysis.

Instead of just summarizing a document, it builds an entire **simulated world** of AI investors — bulls, bears, retail traders, institutional analysts — and lets them argue, influence each other, and shift opinions based on the financial data you provide.

**The result:** A crowd-sourced sentiment score from hundreds of unique AI perspectives, not just one model's opinion.

---

## 🎯 How Does It Work?

```
You → Upload earnings report / news article / RBI policy
  ↓
Stage 1: Ontology → AI reads document, identifies entities & relationships
  ↓
Stage 2: Graph Build → Extracts every fact into a knowledge graph (Neo4j)
  ↓
Stage 3: Environment → Creates 100s of AI agents with unique personalities
  ↓
Stage 4: Simulation → Agents post, argue, shift opinions on simulated social media
  ↓
Stage 5: Report → Structured sentiment analysis + chat with any agent
  ↓
You → Cross-check with Zerodha/TradingView → Make informed trade decision
```

### The 5 Stages Explained

| Stage | Name | What Happens |
|-------|------|--------------|
| 1 | **Ontology Generation** | AI reads your document and creates a "table of contents" — what types of entities exist (companies, people, indices) and how they relate |
| 2 | **Graph Build** | AI re-reads the full document and extracts every fact as nodes and edges in a knowledge graph |
| 3 | **Environment Setup** | Generates hundreds of AI agent personas — each with unique personality, bias, influence level |
| 4 | **Simulation** | Agents interact on simulated Twitter/Reddit — posting, replying, arguing, changing opinions hour by hour |
| 5 | **Report + Chat** | ReportAgent generates structured sentiment analysis. You can chat with any agent to understand their reasoning |

---

## ❓ How Is This Different?

| Feature | Traditional Sentiment Analysis | Maya MIRO |
|---------|-------------------------------|-----------|
| Approach | Single model reads text, outputs score | Hundreds of AI agents debate and evolve opinions |
| Depth | Surface-level positive/negative | Multi-perspective with personality-driven reasoning |
| Temporal | Static snapshot | Dynamic — sentiment evolves hour by hour |
| Explainability | Black box score | Chat with any agent, ask "why are you bearish?" |
| Data Model | Flat text | Knowledge graph with entities and relationships |

---

## 🔄 What Changed from MiroFish-Offline?

This is a customized fork of [MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) by Akhilesh Nanda.

| | MiroFish-Offline | Maya MIRO |
|---|---|---|
| **AI Backend** | Ollama (local models) | NVIDIA NIM API (cloud) |
| **RAM Required** | 16GB minimum | ~2GB (Neo4j only) |
| **LLM Model** | qwen2.5:32b via Ollama | qwen/qwen3.5-397b-a17b via NVIDIA NIM |
| **Embeddings** | nomic-embed-text via Ollama | nvidia/nv-embed-v1 via NVIDIA NIM |
| **GPU** | 10GB VRAM minimum | Not needed |
| **Internet** | Not required | NVIDIA NIM API key required |
| **Use Case** | Generic simulation | Stock sentiment + financial analysis |

---

## ⚙️ Setup Guide

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** installed
- **Neo4j Aura** free account (cloud database — no Docker needed)
- **NVIDIA NIM** free API key

### Step 1 — Clone & Configure
```bash
git clone https://github.com/iakhileshnanda/myMayaMIRO.git
cd myMayaMIRO
cp .env.example .env
```

### Step 2 — Get Your API Keys

**NVIDIA NIM** (free):
1. Go to [integrate.api.nvidia.com](https://integrate.api.nvidia.com)
2. Sign up → Generate API key
3. Paste into `.env` as `LLM_API_KEY` and `EMBEDDING_API_KEY`

**Neo4j Aura** (free):
1. Go to [neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free/)
2. Create free instance → Download credentials
3. Update `.env` with your URI, username, and password

### Step 3 — Update `.env`
```ini
LLM_API_KEY=your_nvidia_nim_key
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-397b-a17b

NEO4J_URI=neo4j+ssc://YOUR_INSTANCE_ID.databases.neo4j.io
NEO4J_USER=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password

EMBEDDING_MODEL=nvidia/nv-embed-v1
EMBEDDING_BASE_URL=https://integrate.api.nvidia.com/v1
EMBEDDING_API_KEY=your_nvidia_nim_key
```

> **Note:** Use `neo4j+ssc://` (not `neo4j+s://`) to avoid SSL certificate issues on Windows.

### Step 4 — Start the Backend
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Step 5 — Start the Frontend
```bash
cd frontend
npm install
npm run dev
```

### Step 6 — Open the App
Navigate to **http://localhost:5173** in your browser.

---

## 💻 Hardware Requirements

| Component | Maya MIRO | Original MiroFish-Offline |
|-----------|-----------|--------------------------|
| RAM | ~2GB (Neo4j only) | 16GB minimum |
| GPU | Not needed | 10GB VRAM minimum |
| Disk | 5GB | 20GB |
| Internet | Required (NVIDIA NIM) | Not required |

---

## 📌 Credits

- Original MiroFish: [github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish)
- MiroFish-Offline fork: [github.com/nikmcfly/MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline)
- Maya MIRO by: [Akhilesh Nanda](https://github.com/iakhileshnanda)

## 📄 License

AGPL-3.0 — See [LICENSE](LICENSE) for details.