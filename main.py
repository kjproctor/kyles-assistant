import uuid

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from itertools import zip_longest


st.set_page_config(layout="wide", page_title="Kyle's - Assistant", initial_sidebar_state="collapsed")
st.header("Kyle's - Assistant")
st.image("https://cdn.midjourney.com/9134fa71-ac7f-46d4-abe1-23b3034921b7/0_1.webp", width=300)
prompt = st.text_input("Prompt", placeholder="Who is Kyle?....What are Kyle's skills?... Can Kyle build an automated system infused with AI?... How do I contact Kyle?... Ask me anything...")
with open("docs/resume.pdf", "rb") as pdf_file:
    st.download_button(
        label="Download Resume",
        data=pdf_file.read(),
        file_name="resume.pdf",
        mime="application/pdf",
    )

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['answer']} \n"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append((prompt, generated_response["answer"]))

if st.session_state["chat_answers_history"]:
    # Reverse both lists simultaneously using zip_longest and reversed
    for generated_response, user_query in zip_longest(
        reversed(st.session_state["chat_answers_history"]),
        reversed(st.session_state["user_prompt_history"]),
        fillvalue="",
    ):
        # Display messages as before
        message(user_query, is_user=True, key=str(uuid.uuid4()))
        message(generated_response, key=str(uuid.uuid4()))
