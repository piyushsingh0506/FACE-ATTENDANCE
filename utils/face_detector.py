import numpy as np
import torch

from PIL import Image

from facenet_pytorch import MTCNN


# ==========================================================
# DEVICE
# ==========================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ==========================================================
# MTCNN
# ==========================================================

_mtcnn = None


def get_detector():

    global _mtcnn

    if _mtcnn is None:

        _mtcnn = MTCNN(
            image_size=160,
            margin=20,
            min_face_size=40,
            thresholds=[0.6, 0.7, 0.7],
            factor=0.709,
            post_process=True,
            keep_all=True,
            device=DEVICE
        )

    return _mtcnn


# ==========================================================
# DETECT FACES
# ==========================================================

def detect_faces(image):

    detector = get_detector()

    if isinstance(image, np.ndarray):

        image = Image.fromarray(image)

    boxes, probabilities = detector.detect(
        image
    )

    return boxes, probabilities


# ==========================================================
# EXTRACT FACE
# ==========================================================

def extract_face(image):

    detector = get_detector()

    if isinstance(image, np.ndarray):

        image = Image.fromarray(image)

    faces = detector(
        image
    )

    if faces is None:

        return None

    if faces.ndim == 3:

        faces = faces.unsqueeze(0)

    return faces