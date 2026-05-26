import numpy as np


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    dot = np.dot(a, b)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    return dot / (norm_a * norm_b)


def retrieve_top_chunks(query_embedding, documents, top_k=3):

    results = []

    for doc in documents:

        for chunk in doc["chunks"]:

            score = cosine_similarity(
                query_embedding,
                chunk["embedding"]
            )

            results.append({
                "text": chunk["text"],
                "score": score
            })

    # Sort by highest score
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]