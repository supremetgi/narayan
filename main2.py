from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi import Request
import asyncio

app = FastAPI()

# Store the dummy data and active WebSocket clients
dummy_data: List[List[int]] = []
active_clients: List[WebSocket] = []

# Template directory for HTML responses
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get(request: Request):
    """
    Simple homepage with a link to the WebSocket data table.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/data")
async def get_data():
    """
    Endpoint to view the dummy data as an HTML table.
    """
    # Create an HTML table from dummy_data
    table_html = "<table border='1'><tr><th>Column 1</th><th>Column 2</th><th>Column 3</th><th>Column 4</th><th>Column 5</th><th>Column 6</th><th>Column 7</th><th>Column 8</th><th>Column 9</th><th>Column 10</th><th>Column 11</th><th>Column 12</th><th>Column 13</th><th>Column 14</th><th>Column 15</th><th>Column 16</th></tr>"
    
    for row in dummy_data:
        table_html += "<tr>" + "".join([f"<td>{col}</td>" for col in row]) + "</tr>"
    
    table_html += "</table>"
    
    return HTMLResponse(content=table_html, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_clients.append(websocket)
    try:
        while True:
            # Receive data from client (dummy data)
            data = await websocket.receive_text()
            print(f"Received data: {data}")
            
            # Parse and store the data in a table (16 columns)
            columns = list(map(int, data.split(',')))
            if len(columns) == 16:
                dummy_data.append(columns)
            else:
                print("Invalid data format, expecting 16 columns.")
                
            # Broadcast the new data to all connected clients
            for client in active_clients:
                await client.send_text(f"new_data:{','.join(map(str, columns))}")
                
            # Optionally, you can print the dummy data to monitor its state
            print("no more dummy data")

    except WebSocketDisconnect:
        active_clients.remove(websocket)
        print("Client disconnected")
