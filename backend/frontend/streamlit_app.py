import uuid
import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Gemini Multimodal Chatbot", layout="wide")

st.title("Gemini Multimodal Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Session")
    st.code(st.session_state.session_id)

    st.subheader("Upload")
    uploads = st.file_uploader(
        "Upload PDF / text / images",
        type=["pdf", "txt", "md", "png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
    )

    if st.button("Ingest files", disabled=not uploads):
        files_payload = []
        for uf in uploads:
            files_payload.append(("files", (uf.name, uf.getvalue(), uf.type)))

        resp = requests.post(
            f"{API_BASE}/ingest",
            data={"session_id": st.session_state.session_id},
            files=files_payload,
            timeout=120,
        )
        if resp.ok:
            st.success(f"Ingested. Added chunks: {resp.json().get('documents_added')}")
        else:
            st.error(resp.text)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("Citations"):
                for c in msg["citations"]:
                    st.write(f"- {c.get('source')} | page={c.get('page')}")
                    st.caption(c.get("snippet", ""))

user_text = st.chat_input("Ask a question about your uploaded files...")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    resp = requests.post(
        f"{API_BASE}/chat",
        json={"session_id": st.session_state.session_id, "message": user_text},
        timeout=120,
    )

    if resp.ok:
        data = resp.json()
        answer = data["answer"]
        citations = data.get("citations", [])
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "citations": citations}
        )
        with st.chat_message("assistant"):
            st.markdown(answer)
            if citations:
                with st.expander("Citations"):
                    for c in citations:
                        st.write(f"- {c.get('source')} | page={c.get('page')}")
                        st.caption(c.get("snippet", ""))
    else:
        st.error(resp.text)
