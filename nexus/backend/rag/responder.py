def generate_response(user_query, retrieved_text, score):

    if score < 0.35:
        return (
            "I could not find enough relevant legal information "
            "for your query. Please ask a more specific legal question."
        )

    response = f"""
Legal Information:

{retrieved_text}

Relevance Score: {round(score, 2)}
"""

    return response