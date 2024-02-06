from typing import Any, List, Dict

from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.load_local(
        "/Users/kproctor/Documents/learning/udemy/LangChain/kyles-assistant/langchain-doc-index/",
        embeddings,
    )

    chat = ChatOpenAI(verbose=True, temperature=0)

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )

    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    pass
