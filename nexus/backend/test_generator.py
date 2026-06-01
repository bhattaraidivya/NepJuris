from rag.generator import Generator

gen = Generator()

print("🔥 NyayaAI RAG System Ready")

while True:
    query = input("\nAsk a legal question: ")
    print("\n" + "="*50)
    print(gen.generate(query))
    print("="*50)