# ghostshell_multiplayer_server_render_safe.py
# Render-compatible WebSocket server with browser-origin safe headers

import asyncio
import websockets
import json
import random

PORT = 10000  # Render uses random ports, overridden by runtime
clients = {}

colors = ["red", "green", "blue", "orange", "purple", "cyan", "yellow"]

async def handler(websocket):
    nickname = f"Player{random.randint(100, 999)}"
    color = random.choice(colors)
    clients[websocket] = {"nickname": nickname, "color": color}
    
    print(f"[+] {nickname} connected as {color} ({len(clients)} total)")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                data["nickname"] = clients[websocket]["nickname"]
                data["color"] = clients[websocket]["color"]
                message = json.dumps(data)
            except:
                pass
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"[-] {clients[websocket]['nickname']} disconnected.")
    finally:
        del clients[websocket]

async def main():
    print("🌐 Starting Ghostshell WebSocket server (Render-safe)...")
    async with websockets.serve(
        handler, "0.0.0.0", PORT, origins=["*"]
    ):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
