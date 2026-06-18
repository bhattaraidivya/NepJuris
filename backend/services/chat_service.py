from rag.retriever import Retriever
from rag.generator import Generator


class ChatService:
    def __init__(self):
        self.retriever = Retriever()
        self.retriever.load()

        self.generator = Generator()

    def generate_response(self, message: str):

        # 1. retrieve context
        contexts = self.retriever.retrieve(message)

        # 2. generate answer using context
        response = self.generator.generate(
            message,
            contexts
        )

        return response