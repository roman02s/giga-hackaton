import glob
from pathlib import Path

import langchain
from langchain.cache import RedisSemanticCache
from langchain.chains import RetrievalQA
from langchain.schema.document import Document
from src.utils.llm import GigaChatLLM
from src.utils.pdf2text import extract_text_from_pdf
from src.utils.retriever import create_retriever

gigachat = GigaChatLLM()

langchain.llm_cache = RedisSemanticCache(
    redis_url="redis://localhost:6379",
    embedding=gigachat.embeddings,
    score_threshold=0.01,
)

pdf_paths = glob.glob("data/*.pdf")
for i in range(len(pdf_paths)):
    pdf_paths[i] = str(Path(pdf_paths[i]))

documents_list = []

for path in pdf_paths:
    page_content = extract_text_from_pdf(path)

    documents_list.append(
        Document(page_content=page_content, metadata={"file_name": path.split("/")[-1]})
    )
retriever = create_retriever(documents_list, embeddings=gigachat.embeddings, k=5)

qa = RetrievalQA.from_chain_type(
    llm=gigachat.model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,  # False
)


def get_model():
    return gigachat


def get_answer(query):
    return qa({"query": query})
