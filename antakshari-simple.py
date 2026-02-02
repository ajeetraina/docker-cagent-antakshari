#!/usr/bin/env python3
"""
🎤 cagent Antakshari Live
Actually runs cagent and shows output in browser

Usage:
    pip install fastapi uvicorn
    python antakshari_simple.py
"""

import asyncio
import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>🎤 cagent Antakshari Live</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-center mb-2">🎤 cagent Antakshari Live 🎵</h1>
        <p class="text-center text-gray-500 mb-4">Real AI Agents via Docker cagent</p>
        
        <div id="status" class="text-center mb-4 text-yellow-600">Connecting...</div>
        
        <!-- Quick Actions -->
        <div class="bg-white rounded-xl p-4 mb-4 shadow">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm text-gray-600 mb-1">Starting Letter</label>
                    <input type="text" id="letter" value="D" maxlength="1" 
                        class="w-full text-2xl font-bold text-center border rounded p-2">
                </div>
                <div>
                    <label class="block text-sm text-gray-600 mb-1">Agent</label>
                    <select id="agent" class="w-full border rounded p-2 h-12">
                        <option value="agents/antakshari-game.yaml">🎵 Antakshari Game</option>
                        <option value="agents/session-host.yaml">🎭 Session Host</option>
                        <option value="agents/bytebeat-singer.yaml">🎤 ByteBeat Singer</option>
                        <option value="agents/the-judge-critic.yaml">⭐ The Judge</option>
                        <option value="agents/remix-raja.yaml">🎧 RemixRaja</option>
                    </select>
                </div>
            </div>
            
            <div class="mt-4">
                <label class="block text-sm text-gray-600 mb-1">Prompt</label>
                <textarea id="prompt" rows="2"
                    class="w-full border rounded p-2">Play Antakshari! Sing a Hindi song starting with letter D. Keep it short (4-6 lines).</textarea>
            </div>
            
            <button onclick="runCagent()" id="runBtn"
                class="w-full mt-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 rounded-xl font-bold text-lg hover:opacity-90">
                🎤 Run cagent
            </button>
            
            <p class="text-xs text-gray-400 mt-2 text-center">
                Command: echo "[prompt]" | cagent run [agent.yaml]
            </p>
        </div>
        
        <!-- Output -->
        <div class="bg-white rounded-xl shadow overflow-hidden">
            <div class="bg-gray-800 text-white px-4 py-2 flex justify-between items-center">
                <span>🎵 cagent Output</span>
                <button onclick="clearOutput()" class="text-xs bg-gray-600 px-2 py-1 rounded">Clear</button>
            </div>
            <pre id="output" class="p-4 bg-gray-900 text-green-400 h-96 overflow-y-auto text-sm">Click "Run cagent" to start!

This will execute:
  echo "[prompt]" | cagent run [agent.yaml]

And stream the real output here.
</pre>
        </div>
    </div>
    
    <script>
        let ws;
        const output = document.getElementById('output');
        const status = document.getElementById('status');
        const runBtn = document.getElementById('runBtn');
        
        function connect() {
            ws = new WebSocket('ws://' + window.location.host + '/ws');
            
            ws.onopen = () => {
                status.textContent = '● Connected';
                status.className = 'text-center mb-4 text-green-600';
                runBtn.disabled = false;
            };
            
            ws.onclose = () => {
                status.textContent = '○ Disconnected - Reconnecting...';
                status.className = 'text-center mb-4 text-red-600';
                setTimeout(connect, 2000);
            };
            
            ws.onerror = (e) => {
                console.error('WebSocket error:', e);
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'output') {
                    output.textContent += data.text;
                    output.scrollTop = output.scrollHeight;
                } else if (data.type === 'done') {
                    output.textContent += '\\n\\n✅ Done!\\n';
                    runBtn.disabled = false;
                    runBtn.textContent = '🎤 Run cagent';
                } else if (data.type === 'error') {
                    output.textContent += '\\n❌ Error: ' + data.text + '\\n';
                    runBtn.disabled = false;
                    runBtn.textContent = '🎤 Run cagent';
                } else if (data.type === 'start') {
                    output.textContent += '🚀 ' + data.text + '\\n\\n';
                }
            };
        }
        
        function runCagent() {
            const letter = document.getElementById('letter').value.toUpperCase() || 'D';
            const agent = document.getElementById('agent').value;
            let prompt = document.getElementById('prompt').value;
            
            // Replace D with actual letter in prompt
            prompt = prompt.replace(/letter [A-Z]/gi, 'letter ' + letter);
            
            output.textContent = '🎮 Running cagent...\\n';
            output.textContent += '📁 Agent: ' + agent + '\\n';
            output.textContent += '💬 Prompt: ' + prompt + '\\n';
            output.textContent += '─'.repeat(50) + '\\n\\n';
            
            runBtn.disabled = true;
            runBtn.textContent = '⏳ Running...';
            
            ws.send(JSON.stringify({
                agent: agent,
                prompt: prompt
            }));
        }
        
        function clearOutput() {
            output.textContent = '';
        }
        
        connect();
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(HTML)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_json()
            agent = data.get('agent', 'agents/bytebeat-singer.yaml')
            prompt = data.get('prompt', 'Create a short song')
            
            print(f"📥 Received command:")
            print(f"   Agent: {agent}")
            print(f"   Prompt: {prompt[:50]}...")
            
            if not os.path.exists(agent):
                await websocket.send_json({
                    "type": "error",
                    "text": f"Agent file not found: {agent}"
                })
                continue
            
            try:
                await websocket.send_json({
                    "type": "start",
                    "text": f"Running: cagent run {agent}"
                })
                
                # Run cagent with prompt via stdin (no -p flag)
                print(f"🚀 Executing: echo '...' | cagent run {agent}")
                
                process = await asyncio.create_subprocess_exec(
                    "cagent", "run", agent,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                )
                
                # Send prompt via stdin
                process.stdin.write(prompt.encode() + b'\n')
                await process.stdin.drain()
                process.stdin.close()
                
                # Stream output
                while True:
                    line = await process.stdout.readline()
                    if not line:
                        break
                    text = line.decode('utf-8')
                    print(f"   📤 {text.rstrip()}")
                    await websocket.send_json({
                        "type": "output",
                        "text": text
                    })
                
                await process.wait()
                print(f"✅ Process completed with code: {process.returncode}")
                await websocket.send_json({"type": "done"})
                
            except FileNotFoundError:
                await websocket.send_json({
                    "type": "error",
                    "text": "cagent not found! Make sure Docker Desktop 4.49+ is installed."
                })
            except Exception as e:
                print(f"❌ Error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "text": str(e)
                })
                
    except Exception as e:
        print(f"WebSocket closed: {e}")

if __name__ == "__main__":
    print()
    print("🎤 cagent Antakshari Live")
    print("=" * 50)
    print(f"📂 Directory: {os.getcwd()}")
    print(f"📁 agents/ exists: {os.path.exists('agents')}")
    print()
    print("🌐 Open http://localhost:8000")
    print("=" * 50)
    print()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
