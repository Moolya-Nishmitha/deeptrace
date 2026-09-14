import cv2
from pathlib import Path

# OpenCV ships with pretrained Haar Cascade files — no separate download needed.
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def has_face(filepath: Path) -> dict:
    """
    Detects whether the image contains at least one human face.
    Returns whether a face was found and how many.
    """
    img = cv2.imread(str(filepath))
    if img is None:
        return {"face_found": False, "face_count": 0}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(40, 40),
    )

    return {
        "face_found": len(faces) > 0,
        "face_count": len(faces),
    }