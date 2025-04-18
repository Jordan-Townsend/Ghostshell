import asyncio
import websockets
import os
import json

PORT = int(os.environ.get("PORT", 10000))
clients = set()

async def handler(websocket):
    clients.add(websocket)
    print(f"[+] New connection: {websocket.remote_address}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"[{data.get('nickname')}] {data.get('message')}")
            except json.JSONDecodeError:
                print("[!] Received non-JSON message:", message)

            # Broadcast to others
            await asyncio.gather(*[
                client.send(message)
                for client in clients if client != websocket
            ])
    except websockets.exceptions.ConnectionClosed:
        print(f"[-] Disconnected: {websocket.remote_address}")
    finally:
        clients.remove(websocket)

async def main():
    print(f"[~] Starting WebSocket server on port {PORT}...")
    async with websockets.serve(handler, "0.0.0.0", PORT):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Server manually stopped.")
