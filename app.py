import os
import joblib
import streamlit as st

from dotenv import load_dotenv
from google import genai

from vector_store import search
from prompts import SYSTEM_PROMPT

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_GEN_MODEL")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found.")
    st.stop()

@st.cache_resource
def load_client():
    return genai.Client(api_key=api_key)

client = load_client()

@st.cache_resource
def load_vector_db():
    return joblib.load("vector_store.pkl")

vector_db = load_vector_db()

st.set_page_config(
    page_title="Mediora AI",
    page_icon="🩺",
    layout="wide"
)
st.markdown("""
<style>

.main{
    background-color:#f5f9fc;
}

h1{
    color:#0B6E99;
    text-align:center;
}

.block-container{
    padding-top:2rem;
}

div[data-testid="stSidebar"]{
    background:#0B6E99;
}

div[data-testid="stSidebar"] *{
    color:white;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
    margin-bottom:10px;
    box-shadow:0 2px 10px rgba(0,0,0,.08);
}

.stButton>button{
    width:100%;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)
with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/stethoscope.png",
        width=80
    )

    st.title("Mediora AI")

   

    st.markdown("---")

    st.subheader("📚 Medical Topics")

    st.write("🩸 Diabetes")

    st.write("🦟 Dengue")

    st.write("❤️ Hypertension")

    st.write("🫁 Asthma")

    st.write("🩹 First Aid")

    st.write("🥗 Nutrition")

    st.markdown("---")

    st.subheader("Example Questions")

    st.write("• What is Dengue?")

    st.write("• Symptoms of Diabetes")

    st.write("• First aid for burns")

    st.write("• How to prevent hypertension?")

    st.markdown("---")

    st.info("This assistant provides educational information only. "
    "Always consult a qualified healthcare professional for diagnosis, treatment, or medical emergencies.")
    if st.button("🗑 Clear Chat"):
      st.session_state.messages = []
      st.session_state.pop("example_question", None)
      st.rerun()
st.markdown("""
<h1>🩺 Mediora AI</h1>

<h4 style="text-align:center;color:gray;">
Your Intelligent Medical Assistant
</h4>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.messages) == 0:

    st.info(
        "👋 Welcome! Ask any health-related question. "
        "Or click one of the examples below."
    )

    st.markdown("### 💬 Try these questions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🦟 What is dengue?"):
            st.session_state.example_question = "What is dengue?"
            st.rerun()

        if st.button("🩸 What are the symptoms of diabetes?"):
            st.session_state.example_question = "What are the symptoms of diabetes?"
            st.rerun()

    with col2:
        if st.button("❤️ How to prevent hypertension?"):
            st.session_state.example_question = "How to prevent hypertension?"
            st.rerun()

        if st.button("🩹 What should I do for burns?"):
            st.session_state.example_question = "What should I do for burns?"
            st.rerun()

question = st.chat_input("Ask your medical question...")

if "example_question" in st.session_state:
    question = st.session_state.pop("example_question")


if question and question.strip():

    st.session_state.messages.append(
        {"role":"user","content":question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    SIMILARITY_THRESHOLD = 0.45

    results = search(question, vector_db, top_k=3)

    if not results or results[0][0] < SIMILARITY_THRESHOLD:
       st.warning("This topic is not available in the medical knowledge base.")
       st.stop()

    context = ""

    for score, text in results:
       if score >= SIMILARITY_THRESHOLD:
          context += text + "\n\n"

    prompt = SYSTEM_PROMPT.format(
      context=context,
      question=question
   )

    with st.chat_message("assistant"):

      with st.spinner("🔍 Analyzing your medical question..."):

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            answer = response.text if response.text else "No response received from Gemini."

            st.markdown(answer)

        except Exception as e:
            print("Gemini Error:", e)
            if "503" in str(e):

              answer = "⚠️ AI is currently busy. Here is the information from Mediora AI's medical knowledge base."

              st.warning(answer)

              final_answer = ""

              for score, text in results:
                if score >= SIMILARITY_THRESHOLD:
                  final_answer += text + "\n\n"

              st.markdown(final_answer)

              answer = final_answer

            elif "429" in str(e):

              answer = "⚠️ Free AI quota has been reached. Showing information from the medical knowledge base."

              st.warning(answer)

              final_answer = ""

              for score, text in results:
                if score >= SIMILARITY_THRESHOLD:
                  final_answer += text + "\n\n"

              st.markdown(final_answer)

              answer = final_answer

            elif "ConnectError" in str(e):

                answer = "⚠️ Unable to connect to Gemini. Please check your internet connection."

                st.warning(answer)

            else:

                print(e)

                answer = "⚠️ Something went wrong. Please try again."

                st.error(answer)
        st.session_state.messages.append(
           {
            "role": "assistant",
             "content": answer
            }
       )
st.markdown("---")

st.caption( 
        "This application is for educational purposes only and should not replace professional medical advice."
        )