import streamlit as st
import os
import tempfile
from PIL import Image

# RAG dependencies (wrapped in try-except so app still runs without them)
RAG_AVAILABLE = False
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.document_loaders import BSHTMLLoader
    from langchain_core.runnables import RunnablePassthrough
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_chroma import Chroma
    RAG_AVAILABLE = True
except ImportError:
    pass

st.set_page_config(
    page_title="Samsung Manual Assistant",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Outfit:wght@500;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
h1, h2, h3 { font-family: 'Outfit', sans-serif; }
.chat-bubble {
    border-radius: 12px; padding: 15px 18px; margin-bottom: 12px;
    max-width: 80%; line-height: 1.5;
}
.user-bubble {
    background-color: #2b3964; color: white; margin-left: auto;
    border-bottom-right-radius: 2px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.assistant-bubble {
    background-color: #1e1e1e; color: #e2e8f0; margin-right: auto;
    border-bottom-left-radius: 2px; border: 1px solid #333;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.system-msg {
    text-align: center; color: #888; font-size: 0.85rem; margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#0057b8 0%,#002f6c 100%);
            padding:35px 30px;border-radius:16px;margin-bottom:28px;
            box-shadow:0 8px 32px rgba(0,0,0,0.35);">
    <h1 style="color:white;margin:0;font-size:2.4rem;">💧 Samsung Washing Machine Assistant</h1>
    <p style="color:#90caf9;margin:8px 0 0;font-size:1.05rem;">
        RAG-powered conversational assistant to query manuals, cycles, maintenance, and error codes
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
st.sidebar.header("⚙️ Configuration")
mode = st.sidebar.selectbox("Choose Mode", ["Demo/Mock Mode (No API Key)", "OpenAI GPT RAG Mode"])

api_key = ""
if mode == "OpenAI GPT RAG Mode":
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your sk- API key")
    if not api_key:
        st.sidebar.warning("🔑 Please enter an OpenAI API Key to run RAG mode.")
    if not RAG_AVAILABLE:
        st.sidebar.error("❌ LangChain/Chroma dependencies are not fully installed. Falling back to Demo Mode.")

st.sidebar.markdown("---")
st.sidebar.header("📄 Document Selection")
uploaded_file = st.sidebar.file_uploader("Upload Samsung HTML Manual", type=["html"])
st.sidebar.caption("If no manual is uploaded, the app uses the built-in `model.html` manual.")

# ─── Manual Loading Helper ───────────────────────────────────────────────────
def get_manual_path():
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
            f.write(uploaded_file.getvalue())
            return f.name
    else:
        # Default model.html
        if os.path.exists("model.html"):
            return "model.html"
        else:
            # Fallback path if run from workspace directory
            # search relative
            possible_paths = ["Project-08-Washing-Machine-Assistant/model.html", "model.html"]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            return None

# ─── Demo Mode Rule Matcher ──────────────────────────────────────────────────
def run_mock_qa(question):
    q = question.lower()
    if "4c" in q or "4e" in q or "water supply" in q:
        return ("🛠️ **Error Code 4C/4E: Water Supply Error**\n\n"
                "This indicates a water supply problem. Try these steps:\n"
                "1. Ensure the water inlet taps are fully open.\n"
                "2. Check that the hose connections are secure and not kinked/twisted.\n"
                "3. Clean the mesh filters inside the inlet valves.")
    elif "5c" in q or "5e" in q or "drain" in q:
        return ("🛠️ **Error Code 5C/5E: Drainage Error**\n\n"
                "This indicates the machine is not draining properly. Try these steps:\n"
                "1. Inspect the drain filter at the bottom right front of the washing machine for blockages.\n"
                "2. Clear out any debris, buttons, or lint.\n"
                "3. Check the drain hose to ensure it is not clogged or bent.")
    elif "ub" in q or "ue" in q or "unbalanced" in q:
        return ("🛠️ **Error Code Ub/UE: Unbalanced Load Error**\n\n"
                "This means the laundry load is distributed unevenly inside the tub:\n"
                "1. Pause the cycle.\n"
                "2. Rearrange the clothing items to distribute their weight evenly.\n"
                "3. Close the door and press Start to resume the spin cycle.")
    elif "delicate" in q:
        return ("🧺 **Delicates Cycle details:**\n\n"
                "Perfect for sheer fabrics, lace, lingerie, silks, and hand-wash-only clothes. "
                "This cycle uses cold water, slow spin speed, and gentle agitation to keep your garments safe.")
    elif "clean" in q or "maintenance" in q or "tub" in q:
        return ("✨ **Self Clean / Tub Clean Mode:**\n\n"
                "Recommended to run once a month. Use this cycle with an empty drum and no detergent to clean the tub and remove mold/bacterial residues.")
    else:
        return ("🤖 **Demo Mode Answer:**\n\n"
                "I found matching information in the Samsung Manual regarding wash cycles and troubleshooting. "
                "To get exact AI-generated RAG answers, please configure the OpenAI API key in the sidebar.\n\n"
                "**Quick Summary of the manual:**\n"
                "- Cycles: Normal (6.0kg load), Delicates (gentle spin), Quick Wash (15 mins, 2.0kg load).\n"
                "- Errors: 4C (Water inlet), 5C (Drainage filter), Ub (Unbalanced spin load).")

# ─── Chat Interface State ────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Samsung Washing Machine Assistant. Ask me anything about modes, error codes, or maintenance."}
    ]

# Display Chat History
for msg in st.session_state.messages:
    bubble_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    st.markdown(f"""
    <div class="chat-bubble {bubble_class}">
        {msg['content']}
    </div>
    """, unsafe_allow_html=True)

# User query input
user_query = st.chat_input("Ask a question (e.g. 'How do I fix error code 5C?')")

if user_query:
    # Append user question
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.markdown(f"""<div class="chat-bubble user-bubble">{user_query}</div>""", unsafe_allow_html=True)
    
    with st.spinner("Analyzing manual…"):
        manual_path = get_manual_path()
        
        if mode == "OpenAI GPT RAG Mode" and api_key and RAG_AVAILABLE and manual_path:
            try:
                # Set API key environment variable
                os.environ["OPENAI_API_KEY"] = api_key
                
                # Setup LangChain pipeline
                loader = BSHTMLLoader(file_path=manual_path)
                docs = loader.load()
                
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                splits = text_splitter.split_documents(docs)
                
                vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
                retriever = vectorstore.as_retriever()
                
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
                
                prompt = ChatPromptTemplate.from_template(
                    "You are a helpful Samsung Washing Machine assistant.\n"
                    "Use the retrieved manual context below to answer the question. If you don't know, say you don't know.\n\n"
                    "Context:\n{context}\n\n"
                    "Question: {question}"
                )
                
                def format_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)
                
                rag_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                )
                
                ans = rag_chain.invoke(user_query).content
            except Exception as e:
                ans = f"⚠️ RAG Pipeline Error: {e}. Falling back to demo response.\n\n" + run_mock_qa(user_query)
        else:
            ans = run_mock_qa(user_query)
            
    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": ans})
    st.markdown(f"""<div class="chat-bubble assistant-bubble">{ans}</div>""", unsafe_allow_html=True)

st.caption("Project 08 — Samsung Washing Machine RAG Assistant • AI/ML Summer Internship")
