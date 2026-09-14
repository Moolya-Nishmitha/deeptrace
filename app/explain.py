def generate_explanation(detection: dict, metadata: dict, face_count: int) -> str:
    """
    Builds a plain-language paragraph from the signals we already computed.
    IMPORTANT: this is NOT the model explaining its own internal reasoning
    (that would require techniques like Grad-CAM). This is us being
    transparent about the supporting context around the verdict.
    """
    label = detection["label"]
    confidence = detection["confidence"]

    # Frame confidence in plain language instead of a bare number
    if confidence >= 85:
        strength = "strong"
    elif confidence >= 65:
        strength = "moderate"
    else:
        strength = "weak"

    parts = []

    if label == "Deepfake":
        parts.append(
            f"The model found a {strength} signal ({confidence}%) that this image "
            f"may be AI-generated or manipulated."
        )
    else:
        parts.append(
            f"The model found a {strength} signal ({confidence}%) that this image "
            f"is likely a real, unmanipulated photo."
        )

    if face_count > 1:
        parts.append(
            f"Note: {face_count} faces were detected in this image. The model's "
            f"training focused on single-face images, so results may be less "
            f"reliable here."
        )

    if not metadata["exif_found"]:
        parts.append(
            "No camera metadata (EXIF) was found in this file. This is common in "
            "screenshots, downloaded images, or images re-saved through social media "
            "or messaging apps — it does not by itself prove manipulation, but it "
            "does mean we can't verify the image's original source device."
        )
    else:
        parts.append(
            "Camera metadata (EXIF) was present, which is more typical of an "
            "unedited photo straight from a camera or phone."
        )

    if strength == "weak":
        parts.append(
            "Because the model's confidence here is low, treat this result as "
            "inconclusive rather than a reliable verdict."
        )

    return " ".join(parts)