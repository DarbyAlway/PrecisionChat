from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from models.SAR import MusashinoAssistant_SAR
from models.RAG import MusashinoAssistant_RAG
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import time
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI Assistants
assistant_SAR = MusashinoAssistant_SAR()
assistant_RAG = MusashinoAssistant_RAG()

# Mount the frontend folder to serve CSS and JS
# Ensure your folder is named 'frontend'
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class SearchRequest(BaseModel):
    query: str

# --- Route to show the HTML page ---
@app.get("/")
async def read_index():
    return FileResponse('frontend/index.html')

@app.post("/search")
async def search(request: SearchRequest):
    try:
        # 1. Start the timer
        start_time = time.perf_counter()
        
        user_query = request.query
        loop = asyncio.get_event_loop()

        # 2. Kick off concurrent tasks
        sar_task = loop.run_in_executor(None, assistant_SAR.get_answer, user_query)
        rag_task = loop.run_in_executor(None, assistant_RAG.get_answer, user_query)

        # 3. Wait for both to finish
        answer_SAR, answer_RAG = await asyncio.gather(sar_task, rag_task)

        # 4. Calculate total duration
        end_time = time.perf_counter()
        duration = end_time - start_time
        print('response time:', duration)
        
        return {
            "status": "success",
            "query": user_query,
            "answer_SAR": answer_SAR,
            "answer_RAG": answer_RAG
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)