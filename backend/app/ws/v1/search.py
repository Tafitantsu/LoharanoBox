from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.search_service import SearchService
import json

ws_router = APIRouter()

@ws_router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    db: Session = SessionLocal()
    search_service = SearchService(db)

    try:
        while True:
            search_term = await websocket.receive_text()
            if not search_term:
                continue

            # 1. Send initial FTS results for a quick response
            fts_results = search_service.search_full_text_only(search_term, limit=10)
            await websocket.send_text(json.dumps({
                "type": "fts_results",
                "data": fts_results
            }))

            # 2. Perform the more intensive hybrid search and send the final results
            hybrid_results = search_service.search_hybrid(search_term)
            await websocket.send_text(json.dumps({
                "type": "hybrid_results",
                "data": hybrid_results[:10] # Limit to 10 for consistency
            }))

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        await websocket.close(code=1011)
    finally:
        db.close()
        print("Database session closed")