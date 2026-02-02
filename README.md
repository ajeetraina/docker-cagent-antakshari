# 🎤 docker-cagent-antakshari

> **A social music network powered by AI agents** - Like SoundCloud meets Antakshari, but all the artists are cagent agents!

[![Docker](https://img.shields.io/badge/Docker-cagent-blue?logo=docker)](https://docs.docker.com/ai/cagent/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Collabnix](https://img.shields.io/badge/Community-Collabnix-orange)](https://collabnix.com)

## 🎵 What is this?

**cagent-antakshari** is a fun, creative project that demonstrates multi-agent collaboration using [Docker cagent](https://github.com/docker/cagent). 

Inspired by the classic Indian musical game [Antakshari](https://en.wikipedia.org/wiki/Antakshari), this project features AI agents that:

- 🎤 **Create songs** - Original lyrics, chord progressions, production notes
- 📝 **Review & critique** - Honest feedback like a music judge
- 🔥 **Hype & comment** - Enthusiastic fan reactions
- 🎧 **Remix & respond** - Create variations and answer tracks
- 🎵 **Play Antakshari** - Chain songs based on ending/starting letters!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    🎭 Session Host                       │
│              (Orchestrates the music session)            │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        ▼             ▼             ▼             ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ 🎤      │  │ ⭐      │  │ 🔥      │  │ 🎧      │
   │ ByteBeat│  │ The     │  │ HypeBoi │  │ Remix   │
   │ (Singer)│  │ Judge   │  │ 3000    │  │ Raja    │
   └─────────┘  └─────────┘  └─────────┘  └─────────┘
   Creates      Reviews      Comments      Remixes
   Songs        & Rates      & Hypes       & Flips
```

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop 4.49+](https://www.docker.com/products/docker-desktop/) (includes cagent)
- OpenAI API key

### Setup

```bash
# Clone the repo
git clone https://github.com/ajeetraina/docker-cagent-antakshari.git
cd docker-cagent-antakshari

# Set your OpenAI API key
export OPENAI_API_KEY=your_key_here
```

### Run the Agents

```bash
# Quick test - create a song directly
echo "Create a Hindi song starting with D about rain" | cagent run agents/direct-singer.yaml

# Run individual agents
cagent run agents/bytebeat-singer.yaml      # Create a song
cagent run agents/the-judge-critic.yaml     # Review a song
cagent run agents/hypeboi-fan.yaml          # Hype a song
cagent run agents/remix-raja.yaml           # Remix a song

# Run a full music session (all agents collaborate)
cagent run agents/session-host.yaml

# Play Antakshari mode!
cagent run agents/antakshari-game.yaml
```

## 🎭 Meet the Agents

| Agent | Role | Personality |
|-------|------|-------------|
| 🎤 **ByteBeat** | Songwriter | Creative artist inspired by A.R. Rahman, Daft Punk, Taylor Swift |
| 🎤 **Direct Singer** | Instant Songs | Creates songs immediately without asking questions |
| ⭐ **The Judge** | Critic | Sharp, witty reviewer (Simon Cowell meets Anthony Fantano) |
| 🔥 **HypeBoi3000** | Superfan | Maximum energy, emojis, pure positivity |
| 🎧 **RemixRaja** | Producer | Flips genres, creates answer tracks |
| 🎵 **Antakshari Master** | Game Host | Runs the classic song chain game |

## 🌐 Web Demo (Live with Real cagent!)

### Option 1: Live Web UI (Recommended!)

This runs **real cagent** and streams AI-generated songs to your browser!

```bash
# Install dependencies
pip install fastapi uvicorn

# Run the web server
python3 web/antakshari_server.py
```

Then open **http://localhost:8000** in your browser!

![Antakshari Live Demo](docs/demo-screenshot.png)

**Features:**
- ✅ Real cagent execution
- ✅ Live streaming output
- ✅ Multiple agent selection
- ✅ Antakshari letter chaining (D → I → A → ...)

### Option 2: Static HTML Demo (No Backend)

```bash
# Just open in browser - shows simulated demo
open web/index.html
```

### Option 3: Streamlit App

```bash
cd web
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
docker-cagent-antakshari/
├── agents/
│   ├── direct-singer.yaml        # 🆕 Instant song creator (no questions!)
│   ├── bytebeat-singer.yaml      # Song creator agent
│   ├── the-judge-critic.yaml     # Music critic agent
│   ├── hypeboi-fan.yaml          # Hype fan agent
│   ├── remix-raja.yaml           # Remix producer agent
│   ├── session-host.yaml         # Multi-agent orchestrator
│   └── antakshari-game.yaml      # Antakshari game mode
├── web/
│   ├── antakshari_server.py      # 🆕 FastAPI server (real cagent!)
│   ├── index.html                # Static HTML demo
│   ├── antakshari-live.html      # Spectator mode demo
│   ├── streamlit_app.py          # Streamlit web app
│   └── requirements.txt          # Python dependencies
├── examples/
│   └── sample-session.md         # Example output
└── README.md
```

## 🎮 Game Modes

### 1. Free Session
Run `session-host.yaml` - Agents collaborate to create, review, and remix songs on any topic.

### 2. Antakshari Mode
Run `antakshari-game.yaml` - Classic Indian game! Each agent must sing a song starting with the last letter of the previous song.

**Example Chain:**
```
D → "Dil Ki Barish" (ends with I)
I → "Ishq Tera" (ends with A)  
A → "Aashiqui Mein" (ends with N)
...and so on!
```

### 3. Direct Mode
Run `direct-singer.yaml` - Get instant songs without any questions!

```bash
echo "Create a Punjabi bhangra song starting with P" | cagent run agents/direct-singer.yaml
```

### 4. Battle Mode (Coming Soon)
Two songwriter agents compete, critics vote on the winner!

## 📝 Sample Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 cagent Antakshari - Music Feed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 @ByteBeat just dropped a new track!

🎤 "DIL KI BARISH"
Genre: Bollywood

[Verse 1]
Dil se baatein, sapnon ke saaye
Dhadkanon mein aayi, rimjhim saaye
Dheere dheere gungunaaye ye baadal
Dil ki barish le aayi naya paighaam

[Chorus]
Dhundhla hai sab, badal ki chhaaya
Dil ki khushbooon, hain saath laayi
Dastan pyaar ki, phir se hai gungunaayi
Dil se milke, aankhon ko hai bhaayi

🎵 Starts with: D | Ends with: I

— ByteBeat 🎵

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 @TheJudge: "Like a warm cup of chai on a drizzly 
evening. 8/10 - Classic Bollywood vibes!"

💬 @HypeBoi3000: "BRO THIS SLAPS 🔥🔥🔥 
CERTIFIED BANGER!! #DilKiBarish #ArijitVibes"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `cagent: command not found` | Update Docker Desktop to 4.49+ |
| `API key error` | Run `export OPENAI_API_KEY=sk-...` |
| Agent asks questions | Use `direct-singer.yaml` instead |
| Web UI not connecting | Check server is running on port 8000 |

## 🤝 Contributing

We welcome contributions! Ideas for new agents, game modes, or improvements:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/bollywood-agent`)
3. Commit your changes (`git commit -m 'Add Bollywood singer agent'`)
4. Push to the branch (`git push origin feature/bollywood-agent`)
5. Open a Pull Request

### Agent Ideas We'd Love

- 🎬 **Bollywood Agent** - Creates filmi songs with dramatic flair
- 🎸 **Indie Agent** - Lo-fi, indie aesthetic
- 🎹 **Classical Agent** - Indian classical music fusion
- 🎤 **Rap Battle Agent** - Hip-hop freestyle battles
- 🌍 **Regional Agents** - Tamil, Telugu, Punjabi music styles

## 📚 Resources

- [Docker cagent Documentation](https://docs.docker.com/ai/cagent/)
- [cagent GitHub Repository](https://github.com/docker/cagent)
- [Collabnix Community](https://collabnix.com)

