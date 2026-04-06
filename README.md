# Maya MIRO — Multi-Agent Parallel World Simulation Engine

> **Enhanced fork of [MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) by [Akhilesh Nanda](https://github.com/iakhileshnanda)**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Node.js](https://img.shields.io/badge/Node.js-18+-green?logo=node.js)
![Neo4j](https://img.shields.io/badge/Neo4j-Aura_Free-008CC1?logo=neo4j)
![NVIDIA NIM](https://img.shields.io/badge/NVIDIA-NIM_API-76B900?logo=nvidia)
![License](https://img.shields.io/badge/License-AGPL--3.0-red)

> **What if you could simulate how the entire market reacts to a news article — before you trade?**

Upload a financial document, watch hundreds of AI investor personas debate on simulated social media, and get a crowd-sourced sentiment verdict you can cross-check with your charts.

---

## What Is Maya MIRO?

Maya MIRO is an open-source simulation engine that creates **parallel worlds** — miniature digital societies where AI characters (called **agents**) read information, form opinions, and argue with each other on simulated social media platforms like Twitter and Reddit.

**Key concepts in plain English:**

| Term | What It Means |
|------|--------------|
| **Knowledge Graph** | A database that stores facts as connections. Instead of rows in a spreadsheet, it stores things like `NVIDIA --supplies chips to--> Tesla`. The database is [Neo4j](https://neo4j.com/). |
| **Agent Swarm** | A group of hundreds of AI characters, each with a unique personality — some are bullish retail traders, some are cautious institutional investors, some panic easily. They act independently. |
| **LLM** (Large Language Model) | The AI brain behind each agent. It reads text, understands context, and generates human-like responses. Maya MIRO uses Alibaba's Qwen 3.5 (397 billion parameters) via NVIDIA's cloud. |
| **Vector Memory / Embeddings** | A way to convert text into numbers (arrays of 768 numbers) so the computer can measure how "similar" two pieces of text are. Used for searching the knowledge graph by meaning, not just keywords. |
| **Ontology** | A "table of contents" that tells the system what types of entities exist (companies, people, indices) and how they can relate to each other. Generated automatically from your document. |
| **Simulation** | The core process: agents post opinions, read each other's posts, argue, change their minds, and shift sentiment — hour by hour — just like real social media. |
| **GraphRAG** | Graph-based Retrieval Augmented Generation. Instead of feeding raw text to the AI, the system queries the knowledge graph for structured facts and relationships, giving the AI much better context. |

**Maya MIRO** takes this engine and points it at **stock market sentiment analysis** — you upload an earnings report, news article, or RBI policy document, and the simulation tells you how the market *might* react.

---

## How Does It Work?

```
You --> Upload earnings report / news article / RBI policy
  |
  v
Stage 1: Ontology --> AI reads document, identifies entities & relationships
  |
  v
Stage 2: Graph Build --> Extracts every fact into a knowledge graph (Neo4j)
  |
  v
Stage 3: Environment --> Creates 100s of AI agents with unique personalities
  |
  v
Stage 4: Simulation --> Agents post, argue, shift opinions on simulated social media
  |
  v
Stage 5: Report --> Structured sentiment analysis + chat with any agent
  |
  v
You --> Cross-check with Zerodha / TradingView --> Make informed trade decision
```

### The 5 Stages Explained

| Stage | Name | What Happens |
|-------|------|--------------|
| 1 | **Ontology Generation** | AI reads your document and creates a schema — what types of entities exist (companies, people, indices) and how they relate. Think of it as a "table of contents" for the facts. |
| 2 | **Graph Build** | AI re-reads the full document, extracts every fact as nodes and edges in Neo4j. For example: `(RBI:CentralBank) --[REGULATES]--> (IndianMarket:Index)`. |
| 3 | **Environment Setup** | Generates hundreds of AI agent personas — each with unique personality, bias, influence level, panic threshold. These are the "simulated investors". |
| 4 | **Simulation** | Agents interact on simulated Twitter/Reddit — posting opinions, replying, arguing, changing their minds hour by hour based on what others say. |
| 5 | **Report + Chat** | A ReportAgent analyzes all simulation data, queries the knowledge graph for evidence, and generates a structured sentiment report. You can then chat with any individual agent to ask "why are you bearish?" |

---

## How Is This Different from Normal Sentiment Analysis?

| Feature | Traditional Sentiment Analysis | Maya MIRO |
|---------|-------------------------------|-----------|
| **Approach** | Single model reads text, outputs a positive/negative score | Hundreds of AI agents debate and evolve opinions over time |
| **Depth** | Surface-level positive/negative | Multi-perspective with personality-driven reasoning |
| **Temporal** | Static snapshot — one score, one moment | Dynamic — sentiment evolves hour by hour across simulation rounds |
| **Explainability** | Black box score — no way to ask "why?" | Chat with any agent, ask "why are you bearish on NVIDIA?" |
| **Data Model** | Flat text input | Structured knowledge graph with entities and relationships |

---

## What Changed from the Original MiroFish?

This fork replaces the entire backend infrastructure while keeping the simulation engine intact.

| | MiroFish-Offline (Original) | Maya MIRO (This Fork) |
|---|---|---|
| **AI Backend** | Ollama (local models) | NVIDIA NIM API (cloud) |
| **LLM Model** | qwen2.5:32b via Ollama | qwen/qwen3.5-397b-a17b via NVIDIA NIM (10x larger model) |
| **Embeddings** | nomic-embed-text via Ollama | nvidia/nv-embed-v1 via NVIDIA NIM |
| **Graph Database** | Neo4j Community (local Docker) | Neo4j Aura (free cloud — no Docker needed) |
| **RAM Required** | 16GB minimum | ~2GB (no local models) |
| **GPU Required** | 10GB VRAM minimum | Not needed |
| **Internet** | Not required | Required (NVIDIA NIM + Neo4j Aura) |
| **Use Case** | Generic simulation | Stock sentiment + financial analysis |
| **Zep Cloud** | Removed (was in original) | Replaced entirely with Neo4j + custom storage layer |
| **Storage Layer** | Zep SDK | Custom `GraphStorage` abstraction with `Neo4jStorage` implementation |
| **Search** | Zep built-in | Hybrid search (0.7 vector + 0.3 BM25 keyword) via Neo4j |
| **Platform** | Linux/Mac focused | Windows + Linux tested with platform-specific setup instructions |

### What I Built / Rewrote

- **Complete storage layer rewrite** — Replaced all Zep Cloud dependencies with a custom `GraphStorage` interface backed by Neo4j (see `backend/app/storage/`)
- **NVIDIA NIM integration** — Swapped Ollama for cloud-based NVIDIA NIM API, enabling access to the 397B parameter Qwen model without any local GPU
- **Neo4j Aura migration** — Moved from local Docker Neo4j to free cloud-hosted Neo4j Aura, eliminating Docker as a prerequisite
- **Custom NER/RE pipeline** — Built `NERExtractor` and `EmbeddingService` that work with NVIDIA NIM's OpenAI-compatible API
- **Hybrid search** — Implemented 0.7 vector + 0.3 BM25 keyword search in Neo4j for graph retrieval
- **Cross-platform support** — Tested and documented setup for both Windows and Linux (Ubuntu/Debian)
- **Stock market focus** — Configured agent archetypes, prompts, and report templates for Indian stock market sentiment analysis

---

## Prerequisites

You need these installed **before** starting. Here's what each one does:

| Prerequisite | Why You Need It | How to Get It |
|-------------|----------------|---------------|
| **Python 3.11** | Runs the backend server and simulation engine. Version 3.11 specifically because `camel-oasis` (the simulation library) does not support Python 3.12+. | [python.org/downloads](https://www.python.org/downloads/) — Windows installs 3.11 directly. Linux: see setup instructions below. |
| **Node.js 18+** | Runs the frontend development server (Vue.js + Vite). | [nodejs.org](https://nodejs.org/) — download the LTS version. |
| **NVIDIA NIM API Key** (free) | Gives your app access to the Qwen 3.5 LLM and embedding models running on NVIDIA's cloud GPUs. Without this, the AI has no brain. | [integrate.api.nvidia.com](https://integrate.api.nvidia.com) — sign up, generate a key. |
| **Neo4j Aura Account** (free) | Cloud-hosted graph database where all extracted knowledge (entities, relationships) is stored. Free tier gives 200K nodes. | [neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free/) — create instance, download credentials. |
| **Git** | Clone this repository. | [git-scm.com](https://git-scm.com/) |

**You do NOT need:** Docker, a GPU, or 16GB+ RAM. Everything heavy runs in the cloud.

---

## Quick Setup

### Step 1 — Clone & Configure

```bash
git clone https://github.com/iakhileshnanda/myMayaMIRO.git
cd myMayaMIRO
cp .env.example .env
```

### Step 2 — Get Your API Keys

**NVIDIA NIM** (free):
1. Go to [integrate.api.nvidia.com](https://integrate.api.nvidia.com)
2. Sign up and generate an API key
3. Paste into `.env` as `LLM_API_KEY` and `EMBEDDING_API_KEY`

**Neo4j Aura** (free):
1. Go to [neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free/)
2. Create a free instance
3. Download the credentials file — it contains your URI, username, and password
4. Update `.env` with these values

### Step 3 — Update `.env`

```ini
# AI Brain — NVIDIA NIM API
LLM_API_KEY=your_nvidia_nim_key
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL_NAME=qwen/qwen3.5-397b-a17b

# Graph Database — Neo4j Aura
NEO4J_URI=neo4j+ssc://YOUR_INSTANCE_ID.databases.neo4j.io
NEO4J_USER=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password

# Text-to-Vector — NVIDIA NIM Embeddings
EMBEDDING_MODEL=nvidia/nv-embed-v1
EMBEDDING_BASE_URL=https://integrate.api.nvidia.com/v1
EMBEDDING_API_KEY=your_nvidia_nim_key
```

> **Note:** Use `neo4j+ssc://` (not `neo4j+s://`) to avoid SSL certificate verification issues on Windows. The `ssc` variant skips certificate checks, which is fine for Aura's self-signed certs.

### Step 4 — Start the Backend

**Windows:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**Linux (Ubuntu/Debian) — First-time setup:**
```bash
# Install Python 3.11 (Ubuntu 24.04 ships with 3.12 which is incompatible)
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv

# Create virtual environment and install dependencies
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

> **Note:** Python 3.11 is required on Linux because `camel-oasis` does not support Python 3.12+. You only need to create the venv once.

**Linux — Every subsequent run:**
```bash
cd backend
source venv/bin/activate
python run.py
```

The backend starts at **http://localhost:5001**.

### Step 5 — Start the Frontend

Open a **new terminal** (keep the backend running):

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at **http://localhost:3000**.

### Step 6 — Open the App

Navigate to **http://localhost:3000** in your browser. You should see the Maya MIRO interface.

---

## Configuration Reference

Every `.env` variable explained:

| Variable | What It Controls | Default | Example |
|----------|-----------------|---------|---------|
| `LLM_API_KEY` | API key for the LLM provider. For NVIDIA NIM, starts with `nvapi-`. For Ollama, set to `ollama`. | *(none — required)* | `nvapi-abc123...` |
| `LLM_BASE_URL` | The URL where LLM API requests are sent. NVIDIA NIM or Ollama's OpenAI-compatible endpoint. | `http://localhost:11434/v1` | `https://integrate.api.nvidia.com/v1` |
| `LLM_MODEL_NAME` | Which LLM model to use for all AI tasks (entity extraction, agent simulation, report generation). | `qwen2.5:32b` | `qwen/qwen3.5-397b-a17b` |
| `NEO4J_URI` | Connection string for Neo4j. Use `neo4j+ssc://` for Aura cloud, `bolt://` for local Docker. | `bolt://localhost:7687` | `neo4j+ssc://xxx.databases.neo4j.io` |
| `NEO4J_USER` | Neo4j database username. | `neo4j` | `430710be` |
| `NEO4J_PASSWORD` | Neo4j database password. | `mirofish` | *(from Aura dashboard)* |
| `EMBEDDING_MODEL` | Which model converts text to vectors for similarity search. | `nomic-embed-text` | `nvidia/nv-embed-v1` |
| `EMBEDDING_BASE_URL` | API endpoint for the embedding model. | `http://localhost:11434` | `https://integrate.api.nvidia.com/v1` |
| `EMBEDDING_API_KEY` | API key for embedding requests. Same as `LLM_API_KEY` for NVIDIA NIM. | *(empty)* | `nvapi-abc123...` |
| `REPORT_AGENT_MAX_TOOL_CALLS` | Max tool calls per report section. Lower = fewer API calls but less detailed report. | `5` | `3` |
| `REPORT_AGENT_MAX_REFLECTION_ROUNDS` | Max reflection rounds per report section. Lower = faster but less polished. | `2` | `1` |

---

## Switching LLM Providers (OpenRouter, Groq, Ollama)

Maya MIRO uses the **OpenAI SDK format** for all LLM calls. Any OpenAI-compatible API works — you only need to change 3 variables in `.env`.

### Provider Quick Reference

| Provider | `LLM_API_KEY` | `LLM_BASE_URL` | `LLM_MODEL_NAME` | Notes |
|----------|--------------|-----------------|-------------------|-------|
| **NVIDIA NIM** | `nvapi-...` | `https://integrate.api.nvidia.com/v1` | `qwen/qwen3.5-397b-a17b` | Free tier, rate-limited. Best for small tests. |
| **OpenRouter** | `sk-or-v1-...` | `https://openrouter.ai/api/v1` | `qwen/qwen3-235b-a22b` | Pay-per-token, many models. Best for full runs. |
| **Groq** | `gsk_...` | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` | Very fast inference, free tier available. |
| **Ollama** | `ollama` | `http://localhost:11434/v1` | `qwen2.5:32b` | Fully local, needs 16GB+ RAM and GPU. |

### How to Switch

Edit your `.env` file — only these 3 lines change:

```ini
# Example: Switch to OpenRouter
LLM_API_KEY=sk-or-v1-your-openrouter-key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=qwen/qwen3-235b-a22b
```

```ini
# Example: Switch to Groq
LLM_API_KEY=gsk_your-groq-key
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL_NAME=llama-3.3-70b-versatile
```

> **Important:** Keep the `EMBEDDING_*` variables pointed at NVIDIA NIM even if you switch the LLM provider. Embeddings are cheap (no rate limit issues) and OpenRouter/Groq don't natively support the embedding models Maya MIRO uses. You can use a different NVIDIA NIM key or the same one — embedding calls are lightweight.

### Why Switch?

The **Report Generation stage (Stage 5)** makes **30–50+ LLM calls** for a single report:
- 1 call to plan the outline (typically 5–6 sections)
- Per section: up to 5 tool calls + 3 reflection rounds ≈ 8 LLM calls each
- The `interview_agents` tool can interview 5–10 agents, each needing its own LLM call

NVIDIA NIM's free tier rate limit often can't handle this burst. Maya MIRO includes **automatic retry with exponential backoff** (waits 10s → 20s → 40s → 60s on 429 errors), but switching to a provider with higher rate limits (OpenRouter, Groq) avoids the slowdown entirely.

### Reducing API Calls (Free Tier Optimization)

If you're staying on a rate-limited free tier, add these to `.env` to reduce report complexity:

```ini
REPORT_AGENT_MAX_TOOL_CALLS=3
REPORT_AGENT_MAX_REFLECTION_ROUNDS=1
```

This cuts report API calls roughly in half, at the cost of slightly less detailed reports.

---

## How to Run Your First Simulation

Once the app is running at **http://localhost:3000**, follow these steps:

### 1. Upload a Reality Seed

A **reality seed** is the document that defines the "world" your agents will react to. It can be:
- A financial news article (`.txt`)
- An earnings report (`.pdf`)
- An RBI policy document (`.md`)

Click the upload area and select your file (max 50MB). The file is parsed and the raw text is extracted.

### 2. Generate Ontology (Stage 1)

Click **"Generate Ontology"**. The AI reads your document and identifies:
- **Entity types** — e.g., `RetailInvestor`, `CentralBankOfficial`, `EnergyCorporation`
- **Relation types** — e.g., `INVESTS_IN`, `REGULATES`, `INFLUENCES_SENTIMENT`

This takes 10-30 seconds. You'll see the generated types appear on screen.

### 3. Build Knowledge Graph (Stage 2)

Click **"Build Graph"**. The system:
- Splits your document into 500-character chunks
- Extracts entities and relationships from each chunk using the LLM
- Converts entities to vector embeddings for similarity search
- Writes everything to Neo4j

You'll see a count of nodes and edges when complete (e.g., "15 Entity Nodes, 8 Relation Edges").

### 4. Create Simulation Environment (Stage 3)

Click **"Create Environment"**. The system generates hundreds of AI agent profiles — each with:
- A name, age, and occupation
- Investment style (bullish/bearish/neutral)
- Influence level (how much others listen to them)
- Panic threshold (how easily they change their mind)

### 5. Run Simulation (Stage 4)

Click **"Run Simulation"**. Agents begin interacting:
- They post opinions on simulated Twitter/Reddit
- They read each other's posts
- They argue, agree, shift their stance
- Each round represents one simulated hour

Default: 10 rounds. You can watch the activity feed in real time.

### 6. Read the Report (Stage 5)

Once simulation completes, click **"Generate Report"**. The ReportAgent:
- Analyzes all posts and opinion shifts
- Queries the knowledge graph for supporting evidence
- Generates a structured sentiment analysis

### 7. Chat with Agents

After the report, you can chat with any individual agent. Ask questions like:
- "Why are you bearish on this stock?"
- "What changed your mind in round 5?"
- "What evidence supports your position?"

---

## Project Structure

```
myMayaMIRO/
|
|-- .env                              # Your API keys and database credentials (never commit this)
|-- .env.example                      # Template for .env (safe to commit)
|-- README.md                         # This file
|-- ROADMAP.md                        # Future plans and version milestones
|
|-- backend/                          # Python backend (Flask)
|   |-- run.py                        # Entry point: starts the Flask server on port 5001
|   |-- requirements.txt              # Python dependencies
|   |-- app/
|   |   |-- __init__.py               # App factory: initializes Neo4j connection, CORS, blueprints
|   |   |-- config.py                 # Reads .env and exposes all settings to the app
|   |   |
|   |   |-- api/                      # REST API routes (what the frontend calls)
|   |   |   |-- graph.py              # /api/graph/* — upload, ontology, graph build
|   |   |   |-- simulation.py         # /api/simulation/* — create, run, status
|   |   |   |-- report.py             # /api/report/* — generate report, chat
|   |   |
|   |   |-- services/                 # Business logic (the "brain")
|   |   |   |-- ontology_generator.py       # Stage 1: Document --> entity/relation types
|   |   |   |-- graph_builder.py            # Stage 2: Document --> Neo4j knowledge graph
|   |   |   |-- simulation_config_generator.py  # Stage 3: Graph --> agent profiles
|   |   |   |-- oasis_profile_generator.py  # Generates OASIS-compatible agent configs
|   |   |   |-- simulation_runner.py        # Stage 4: Runs the multi-agent simulation
|   |   |   |-- simulation_manager.py       # Manages simulation lifecycle
|   |   |   |-- report_agent.py             # Stage 5: Generates sentiment report
|   |   |   |-- entity_reader.py            # Reads entities from Neo4j (replaced Zep)
|   |   |   |-- graph_tools.py              # LLM tools for querying the graph
|   |   |   |-- graph_memory_updater.py     # Updates graph with simulation results
|   |   |   |-- text_processor.py           # Text chunking (500 char, 50 overlap)
|   |   |
|   |   |-- storage/                  # Data access layer (database operations)
|   |   |   |-- neo4j_storage.py      # All Neo4j read/write operations
|   |   |   |-- graph_storage.py      # Abstract interface (so you can swap databases)
|   |   |   |-- embedding_service.py  # Text --> vector via NVIDIA NIM
|   |   |   |-- ner_extractor.py      # Named Entity Recognition via LLM
|   |   |   |-- search_service.py     # Hybrid search (70% vector + 30% keyword)
|   |   |   |-- neo4j_schema.py       # Database schema and index definitions
|   |   |
|   |   |-- models/                   # Data models
|   |   |   |-- project.py            # Project state management
|   |   |   |-- task.py               # Background task tracking
|   |
|   |-- uploads/                      # Uploaded documents and simulation data
|
|-- frontend/                         # Vue.js frontend (Vite)
|   |-- src/
|   |   |-- views/                    # Page-level components
|   |   |   |-- Home.vue              # Landing page
|   |   |   |-- MainView.vue          # Main simulation workflow
|   |   |   |-- SimulationView.vue    # Simulation control panel
|   |   |   |-- ReportView.vue        # Sentiment report display
|   |   |   |-- InteractionView.vue   # Agent chat interface
|   |   |
|   |   |-- components/               # Reusable UI components
|   |   |   |-- Step1GraphBuild.vue   # Ontology + graph build UI
|   |   |   |-- Step2EnvSetup.vue     # Environment setup UI
|   |   |   |-- Step3Simulation.vue   # Simulation runner UI
|   |   |   |-- Step4Report.vue       # Report display UI
|   |   |   |-- Step5Interaction.vue  # Agent chat UI
|   |   |   |-- GraphPanel.vue        # Graph visualization
|   |   |
|   |   |-- api/                      # API client (Axios calls to backend)
|   |   |   |-- graph.js              # Graph API calls
|   |   |   |-- simulation.js         # Simulation API calls
|   |   |   |-- report.js             # Report API calls
|   |   |
|   |   |-- router/index.js          # Vue Router configuration
|   |   |-- store/pendingUpload.js    # Upload state management
|   |   |-- App.vue                   # Root component
|   |   |-- main.js                   # App entry point
|   |
|   |-- vite.config.js               # Dev server config (proxies API to port 5001)
|   |-- package.json                  # Node.js dependencies
|
|-- docs/
|   |-- technical.md                  # Detailed technical deep dive
|   |-- progress.md                   # Migration progress from Zep to Neo4j
```

---

## How It Works (Simplified Architecture)

```
                        +------------------+
                        |   Your Browser   |
                        |  (Vue.js + Vite) |
                        +--------+---------+
                                 |
                            HTTP REST API
                                 |
                        +--------v---------+
                        |   Flask Backend  |
                        |   (Python 3.11)  |
                        +--------+---------+
                                 |
              +------------------+------------------+
              |                  |                  |
     +--------v-------+ +-------v--------+ +-------v--------+
     | NVIDIA NIM API | | Neo4j Aura     | | CAMEL-OASIS    |
     | (Cloud)        | | (Cloud)        | | (Local)        |
     |                | |                | |                |
     | - Qwen 3.5 LLM| | - Graph DB     | | - Agent Engine |
     | - nv-embed-v1  | | - Nodes/Edges  | | - Twitter/Reddit|
     | - 397B params  | | - Vector Index | | - Opinion Sim  |
     +----------------+ +----------------+ +----------------+
```

**Data flow in one sentence:** Your document is chunked and fed to the LLM, which extracts entities and relationships into a Neo4j knowledge graph; CAMEL-OASIS then spawns hundreds of AI agents who read the graph, form opinions, argue on simulated social media, and a ReportAgent summarizes the resulting sentiment shifts.

---

## Troubleshooting Common Issues

### "ModuleNotFoundError: No module named 'flask'"
You forgot to activate the virtual environment (Linux) or install dependencies.
```bash
# Linux
source venv/bin/activate
pip install -r requirements.txt

# Windows
pip install -r requirements.txt
```

### "camel-oasis: No matching distribution found"
Your Python version is 3.12+. `camel-oasis==0.2.5` requires Python <3.12.
- **Linux:** Install Python 3.11 via deadsnakes PPA (see setup instructions above)
- **Windows:** Download and install [Python 3.11](https://www.python.org/downloads/release/python-3119/) specifically

### "externally-managed-environment" error on Linux
Ubuntu 24.04 blocks system-wide pip installs. Always use a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "neo4j.exceptions.ServiceUnavailable" or connection timeout
- Check that your `NEO4J_URI` in `.env` starts with `neo4j+ssc://` (not `neo4j+s://` or `bolt://`) when using Aura
- Verify your Neo4j Aura instance is running (check the Aura dashboard)
- Make sure your password has no trailing spaces in `.env`

### "LLM_API_KEY not configured"
Your `.env` file is missing or `LLM_API_KEY` is empty. Copy the example and fill in your key:
```bash
cp .env.example .env
# Then edit .env with your NVIDIA NIM key
```

### Port 5001 or 5173 already in use
Another process is using that port. Find and kill it:
```bash
# Linux
lsof -i :5001
kill -9 <PID>

# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### Simulation is slow or timing out
- NVIDIA NIM free tier has rate limits. If you hit them, wait a minute and retry.
- Reduce simulation rounds: the default is 10. For testing, 3-5 rounds is enough.
- Check your internet connection — all LLM calls go to NVIDIA's cloud.

### High token costs
NVIDIA NIM free tier gives limited credits. To reduce usage:
- Use shorter documents (1-2 pages)
- Reduce simulation rounds in the config
- The 397B model is expensive per call — for testing, you can temporarily switch `LLM_MODEL_NAME` to a smaller model like `qwen/qwen2.5-7b-instruct`

---

## Hardware Requirements

| Component | Requirement |
|-----------|------------|
| **RAM** | ~2GB |
| **GPU** | Not needed |
| **Disk** | ~5GB |
| **Internet** | Required (NVIDIA NIM + Neo4j Aura) |
| **OS** | Windows 10+, Ubuntu 22.04+ |

---

## API Routes Reference

| Method | Route | Purpose |
|--------|-------|---------|
| `POST` | `/api/graph/ontology/generate` | Upload document, generate entity/relation types |
| `POST` | `/api/graph/build` | Build knowledge graph from document |
| `GET` | `/api/graph/task/{id}` | Check progress of a background task |
| `POST` | `/api/simulation/create` | Create simulation environment with agent profiles |
| `POST` | `/api/simulation/run` | Start the multi-agent simulation |
| `POST` | `/api/report/generate` | Generate sentiment analysis report |

---

## Resources & Credits

| Resource | Link |
|----------|------|
| **Original MiroFish** | [github.com/666ghj/MiroFish](https://github.com/666ghj/MiroFish) |
| **MiroFish-Offline fork** | [github.com/nikmcfly/MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) |
| **Maya MIRO (this repo)** | [github.com/iakhileshnanda/myMayaMIRO](https://github.com/iakhileshnanda/myMayaMIRO) |
| **NVIDIA NIM** | [integrate.api.nvidia.com](https://integrate.api.nvidia.com) |
| **Neo4j Aura** | [neo4j.com/cloud/aura-free](https://neo4j.com/cloud/aura-free/) |
| **CAMEL-AI / OASIS** | [github.com/camel-ai/camel](https://github.com/camel-ai/camel) |
| **Technical Deep Dive** | [docs/technical.md](docs/technical.md) |
| **Migration Progress** | [docs/progress.md](docs/progress.md) |
| **Roadmap** | [ROADMAP.md](ROADMAP.md) |

---

## License

AGPL-3.0 — See [LICENSE](LICENSE) for details.

Built by [Akhilesh Nanda](https://github.com/iakhileshnanda).
