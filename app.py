import os
import joblib
import streamlit as st

from dotenv import load_dotenv
from google import genai

from vector_store import search
from prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
model = os.getenv("GEMINI_GEN_MODEL")

vector_db = joblib.load("vector_store.pkl")

st.set_page_config(
    page_title="Mediora AI",
    page_icon="🩺",
    layout="wide"
)


# ---------------- Topic -> Suggested Questions ---------------- #

TOPIC_QUESTIONS = {
    "🩸 Diabetes": [
        "What are the symptoms of diabetes?",
        "How can I manage blood sugar levels?",
        "What foods should diabetics avoid?",
        "What is the difference between Type 1 and Type 2 diabetes?",
    ],
    "🦟 Dengue": [
        "What is Dengue?",
        "What are the early symptoms of Dengue?",
        "How is Dengue transmitted?",
        "How can I prevent Dengue at home?",
    ],
    "❤️ Hypertension": [
        "How to prevent hypertension?",
        "What are the symptoms of high blood pressure?",
        "What lifestyle changes help lower blood pressure?",
        "What foods should I avoid for hypertension?",
    ],
    "🫁 Asthma": [
        "What triggers an asthma attack?",
        "What are the symptoms of asthma?",
        "How is asthma managed day to day?",
        "What should I do during an asthma attack?",
    ],
    "🩹 First Aid": [
        "What should I do for burns?",
        "How do I treat a minor cut at home?",
        "What is the first aid for a sprained ankle?",
        "How do I help someone who is choking?",
    ],
    "🥗 Nutrition": [
        "What does a balanced diet look like?",
        "How much water should I drink daily?",
        "What are good sources of protein?",
        "How can I eat healthier on a budget?",
    ],
    "👂 ENT": [
        "What causes a sore throat?",
        "How do I treat an ear infection?",
        "What causes frequent nosebleeds?",
        "When should I see an ENT specialist?",
    ],
    "🧑‍⚕️ Dermatology": [
        "What causes acne?",
        "How can I treat dry skin?",
        "What are common signs of a skin infection?",
        "How do I protect my skin from sun damage?",
    ],
    "👶 Pediatrics": [
        "What is a normal fever in children?",
        "What vaccines does my child need?",
        "How much sleep does a toddler need?",
        "What are signs of dehydration in kids?",
    ],
    "🩺 General Medicine": [
        "What causes frequent headaches?",
        "How do I know if I have the flu or a cold?",
        "What are signs I should see a doctor?",
        "How can I boost my immune system?",
    ],
    "❤️ Cardiology": [
        "What are the warning signs of a heart attack?",
        "How can I keep my heart healthy?",
        "What causes high cholesterol?",
        "What is a normal heart rate?",
    ],
    "🤰 Obstetrics & Gynecology": [
        "What should I expect during pregnancy?",
        "What are common causes of irregular periods?",
        "What prenatal vitamins are recommended?",
        "What are signs of a healthy pregnancy?",
    ],

    "🧠 Neurology": [
        "What are the early signs of a stroke?",
        "What causes frequent migraines and how are they treated?",
        "What are the symptoms of Parkinson's disease?",
        "How can epilepsy be diagnosed and managed?",
    ],

    "🦴 Orthopedics": [
        "What are the most common sports injuries?",
        "How do I treat a broken bone?",
        "What causes back pain and how can it be managed?",
        "How can I prevent osteoporosis?",
    ],

    
    "💊 Pharmacology ": [
        "What are the side effects of Paracetamol?",
        "How do antibiotics work?",
        "How do vaccines stimulate immunity?",
        "Which drugs are used for hypertension?",
    ],


"🧬 Pathology": [
    "What is inflammation and what are its types?",
    "What is the difference between benign and malignant tumors?",
    "What causes anemia and how is it classified?",
    "What is necrosis and how does it differ from apoptosis?",
],

}

GENERAL_EXAMPLE_QUESTIONS = [
    "What is dengue?",
    "What are the symptoms of diabetes?",
    "How to prevent hypertension?",
    "What should I do for burns?",
]

TITLE_WORD_LIMIT = 4  # how many words to keep in an auto-generated chat title


def make_chat_title(question: str, topic_name: str | None = None) -> str:
    """Build a short, clean sidebar title instead of dumping the raw question."""
    if topic_name:
        return topic_name
    words = question.strip().split()
    short = " ".join(words[:TITLE_WORD_LIMIT])
    if len(words) > TITLE_WORD_LIMIT:
        short += "…"
    return short


def new_chat_dict():
    return {
        "title": "New Chat",
        "messages": [],
        "show_welcome": True,  # per-chat flag: welcome/topics view vs conversation view
    }


# ---------------- Session State ---------------- #

if "chats" not in st.session_state:
    st.session_state.chats = {1: new_chat_dict()}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = 1

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "pending_topic_title" not in st.session_state:
    st.session_state.pending_topic_title = None


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
        width=120
    )

    st.title("Mediora AI")

    st.success("System Ready")

    st.markdown("---")

    # ===============================
    # ChatGPT Style Chats
    # ===============================

    if st.button("➕ New Chat", use_container_width=True):
        new_id = max(st.session_state.chats.keys()) + 1
        st.session_state.chats[new_id] = new_chat_dict()
        st.session_state.current_chat = new_id
        st.session_state.selected_topic = None
        st.rerun()

    st.markdown("### 💬 Chats")

    # scrollable container so a long chat history doesn't push the sidebar off-screen
    chat_list = st.container(height=320)

    with chat_list:
        # iterate over a static list of items so we can safely delete during the loop
        for chat_id, chat in list(st.session_state.chats.items()):

            col1, col2 = st.columns([5, 1])

            with col1:
                if st.button(
                    f"💬 {chat['title']}",
                    key=f"chat_{chat_id}",
                    use_container_width=True
                ):
                    st.session_state.current_chat = chat_id
                    st.session_state.selected_topic = None
                    st.rerun()

            with col2:
                if len(st.session_state.chats) > 1:
                    if st.button("🗑", key=f"delete_{chat_id}"):
                        del st.session_state.chats[chat_id]
                        if st.session_state.current_chat == chat_id:
                            st.session_state.current_chat = list(
                                st.session_state.chats.keys()
                            )[0]
                        st.rerun()

            st.markdown("---")

    st.info("Educational Purposes Only")


st.markdown("""
<h1>🩺 Mediora AI</h1>

<h4 style="text-align:center;color:gray;">
Your Intelligent Medical Assistant
</h4>
""", unsafe_allow_html=True)

current_chat_id = st.session_state.current_chat
current_chat_data = st.session_state.chats[current_chat_id]
current_messages = current_chat_data["messages"]

show_welcome = (not current_messages) or current_chat_data.get("show_welcome", False)

# ===============================
# Welcome screen (topics + example questions)
# ===============================
if show_welcome:

    # if there's an ongoing conversation, offer a way back into it
    if current_messages:
        if st.button("💬 Back to Conversation"):
            current_chat_data["show_welcome"] = False
            st.rerun()
        st.markdown("---")

    if st.session_state.selected_topic:
        # ---- suggested questions for the selected topic ----
        topic = st.session_state.selected_topic

        if st.button("⬅ Back to Health Topics"):
            st.session_state.selected_topic = None
            st.rerun()

        st.markdown(f"### {topic} — Suggested Questions")

        q_cols = st.columns(2)
        for i, q in enumerate(TOPIC_QUESTIONS[topic]):
            with q_cols[i % 2]:
                if st.button(q, key=f"sugg_{topic}_{i}", use_container_width=True):
                    st.session_state.pending_question = q
                    st.session_state.pending_topic_title = topic.split(" ", 1)[1]  # strip emoji
                    st.session_state.selected_topic = None
                    current_chat_data["show_welcome"] = False
                    st.rerun()

    else:
        # ---- clickable health topic cards ----
        st.markdown("### 🩺 Health Topics")

        topic_cols = st.columns(4)
        for i, topic in enumerate(TOPIC_QUESTIONS.keys()):
            with topic_cols[i % 4]:
                if st.button(topic, key=f"topic_{i}", use_container_width=True):
                    st.session_state.selected_topic = topic
                    st.rerun()

        st.markdown("---")

        # ---- general example questions ----
        st.markdown("### 💬 Example Questions")
        ex_cols = st.columns(2)
        for i, q in enumerate(GENERAL_EXAMPLE_QUESTIONS):
            with ex_cols[i % 2]:
                if st.button(q, key=f"ex_{i}", use_container_width=True):
                    st.session_state.pending_question = q
                    current_chat_data["show_welcome"] = False
                    st.rerun()

    st.info(
        "👋 Welcome! Ask any health-related question. "
        "Mediora AI will provide educational information based on its medical knowledge base."
    )

# ===============================
# Chat messages (scrollable)
# ===============================
else:
    if st.button("⬅ Back to Health Topics"):
        current_chat_data["show_welcome"] = True
        st.rerun()

    chat_window = st.container(height=500)
    with chat_window:
        for message in current_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


question = st.chat_input("Ask your medical question...")

# a click on a topic/example question acts the same as typing it
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None

if question:
    current_chat = st.session_state.current_chat
    chat_data = st.session_state.chats[current_chat]

    chat_data["messages"].append(
        {
            "role": "user",
            "content": question
        }
    )
    chat_data["show_welcome"] = False

    # short, clean sidebar title instead of the full question
    if chat_data["title"] == "New Chat":
        chat_data["title"] = make_chat_title(
            question, topic_name=st.session_state.pending_topic_title
        )
    st.session_state.pending_topic_title = None

    results = search(question, vector_db, top_k=3)

    context = ""
    for score, text in results:
        context += f"\n[Similarity: {score:.3f}]\n{text}\n"

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        answer = response.text if response.text else "No response received from Gemini."

    except Exception as e:
        print("Gemini Error:", e)
        if "503" in str(e):
            answer = "⚠️ Gemini server is currently busy. Please try again in a few seconds."
        elif "429" in str(e):
            answer = "⚠️ AI service is temporarily unavailable because the free API quota has been reached."
        elif "ConnectError" in str(e):
            answer = "⚠️ Unable to connect to Gemini. Please check your internet connection."
        else:
            answer = f"Error: {e}"

    chat_data["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()

st.caption(
    "This application is for educational purposes only and should not replace professional medical advice."
)