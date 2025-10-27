

For testing:
``` py

import asyncio
import websockets

allowed="localhost"
allowed="0.0.0.0"
port = 4513
async def echo(websocket):
	try:
		async for message in websocket:
			print(f"Received message: {message}")
			await websocket.send(f"Echo: {message}")
	except websockets.exceptions.ConnectionClosed:
		print("Client disconnected")
	except Exception as e:
		print(f"Error: {e}")

async def main():
	server = await websockets.serve(echo, allowed, port)
	print(f"WebSocket server started on ws://{allowed}:{port}")
	await server.wait_closed()

if __name__ == "__main__":
	asyncio.run(main())

```
