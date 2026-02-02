"""
🎤 cagent Antakshari Live - Real Backend
This actually runs cagent and streams results to the web UI!

Usage:
    pip install fastapi uvicorn websockets
    python antakshari_server.py
    
Then open http://localhost:8000 in your browser
"""

import asyncio
import subprocess
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="cagent Antakshari Live")

# Store active game state
game_state = {
    "is_playing": False,
    "current_letter": "D",
    "round": 0,
    "songs": [],
    "current_agent_index": 0
}

# Agent definitions
AGENTS = [
    {"id": "bytebeat", "name": "ByteBeat", "emoji": "🎤", "yaml": "agents/bytebeat-singer.yaml"},
    {"id": "remixraja", "name": "RemixRaja", "emoji": "🎧", "yaml": "agents/remix-raja.yaml"},
]

async def run_cagent(prompt: str, agent_yaml: str = "agents/antakshari-game.yaml") -> str:
    """Actually run cagent and return the output"""
    try:
        # Run cagent command
        process = await asyncio.create_subprocess_exec(
            "cagent", "run", agent_yaml, "-p", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ}
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=120  # 2 minute timeout
        )
        
        if process.returncode == 0:
            return stdout.decode('utf-8')
        else:
            return f"Error: {stderr.decode('utf-8')}"
            
    except asyncio.TimeoutError:
        return "Error: cagent timed out"
    except FileNotFoundError:
        return "Error: cagent not found. Make sure Docker Desktop 4.49+ is installed."
    except Exception as e:
        return f"Error: {str(e)}"


async def run_cagent_streaming(prompt: str, websocket: WebSocket, agent_yaml: str = "agents/antakshari-game.yaml"):
    """Run cagent and stream output line by line"""
    try:
        process = await asyncio.create_subprocess_exec(
            "cagent", "run", agent_yaml, "-p", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ}
        )
        
        # Stream stdout line by line
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            text = line.decode('utf-8')
            await websocket.send_json({
                "type": "stream",
                "content": text
            })
            
        await process.wait()
        
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "content": str(e)
        })


@app.websocket("/ws/antakshari")
async def websocket_antakshari(websocket: WebSocket):
    """WebSocket endpoint for real-time Antakshari game"""
    await websocket.accept()
    
    try:
        while True:
            # Receive command from client
            data = await websocket.receive_json()
            command = data.get("command")
            
            if command == "start":
                game_state["is_playing"] = True
                game_state["current_letter"] = data.get("letter", "D")
                game_state["round"] = 0
                game_state["songs"] = []
                
                await websocket.send_json({
                    "type": "status",
                    "content": "Game started!",
                    "state": game_state
                })
                
            elif command == "next_round":
                if not game_state["is_playing"]:
                    continue
                    
                letter = game_state["current_letter"]
                game_state["round"] += 1
                
                # Notify client we're thinking
                await websocket.send_json({
                    "type": "thinking",
                    "agent": AGENTS[game_state["current_agent_index"] % len(AGENTS)],
                    "letter": letter
                })
                
                # Actually run cagent!
                prompt = f"Play Antakshari. Sing a song starting with the letter '{letter}'. Make it short (4-6 lines). Clearly state what letter the song ends with."
                
                await websocket.send_json({
                    "type": "singing",
                    "agent": AGENTS[game_state["current_agent_index"] % len(AGENTS)],
                })
                
                # Run cagent and stream output
                await run_cagent_streaming(prompt, websocket)
                
                # Move to next agent
                game_state["current_agent_index"] += 1
                
                await websocket.send_json({
                    "type": "round_complete",
                    "state": game_state
                })
                
            elif command == "stop":
                game_state["is_playing"] = False
                await websocket.send_json({
                    "type": "status",
                    "content": "Game stopped",
                    "state": game_state
                })
                
            elif command == "single_prompt":
                # Run a single prompt through cagent
                prompt = data.get("prompt", "Create a short Hindi song")
                agent_yaml = data.get("agent", "agents/session-host.yaml")
                
                await websocket.send_json({
                    "type": "thinking",
                    "content": f"Running cagent with: {prompt[:50]}..."
                })
                
                await run_cagent_streaming(prompt, websocket, agent_yaml)
                
                await websocket.send_json({
                    "type": "complete"
                })
                
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


# Serve the HTML UI
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎤 cagent Antakshari Live (Real!)</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen p-4">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-6">
            <h1 class="text-3xl font-bold text-gray-800">🎤 cagent Antakshari Live 🎵</h1>
            <p class="text-gray-500 text-sm">Real AI Agents via Docker cagent</p>
            <div id="connectionStatus" class="text-xs mt-2 text-yellow-600">Connecting...</div>
        </div>

        <!-- Controls -->
        <div class="bg-white rounded-xl p-4 mb-4 shadow-sm">
            <div class="flex items-center justify-between flex-wrap gap-4">
                <div class="flex items-center gap-4">
                    <div>
                        <label class="text-xs text-gray-500">Starting Letter</label>
                        <input type="text" id="letterInput" value="D" maxlength="1" 
                            class="w-16 text-2xl font-bold text-center border rounded p-1">
                    </div>
                    <div>
                        <label class="text-xs text-gray-500">Round</label>
                        <div id="roundDisplay" class="text-2xl font-bold text-purple-600">0</div>
                    </div>
                </div>
                <div class="flex gap-2">
                    <button onclick="startGame()" id="startBtn"
                        class="bg-green-500 text-white px-6 py-2 rounded-full font-bold hover:bg-green-600">
                        ▶ Start
                    </button>
                    <button onclick="nextRound()" id="nextBtn" disabled
                        class="bg-purple-500 text-white px-6 py-2 rounded-full font-bold hover:bg-purple-600 disabled:opacity-50">
                        Next Round
                    </button>
                    <button onclick="stopGame()" 
                        class="bg-red-500 text-white px-6 py-2 rounded-full font-bold hover:bg-red-600">
                        ⏹ Stop
                    </button>
                </div>
            </div>
        </div>

        <!-- Current Action -->
        <div id="currentAction" class="hidden bg-white rounded-xl p-4 mb-4 shadow-sm border-2 border-purple-300">
            <div id="actionContent" class="text-gray-700"></div>
        </div>

        <!-- Output Feed -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gray-50 px-4 py-2 border-b font-bold text-gray-700">
                🎵 cagent Output (Real!)
            </div>
            <div id="outputFeed" class="p-4 max-h-96 overflow-y-auto font-mono text-sm whitespace-pre-wrap bg-gray-900 text-green-400">
                Waiting for game to start...
            </div>
        </div>

        <!-- Custom Prompt -->
        <div class="bg-white rounded-xl p-4 mt-4 shadow-sm">
            <div class="text-sm font-bold text-gray-700 mb-2">🎯 Custom Prompt (Direct cagent)</div>
            <div class="flex gap-2">
                <input type="text" id="customPrompt" placeholder="Enter any prompt for cagent..."
                    class="flex-1 border rounded px-3 py-2">
                <select id="agentSelect" class="border rounded px-3 py-2">
                    <option value="agents/session-host.yaml">Session Host</option>
                    <option value="agents/antakshari-game.yaml">Antakshari</option>
                    <option value="agents/bytebeat-singer.yaml">ByteBeat</option>
                    <option value="agents/the-judge-critic.yaml">The Judge</option>
                </select>
                <button onclick="runCustom()" class="bg-blue-500 text-white px-4 py-2 rounded font-bold hover:bg-blue-600">
                    Run cagent
                </button>
            </div>
        </div>

        <div class="text-center mt-6 text-gray-400 text-sm">
            <p>🐳 Powered by Docker cagent | github.com/ajeetraina/docker-cagent-antakshari</p>
        </div>
    </div>

    <script>
        let ws;
        let isPlaying = false;
        let round = 0;

        function connect() {
            ws = new WebSocket(`ws://${window.location.host}/ws/antakshari`);
            
            ws.onopen = () => {
                document.getElementById('connectionStatus').textContent = '● Connected to cagent backend';
                document.getElementById('connectionStatus').className = 'text-xs mt-2 text-green-600';
            };
            
            ws.onclose = () => {
                document.getElementById('connectionStatus').textContent = '○ Disconnected - Reconnecting...';
                document.getElementById('connectionStatus').className = 'text-xs mt-2 text-red-600';
                setTimeout(connect, 2000);
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
        }

        function handleMessage(data) {
            const output = document.getElementById('outputFeed');
            const action = document.getElementById('currentAction');
            const actionContent = document.getElementById('actionContent');
            
            switch(data.type) {
                case 'thinking':
                    action.classList.remove('hidden');
                    actionContent.innerHTML = `
                        <div class="flex items-center gap-2">
                            <span class="text-2xl">${data.agent?.emoji || '🤔'}</span>
                            <span class="font-bold">${data.agent?.name || 'Agent'}</span>
                            <span class="text-gray-500">is thinking about "${data.letter}"...</span>
                            <span class="animate-pulse">●●●</span>
                        </div>
                    `;
                    break;
                    
                case 'singing':
                    actionContent.innerHTML = `
                        <div class="flex items-center gap-2">
                            <span class="text-2xl">${data.agent?.emoji || '🎤'}</span>
                            <span class="font-bold">${data.agent?.name || 'Agent'}</span>
                            <span class="text-purple-600">is singing...</span>
                        </div>
                    `;
                    break;
                    
                case 'stream':
                    output.textContent += data.content;
                    output.scrollTop = output.scrollHeight;
                    break;
                    
                case 'round_complete':
                    action.classList.add('hidden');
                    round = data.state?.round || round;
                    document.getElementById('roundDisplay').textContent = round;
                    document.getElementById('nextBtn').disabled = false;
                    break;
                    
                case 'status':
                    output.textContent += '\\n--- ' + data.content + ' ---\\n';
                    break;
                    
                case 'complete':
                    action.classList.add('hidden');
                    document.getElementById('nextBtn').disabled = false;
                    break;
                    
                case 'error':
                    output.textContent += '\\n[ERROR] ' + data.content + '\\n';
                    action.classList.add('hidden');
                    break;
            }
        }

        function startGame() {
            const letter = document.getElementById('letterInput').value.toUpperCase() || 'D';
            document.getElementById('outputFeed').textContent = '🎮 Starting Antakshari with letter: ' + letter + '\\n\\n';
            round = 0;
            document.getElementById('roundDisplay').textContent = '0';
            ws.send(JSON.stringify({ command: 'start', letter }));
            document.getElementById('nextBtn').disabled = false;
            isPlaying = true;
        }

        function nextRound() {
            document.getElementById('nextBtn').disabled = true;
            document.getElementById('outputFeed').textContent += '\\n--- Round ' + (round + 1) + ' ---\\n';
            ws.send(JSON.stringify({ command: 'next_round' }));
        }

        function stopGame() {
            ws.send(JSON.stringify({ command: 'stop' }));
            isPlaying = false;
            document.getElementById('currentAction').classList.add('hidden');
        }

        function runCustom() {
            const prompt = document.getElementById('customPrompt').value;
            const agent = document.getElementById('agentSelect').value;
            if (!prompt) return;
            
            document.getElementById('outputFeed').textContent = '🚀 Running: ' + prompt + '\\n\\n';
            document.getElementById('nextBtn').disabled = true;
            ws.send(JSON.stringify({ 
                command: 'single_prompt',
                prompt,
                agent
            }));
        }

        // Connect on load
        connect();
    </script>
</body>
</html>
"""

@app.get("/")
async def get_ui():
    return HTMLResponse(content=HTML_CONTENT)


if __name__ == "__main__":
    print("🎤 cagent Antakshari Live Server")
    print("=" * 40)
    print("Starting server at http://localhost:8000")
    print("Make sure you have:")
    print("  1. Docker Desktop 4.49+ installed")
    print("  2. OPENAI_API_KEY set")
    print("  3. cagent available in PATH")
    print("=" * 40)
    uvicorn.run(app, host="0.0.0.0", port=8000)
