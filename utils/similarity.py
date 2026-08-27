import numpy as np


# ==========================================================
# COSINE DISTANCE
# ==========================================================

def cosine_distance(
    embedding1,
    embedding2
):

    embedding1 = np.asarray(
        embedding1
    )

    embedding2 = np.asarray(
        embedding2
    )

    norm1 = np.linalg.norm(
        embedding1
    )

    norm2 = np.linalg.norm(
        embedding2
    )

    if norm1 == 0 or norm2 == 0:

        return 1.0

    similarity = np.dot(
        embedding1,
        embedding2
    ) / (norm1 * norm2)

    similarity = np.clip(
        similarity,
        -1,
        1
    )

    return 1 - similarity


# ==========================================================
# FIND BEST MATCH
# ==========================================================

def find_best_match(
    query_embedding,
    registered_embeddings
):

    if not registered_embeddings:

        return None

    best_match = None

    best_distance = float("inf")

    for item in registered_embeddings:

        distance = cosine_distance(
            query_embedding,
            item["embedding"]
        )

        if distance < best_distance:

            best_distance = distance

            best_match = {
                "person_id": item.get("person_id"),
                "name": item.get("name", item.get("person_id", "Unknown")),
                "phone_number": item.get("phone_number"),
                "distance": float(
                    distance
                )
            }

    return best_match