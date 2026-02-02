# 🎤 cagent-antakshari

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
- API key for your preferred LLM provider

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
# Run a full music session (all agents collaborate)
cagent run agents/session-host.yaml

# Run individual agents
cagent run agents/bytebeat-singer.yaml      # Create a song
cagent run agents/the-judge-critic.yaml     # Review a song
cagent run agents/hypeboi-fan.yaml          # Hype a song
cagent run agents/remix-raja.yaml           # Remix a song

# Play Antakshari mode!
cagent run agents/antakshari-game.yaml
```

## 🎭 Meet the Agents

| Agent | Role | Personality |
|-------|------|-------------|
| 🎤 **ByteBeat** | Songwriter | Creative artist inspired by A.R. Rahman, Daft Punk, Taylor Swift |
| ⭐ **The Judge** | Critic | Sharp, witty reviewer (Simon Cowell meets Anthony Fantano) |
| 🔥 **HypeBoi3000** | Superfan | Maximum energy, emojis, pure positivity |
| 🎧 **RemixRaja** | Producer | Flips genres, creates answer tracks |
| 🎵 **Antakshari Master** | Game Host | Runs the classic song chain game |

## 📁 Project Structure

```
cagent-antakshari/
├── agents/
│   ├── bytebeat-singer.yaml      # Song creator agent
│   ├── the-judge-critic.yaml     # Music critic agent
│   ├── hypeboi-fan.yaml          # Hype fan agent
│   ├── remix-raja.yaml           # Remix producer agent
│   ├── session-host.yaml         # Multi-agent orchestrator
│   └── antakshari-game.yaml      # Antakshari game mode
├── examples/
│   ├── sample-session.md         # Example output
│   └── song-themes.md            # Theme ideas
├── docs/
│   └── how-it-works.md           # Detailed documentation
└── README.md
```

## 🎮 Game Modes

### 1. Free Session
Run `session-host.yaml` - Agents collaborate to create, review, and remix songs on any topic.

### 2. Antakshari Mode
Run `antakshari-game.yaml` - Classic Indian game! Each agent must sing a song starting with the last letter of the previous song.

### 3. Battle Mode (Coming Soon)
Two songwriter agents compete, critics vote on the winner!

## 📝 Sample Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 cagent Antakshari - Music Feed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 @ByteBeat just dropped a new track!

🎤 "DOCKER DREAMS"
Genre: Synthwave / Electronic Pop

[Verse 1]
Spinning up containers in the midnight glow
Every microservice has a place to go
YAML files like poetry, configs so clean
Building something bigger than we've ever seen

[Chorus]
Docker dreams, running in the cloud
Ship it once, ship it proud
From my laptop to the world
Watch these containers unfurl

— ByteBeat 🎵

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 @TheJudge: "ByteBeat delivers a catchy ode to 
containerization. The chorus is an earworm. 7/10 
- Would mass-deploy."

💬 @HypeBoi3000: "BRO THIS SLAPS 🔥🔥🔥 
'SHIP IT ONCE SHIP IT PROUD' IS MY NEW MOTTO 💯"

🔄 @RemixRaja dropped a Lo-Fi remix!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

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
- [awesome-docker-cagent](https://github.com/collabnix/awesome-docker-cagent)

## 🙏 Credits

Built with ❤️ by the [Collabnix Community](https://collabnix.com)

Inspired by:
- The timeless Indian game of **Antakshari**
- Docker's vision for AI agents
- Music lovers everywhere

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>🎤 Let the music play! 🎵</b><br>
  <i>Where AI agents jam together</i>
</p>
