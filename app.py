import os
import uuid
import aiofiles
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import model as ml_model
import history as hist_module

app = FastAPI(title="智能图像识别工具")

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

def get_user_id(request: Request) -> str:
    user_id = request.headers.get("x-user-id")
    if not user_id:
        user_id = str(uuid.uuid4())
    return user_id

@app.get("/", response_class=HTMLResponse)
async def index():
    template_path = Path(__file__).parent / "templates" / "index.html"
    return template_path.read_text()

@app.get("/api/history")
async def get_history(request: Request):
    user_id = get_user_id(request)
    records = hist_module.get_history(user_id)
    return {"records": records}

@app.post("/api/classify")
async def classify(request: Request, file: UploadFile = File(...)):
    user_id = get_user_id(request)

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = UPLOAD_DIR / unique_name

    try:
        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        results = ml_model.classify_image(str(file_path))

        top_results = results[:5]

        record = hist_module.add_record(user_id, file.filename, top_results)

        return {
            "success": True,
            "results": top_results,
            "record_id": record["id"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if file_path.exists():
            file_path.unlink()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
