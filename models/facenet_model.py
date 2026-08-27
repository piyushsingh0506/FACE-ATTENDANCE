import torch

from facenet_pytorch import InceptionResnetV1


# ==========================================================
# LOAD DEVICE
# ==========================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# ==========================================================
# LOAD FACENET
# ==========================================================

_model = None


def get_facenet_model():

    global _model

    if _model is None:

        _model = InceptionResnetV1(
            pretrained="vggface2"
        ).eval().to(DEVICE)

    return _model


# ==========================================================
# GET DEVICE
# ==========================================================

def get_device():

    return DEVICE