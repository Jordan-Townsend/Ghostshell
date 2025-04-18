# ghostshell_multiplayer_server_v2.py
# Patched Python 3.12-compatible multiplayer server with nicknames and symbolic sync

import asyncio
import websockets
import json
import random

PORT = 8765
clients = {}

colors = ["red", "green", "blue", "orange", "purple", "cyan", "yellow"]

async def handler(websocket):
    # Assign nickname and color
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
                pass  # Leave raw if not json
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        print(f"[-] {clients[websocket]['nickname']} disconnected.")
    finally:
        del clients[websocket]

async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"🌐 Ghostshell multiplayer server running at ws://localhost:{PORT}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
