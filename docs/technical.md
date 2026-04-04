# Maya MIRO — Technical Deep Dive

A detailed breakdown of every technology used in Maya MIRO: what it is, why it's here, and how it fits together.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────┐
│                    FRONTEND (Browser)                │
│              Vue.js + Vite + Axios                   │
│         UI for upload, visualization, chat           │
└───────────────────────┬──────────────────────────────┘
                        │ HTTP REST API
┌───────────────────────▼──────────────────────────────┐
│                   BACKEND (Python)                   │
│              Flask + Flask-CORS                      │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ Graph API   │  │ Simulation   │  │ Report     │  │
│  │ /api/graph  │  │ /api/sim     │  │ /api/report│  │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                │                 │         │
│  ┌──────▼────────────────▼─────────────────▼──────┐  │
│  │              Services Layer                    │  │
│  │  OntologyGenerator │ GraphBuilder │ ReportAgent│  │
│  └──────┬────────────────┬─────────────────┬──────┘  │
│         │                │                 │         │
│  ┌──────▼──┐  ┌──────────▼──────┐  ┌──────▼──────┐  │
│  │NVIDIA   │  │  Neo4j Storage  │  │ CAMEL-OASIS │  │
│  │NIM API  │  │  (neo4j driver) │  │ (agents)    │  │
│  └─────────┘  └────────┬────────┘  └─────────────┘  │
└─────────────────────────┼────────────────────────────┘
                          │ Bolt Protocol (encrypted)
              ┌───────────▼───────────┐
              │  Neo4j Aura (Cloud)   │
              │  Graph Database       │
              └───────────────────────┘
```

---

## Core Technologies

### 1. Neo4j — The Brain (Graph Database)

**What is it?**
Neo4j is a **graph database**. Unlike traditional databases (MySQL, PostgreSQL) that store data in tables with rows and columns, Neo4j stores data as **nodes** (things) and **relationships** (connections between things).

**Why a graph database?**
Financial data is naturally a graph. "NVIDIA supplies chips to Tesla" isn't a row in a table — it's a relationship between two entities. Graph databases let you:
- Store these relationships natively (not as foreign keys)
- Query connections efficiently ("find all companies connected to Elon Musk within 2 hops")
- Visualize the network of relationships

**Example of what's stored:**
```
(NVIDIA:Company) ──[SUPPLIES_TO]──> (Tesla:Company)
(Elon Musk:Person) ──[LEADS]──> (Tesla:Company)
(S&P 500:Index) ──[TRACKS]──> (NVIDIA:Company)
```

**Neo4j Aura** is the cloud-hosted version. Free tier gives you 200K nodes and 400K relationships — more than enough for Maya MIRO.

**Key terms:**
| Term | Meaning |
|------|---------|
| **Node** | An entity (company, person, index) |
| **Relationship/Edge** | A connection between two nodes |
| **Label** | A type tag on a node (`:Company`, `:Person`) |
| **Property** | Key-value data on a node/edge (`name: "NVIDIA"`) |
| **Cypher** | Neo4j's query language (like SQL but for graphs) |

---

### 2. NVIDIA NIM — The Intelligence (LLM API)

**What is it?**
NVIDIA NIM (NVIDIA Inference Microservices) is a cloud API that lets you call large AI models without running them locally. Maya MIRO uses it for two things:

**a) LLM (Large Language Model): `qwen/qwen3.5-397b-a17b`**
- A 397 billion parameter AI model by Alibaba (Qwen team)
- Used for: reading documents, extracting entities, generating agent personalities, running simulations, writing reports
- This model is massive — normally needs 200GB+ VRAM to run locally. NVIDIA NIM runs it on their infrastructure.

**b) Embeddings: `nvidia/nv-embed-v1`**
- Converts text into mathematical vectors (arrays of numbers)
- Used for: similarity search ("find entities related to this query")
- A 768-dimensional vector captures the *meaning* of text, not just keywords

**Why NIM instead of Ollama (local)?**
| | Ollama (Local) | NVIDIA NIM (Cloud) |
|---|---|---|
| Hardware | 16GB+ RAM, 10GB+ VRAM | Any computer |
| Speed | Depends on your GPU | Fast (NVIDIA A100 GPUs) |
| Model size | Limited by your hardware | 397B parameter model |
| Internet | Not needed | Required |
| Cost | Free (your electricity) | Free tier available |

---

### 3. CAMEL-OASIS — The Simulation Engine

**What is it?**
CAMEL-AI is an open-source framework for building multi-agent AI systems. OASIS (Open Agent Social Interaction Simulations) is a module within CAMEL specifically designed to simulate social media interactions.

**What it does in Maya MIRO:**
1. **Creates agents** — Each with a unique personality profile (age, occupation, investment style, emotional triggers)
2. **Simulates platforms** — Agents interact on simulated Twitter/Reddit
3. **Available actions** — Agents can: create posts, like, repost, quote, follow, or do nothing
4. **Opinion dynamics** — Agents influence each other based on their "influence level" and who they follow

**Agent personality example:**
```json
{
  "name": "Rajesh Kumar",
  "age": 45,
  "type": "institutional_investor",
  "bias": "bullish_tech",
  "influence": 0.8,
  "reaction_speed": "slow",
  "panic_threshold": 0.3
}
```

---

### 4. Flask — The API Server (Backend)

**What is it?**
Flask is a lightweight Python web framework. It receives HTTP requests from the frontend and routes them to the right service.

**API routes:**
| Route | Purpose |
|-------|---------|
| `POST /api/graph/ontology/generate` | Upload document → generate ontology |
| `POST /api/graph/build` | Build knowledge graph from document |
| `GET /api/graph/task/{id}` | Check progress of a running task |
| `POST /api/simulation/create` | Create simulation environment |
| `POST /api/simulation/run` | Start the agent simulation |
| `POST /api/report/generate` | Generate sentiment analysis report |

---

### 5. Vue.js + Vite — The Frontend

**What is it?**
- **Vue.js** — A JavaScript framework for building reactive user interfaces
- **Vite** — A fast development server and build tool

**What it shows you:**
- File upload interface
- Graph visualization (nodes and edges)
- Simulation progress and agent activity feed
- Sentiment report dashboard
- Agent chat interface

---

## Data Flow — What Happens When You Upload a Document

### Stage 1: Ontology Generation
```
Document (PDF/TXT) 
  → FileParser extracts raw text
  → TextProcessor cleans it
  → OntologyGenerator sends text to NVIDIA NIM (Qwen 3.5)
  → LLM returns: entity types + relationship types
  → Saved to project state
```

### Stage 2: Graph Build
```
Raw text 
  → TextProcessor.split_text() chunks it (500 char chunks, 50 char overlap)
  → For each chunk:
      → NERExtractor sends to NVIDIA NIM
      → LLM returns: entities + relations
      → EmbeddingService converts to vectors (nvidia/nv-embed-v1)
      → Neo4jStorage writes nodes and edges to database
  → Knowledge graph is complete
```

### Stage 3: Environment Setup
```
Knowledge graph data
  → NVIDIA NIM generates agent personality profiles
  → CAMEL-OASIS creates agent instances
  → Each agent reads relevant graph data to form initial opinions
  → Simulated social platform is initialized
```

### Stage 4: Simulation
```
For each simulation round (hour):
  → Each agent decides an action (post, reply, like, do nothing)
  → Actions are processed by OASIS platform
  → Agents read others' posts and update their opinions
  → Sentiment metrics are tracked
  → Repeat for configured number of rounds
```

### Stage 5: Report
```
Simulation data (all posts, opinion shifts, metrics)
  → ReportAgent analyzes with NVIDIA NIM
  → Uses tool calls to query graph for supporting evidence
  → Generates structured sentiment report
  → Report is displayed in frontend
```

---

## Key Files & Folders

```
myMayaMIRO/
├── .env                          # API keys and database credentials
├── README.md                     # Project overview
├── backend/
│   ├── run.py                    # Entry point — starts Flask server
│   ├── app/
│   │   ├── __init__.py           # App factory — initializes Neo4j, CORS, blueprints
│   │   ├── config.py             # All configuration (reads .env)
│   │   ├── api/
│   │   │   └── graph.py          # REST API routes for graph operations
│   │   ├── services/
│   │   │   ├── ontology_generator.py   # Stage 1: Document → Ontology
│   │   │   ├── graph_builder.py        # Stage 2: Ontology → Knowledge Graph
│   │   │   └── simulation_runner.py    # Stage 3-4: Agent simulation
│   │   ├── storage/
│   │   │   ├── neo4j_storage.py        # All Neo4j database operations
│   │   │   ├── embedding_service.py    # Text → Vector embeddings
│   │   │   ├── ner_extractor.py        # Named Entity Recognition via LLM
│   │   │   └── search_service.py       # Hybrid search (vector + keyword)
│   │   └── utils/
│   │       ├── file_parser.py          # PDF/TXT text extraction
│   │       └── logger.py              # Logging setup
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/                      # Vue.js source code
│   ├── package.json              # Node.js dependencies
│   └── vite.config.js            # Vite dev server config
└── docs/
    └── technical.md              # This file
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **GraphRAG** | Graph-based Retrieval Augmented Generation — using a knowledge graph (not just text chunks) to provide context to an LLM |
| **NER** | Named Entity Recognition — identifying entities (people, companies) in text |
| **RE** | Relation Extraction — identifying relationships between entities |
| **Ontology** | A schema defining what types of entities and relationships exist |
| **Knowledge Graph** | A database of entities and their relationships |
| **Embedding** | A mathematical vector representing the meaning of text |
| **Agent** | A simulated AI persona with unique personality and opinions |
| **OASIS** | Open Agent Social Interaction Simulations — the multi-agent framework |
| **Cypher** | Neo4j's graph query language |
| **Bolt** | Neo4j's binary communication protocol |
| **SSC** | Self-Signed Certificate — `neo4j+ssc://` skips SSL cert verification |

---

## Configuration Reference

| Environment Variable | Purpose | Example |
|---------------------|---------|---------|
| `LLM_API_KEY` | NVIDIA NIM API key for LLM calls | `nvapi-xxxx` |
| `LLM_BASE_URL` | NVIDIA NIM endpoint | `https://integrate.api.nvidia.com/v1` |
| `LLM_MODEL_NAME` | Which LLM to use | `qwen/qwen3.5-397b-a17b` |
| `NEO4J_URI` | Neo4j connection string | `neo4j+ssc://xxx.databases.neo4j.io` |
| `NEO4J_USER` | Neo4j database username | `430710be` |
| `NEO4J_PASSWORD` | Neo4j database password | (from Aura dashboard) |
| `EMBEDDING_MODEL` | Embedding model name | `nvidia/nv-embed-v1` |
| `EMBEDDING_BASE_URL` | Embedding API endpoint | `https://integrate.api.nvidia.com/v1` |
| `EMBEDDING_API_KEY` | API key for embeddings | `nvapi-xxxx` |
