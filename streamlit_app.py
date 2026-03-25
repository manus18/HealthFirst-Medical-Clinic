try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
import asyncio
import uuid
from langchain_core.messages import AIMessage, HumanMessage
from graph.workflow import build_workflow, build_faq_only_workflow
import os

# Set page config
st.set_page_config(page_title="HealthFirst Medical Clinic MAS", page_icon="🏥", layout="wide")

def _extract_text(messages) -> str:
    """Extract text from the last AI message, handling Bedrock's list content format."""
    for msg in reversed(messages):
        if not isinstance(msg, AIMessage):
            continue
        content = msg.content
        if isinstance(content, str) and content.strip():
            return content
        if isinstance(content, list):
            parts = [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if parts:
                return "\n".join(parts)
    return "I'm sorry, I couldn't generate a response. Please try again."

async def init_graph(mode):
    if mode == "Full System":
        try:
            graph, _ = await build_workflow()
            return graph
        except Exception as e:
            st.error(f"Failed to initialize full system: {e}")
            st.info("Falling back to FAQ-only mode...")
            return build_faq_only_workflow()
    else:
        return build_faq_only_workflow()

# Sidebar configuration
st.sidebar.title("🏥 Clinic Assistant Settings")
mode = st.sidebar.selectbox("System Mode", ["FAQ Only", "Full System"])
user_id = st.sidebar.text_input("User ID", value="demo_user")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())[:8]
    st.rerun()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "graph" not in st.session_state or st.session_state.get("current_mode") != mode:
    with st.spinner("Initializing system..."):
        st.session_state.graph = asyncio.run(init_graph(mode))
        st.session_state.current_mode = mode

# Main UI
st.title("🏥 HealthFirst Medical Clinic")

# Check if Chroma DB exists
if not os.path.exists("./chroma_langchain_db"):
    st.warning("⚠️ Chroma database not found locally. If this is running on Streamlit Cloud, ensure you have ingested data or provided the persistence directory. You can run `python rag/ingest.py` to initialize it.")

st.markdown(f"**Current Session:** User: `{user_id}` | Thread: `{st.session_state.thread_id}` | Mode: `{mode}`")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = {
                "configurable": {
                    "thread_id": st.session_state.thread_id,
                    "user_id": user_id
                }
            }
            
            # Run the graph
            try:
                if mode == "Full System":
                    result = asyncio.run(st.session_state.graph.ainvoke(
                        {"messages": [("user", prompt)]}, config
                    ))
                else:
                    result = st.session_state.graph.invoke(
                        {"messages": [("user", prompt)]}, config
                    )
                
                response_text = _extract_text(result["messages"])
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error processing request: {e}")
