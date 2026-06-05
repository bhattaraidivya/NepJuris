from rag.generator import Generator


class ChatService:
    def __init__(self):
        
        self.generator = Generator()
        self.generator.retriever.load()

    def generate_response(self, message: str):
        return self.generator.generate(message)