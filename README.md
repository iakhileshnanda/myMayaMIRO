# 🐟 Maya MIRO — Stock Sentiment Analysis using MiroFish + NVIDIA NIM

> Customized fork of MiroFish-Offline by Akhilesh Nanda  
> Original: https://github.com/nikmcfly/MiroFish-Offline

---

## 🧠 What is this?

Maya MIRO is a stock sentiment analysis tool built on MiroFish — a multi-agent simulation engine. You upload any financial document (earnings report, news article, RBI policy draft, stock analysis) and it generates hundreds of AI agents with unique personalities that simulate how the market reacts. Posts, arguments, opinion shifts — hour by hour.

---

## 🔄 What changed from MiroFish-Offline?

| MiroFish-Offline | Maya MIRO |
|---|---|
| Ollama (local models) | NVIDIA NIM API |
| 16GB RAM minimum | ~2GB RAM (Neo4j only) |
| qwen2.5:32b via Ollama | qwen/qwen3.5-397b-a17b via NVIDIA NIM |
| nomic-embed-text via Ollama | nvidia/nv-embed-v1 via NVIDIA NIM |
| No internet required | NVIDIA NIM API key required |
| Generic use case | Stock sentiment + financial analysis |

---

## 🎯 Use Case

You → upload earnings report or news article  
↓  
Maya MIRO → builds knowledge graph (Neo4j)  
↓  
Generates 100s of agent personas (bulls, bears, retail, institutional)  
↓  
Agents simulate social reactions hour by hour  
↓  
ReportAgent generates sentiment analysis  
↓  
You → cross check with Zerodha charts → make informed trade decision

---

## ⚙️ How It Works (5 Stages)

1. **Graph Build** — Extracts entities (companies, events, financial signals) from your document. Builds knowledge graph in Neo4j.
2. **Env Setup** — Generates hundreds of agent personas with unique personality, opinion bias (bullish/bearish), reaction speed, influence level.
3. **Simulation** — Agents interact on simulated social platforms: posting, replying, arguing, shifting opinions. Tracks sentiment evolution in real time.
4. **Report** — ReportAgent analyzes post-simulation environment and generates structured sentiment report.
5. **Interaction** — Chat with any agent from the simulated world. Full memory and personality persists.

---

## 🛠️ Setup (No Ollama needed)

### Prerequisites
- Docker Desktop installed
- NVIDIA NIM API key from https://integrate.api.nvidia.com

### Step 1 — Clone
```bash
git clone https://github.com/iakhileshnanda/myMayaMIRO.git
cd myMayaMIRO
cp .env.example .env
```

### Step 2 — Add your NVIDIA key in .env
```
LLM_API_KEY=your_actual_nvidia_nim_key
EMBEDDING_API_KEY=your_actual_nvidia_nim_key
```

### Step 3 — Start Neo4j only
```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/mirofish \
  neo4j:5.15-community
```

### Step 4 — Run backend
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Step 5 — Run frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## 💻 Hardware Requirements

| Component | Maya MIRO | Original MiroFish-Offline |
|---|---|---|
| RAM | ~2GB (Neo4j only) | 16GB minimum |
| GPU | Not needed | 10GB VRAM minimum |
| Disk | 5GB | 20GB |
| Internet | Required (NVIDIA NIM) | Not required |

---

## 🔑 Get NVIDIA NIM API Key
1. Go to https://integrate.api.nvidia.com
2. Sign up / log in
3. Generate free API key
4. Paste in .env

---

## 📌 Credits
- Original MiroFish: https://github.com/666ghj/MiroFish
- MiroFish-Offline fork: https://github.com/nikmcfly/MiroFish-Offline