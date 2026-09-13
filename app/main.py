import uuid
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.analysis import extract_metadata


app = FastAPI(title="DeepTrace")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = Path("app/static/uploads")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/analyze")
async def analyze_image(request: Request, image: UploadFile = File(...)):
    ext = Path(image.filename).suffix
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / unique_name

    contents = await image.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    metadata = extract_metadata(save_path)

    return templates.TemplateResponse(
        request,
        "result.html",
        {"filename": unique_name, "metadata": metadata}
    )