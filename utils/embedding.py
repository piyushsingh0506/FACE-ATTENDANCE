import numpy as np
import torch

from PIL import Image

from models.facenet_model import (
    get_facenet_model,
    get_device
)


# ==========================================================
# IMAGE TO EMBEDDING
# ==========================================================

def generate_embedding(face):

    model = get_facenet_model()

    device = get_device()

    # ------------------------------------------------------
    # PIL IMAGE
    # ------------------------------------------------------

    if isinstance(face, Image.Image):

        face = face.convert("RGB")

        face = np.array(face)

        face = torch.tensor(
            face
        ).permute(2, 0, 1).float()

        face = face / 255.0

    # ------------------------------------------------------
    # NUMPY IMAGE
    # ------------------------------------------------------

    elif isinstance(face, np.ndarray):

        face = Image.fromarray(face)

        face = np.array(face)

        face = torch.tensor(
            face
        ).permute(2, 0, 1).float()

        face = face / 255.0

    # ------------------------------------------------------
    # TORCH TENSOR
    # ------------------------------------------------------

    elif not isinstance(face, torch.Tensor):

        raise ValueError(
            "Unsupported face format"
        )

    if face.ndim == 3:

        face = face.unsqueeze(0)

    face = face.to(device)

    # ------------------------------------------------------
    # MODEL
    # ------------------------------------------------------

    with torch.no_grad():

        embedding = model(
            face
        )

    # ------------------------------------------------------
    # NORMALIZE
    # ------------------------------------------------------

    embedding = embedding.cpu().numpy()[0]

    norm = np.linalg.norm(
        embedding
    )

    if norm != 0:

        embedding = embedding / norm

    return embedding