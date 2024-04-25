from typing import List

from langchain.embeddings.base import Embeddings
from langchain.retrievers import ParentDocumentRetriever
from langchain.schema.document import Document
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma


def create_retriever(
    docs: List[Document],
    embeddings: Embeddings,
    retriever_name: str = "retriever",
    k: int = 20,
    child_chunk_size: int = 250,
    parent_chunk_size: int = 1000,
    use_parent_splitter: bool = True,
) -> ParentDocumentRetriever:
    """
    Creates embedding retriever from provided docs. Uses RecursiveCharacterTextSplitter and ParentDocumentRetriever for better performance.

    :param List[Document] docs: A list of documents to embed
    :param str retriever_name: Name of retriever
    :param int k: Number of child chunks to retrieve
    :param int child_chunk_size: the maximum size of child chunks (as measured by the length function)
    :param int parent_chunk_size: the maximum size of parent chunks (as measured by the length function)
    :returns: List with information from jmix forum
    """

    if use_parent_splitter:
        parent_splitter = RecursiveCharacterTextSplitter(chunk_size=parent_chunk_size)
    else:
        parent_splitter = None

    child_splitter = RecursiveCharacterTextSplitter(chunk_size=child_chunk_size)
    vectorstore = Chroma(collection_name=retriever_name, embedding_function=embeddings)
    store = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        search_kwargs={"k": k},
    )

    retriever.add_documents(docs)
    return retriever
