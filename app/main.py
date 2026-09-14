import uuid
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from app.support_content import SUPPORT_CONTENT


from app.analysis import extract_metadata
from app.detector import detect_deepfake
from app.face_check import has_face
from app.explain import generate_explanation

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
    face_result = has_face(save_path)

    detection = None
    explanation = None

    if face_result["face_found"]:
        detection = detect_deepfake(save_path)
        explanation = generate_explanation(detection, metadata, face_result["face_count"])

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "filename": unique_name,
            "metadata": metadata,
            "detection": detection,
            "explanation": explanation,
            "face_result": face_result,
        }
    )
@app.get("/support")
def support_page(request: Request):
    return templates.TemplateResponse(request, "support.html", {})


@app.get("/support-content/{path_key}")
def support_content(path_key: str, known: bool = False):
    if path_key not in ("urgent", "contained"):
        return JSONResponse({"error": "invalid path"}, status_code=400)

    data = dict(SUPPORT_CONTENT[path_key])  # copy so we don't mutate the original

    if known:
        data["addendum"] = SUPPORT_CONTENT["known_perpetrator_addendum"]

    return JSONResponse(data)