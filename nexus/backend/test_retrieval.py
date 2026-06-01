from rag.retriever import Retriever

retriever = Retriever()

query = "Can government restrict freedom of speech?"

results = retriever.retrieve(query)

print("\nTOP RESULTS:\n")

for i, r in enumerate(results):
    print(f"\n--- RESULT {i+1} ---")
    print(r["text"][:300])