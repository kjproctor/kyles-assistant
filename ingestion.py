# from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from consts import INDEX_NAME


def ingest_docs(path: str) -> None:
    loader = PyPDFLoader(file_path=path)
    raw_documents = loader.load()
    # loader = ReadTheDocsLoader(path="docs/")
    # raw_documents = loader.load()
    print(f"loaded {len(raw_documents) }documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Split into {len(documents)} chunks")

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(INDEX_NAME)

    # new_vectorstore = FAISS.load_local(INDEX_NAME, embeddings)
    print("****** Added to FAISS vectorstore vectors")


if __name__ == "__main__":
     #ingest_docs("docs/resume.pdf")
     ingest_docs("docs/resume4.pdf")
