import os

from dotenv import load_dotenv
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.embeddings import GigaChatEmbeddings

load_dotenv()


class GigaChatLLM:
    def __init__(self) -> None:
        self._model = GigaChat(
            credentials=os.getenv("GIGACHAT_API_TOKEN"),
            verify_ssl_certs=False,
            scope="GIGACHAT_API_CORP",
            model="GigaChat-Pro",
        )
        self._embeddings = GigaChatEmbeddings(
            credentials=os.getenv("GIGACHAT_API_TOKEN"),
            verify_ssl_certs=False,
            scope="GIGACHAT_API_CORP",
            model="Embeddings",
        )

    @property
    def model(self):
        return self._model

    @property
    def name(self):
        return "gigachat"

    @property
    def embeddings(self):
        return self._model

    def call(self, query, instructions, context, previous_questions):
        messages = [
            SystemMessage(
                content="You are a chemistry expert. Please answer the questions as accurately as possible, based on the information in the article. If you don't have an answer for a question, please say 'I don't know.'"
            ),
            SystemMessage(
                content="\n".join(
                    [
                        "The article is based on the following information:",
                        f"Instruction: {instructions}" if instructions else "",
                        f"Maximal relevant context: {context}" if context else "",
                        f"Previous questions: {previous_questions}"
                        if previous_questions
                        else "",
                    ]
                )
            ),
        ]
        messages.append(HumanMessage(content="Question: " + query))
        res = self.model(messages)
        return res.content


if __name__ == "__main__":
    """Пример работы с чатом через gigachain"""
    messages = [
        SystemMessage(
            content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
        )
    ]
    gigachat = GigaChatLLM()
    user_input = "Столица Германии"
    messages.append(HumanMessage(content=user_input))
    res = gigachat.model(messages)
    messages.append(res)
    print("Bot: ", res.content)
