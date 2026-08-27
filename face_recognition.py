import numpy as np

from utils.face_detector import (
    get_detector
)

from utils.embedding import (
    generate_embedding
)

from utils.similarity import (
    find_best_match
)

from database import (
    get_all_embeddings
)

from config import (
    RECOGNITION_THRESHOLD
)


# ==========================================================
# RECOGNIZE FACE
# ==========================================================

def recognize_face(face):

    # ------------------------------------------------------
    # GENERATE EMBEDDING
    # ------------------------------------------------------

    query_embedding = generate_embedding(
        face
    )

    # ------------------------------------------------------
    # GET REGISTERED EMBEDDINGS
    # ------------------------------------------------------

    registered = get_all_embeddings()

    if not registered:

        return {
            "recognized": False,
            "name": "No registered people",
            "person_id": None,
            "distance": None
        }

    # ------------------------------------------------------
    # FIND MATCH
    # ------------------------------------------------------

    match = find_best_match(
        query_embedding,
        registered
    )

    if match is None:

        return {
            "recognized": False,
            "name": "Unknown Person",
            "person_id": None,
            "distance": None
        }

    # ------------------------------------------------------
    # THRESHOLD
    # ------------------------------------------------------

    if (
        match["distance"]
        < RECOGNITION_THRESHOLD
    ):

        return {
            "recognized": True,
            "name": match["name"],
            "person_id": match["person_id"],
            "distance": match["distance"]
        }

    return {
        "recognized": False,
        "name": "Unknown Person",
        "person_id": None,
        "distance": match["distance"]
    }