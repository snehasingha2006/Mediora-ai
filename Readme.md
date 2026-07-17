# 🩺 Mediora AI

> **AI-Powered Medical Knowledge Assistant using Retrieval-Augmented Generation (RAG)**

Mediora AI is an intelligent medical chatbot that answers health-related questions using **Retrieval-Augmented Generation (RAG)**. It searches a curated medical knowledge base built from PDF documents and generates context-aware responses using **Google Gemini AI**.

> **⚠️ Disclaimer:** Mediora AI is intended for educational purposes only and should not be used as a substitute for professional medical advice.

---

# ✨ Features

- 🩺 AI-powered medical question answering
- 📚 Knowledge base built from medical PDF documents
- 🔍 Semantic search using Sentence Transformers
- 🤖 Google Gemini for natural language responses
- ⚡ Fast retrieval with precomputed vector embeddings
- 💬 Clean and interactive Streamlit chatbot interface
- 📝 Conversation history
- 🗑️ Clear Chat functionality
- 💡 Clickable example questions
- 🚫 Similarity threshold to reduce incorrect answers
- ⚠️ Graceful handling of API quota and server errors

---

# 🛠️ Tech Stack

| Technology            | Purpose               |
| --------------------- | --------------------- |
| Python                | Backend               |
| Streamlit             | Web Application       |
| Google Gemini API     | Large Language Model  |
| Sentence Transformers | Text Embeddings       |
| Joblib                | Vector Storage        |
| scikit-learn          | Similarity Search     |
| python-dotenv         | Environment Variables |

---

# 📂 Project Structure

```text
Mediora-ai/
│
├── docs/                     # Medical PDF documents
│
├── app.py                    # Streamlit application
├── build_database.py         # Build vector database
├── embedding.py              # Generate embeddings
├── vector_store.py           # Semantic search
├── prompts.py                # Prompt template
├── rag.py                    # RAG pipeline
│
├── vector_store.pkl          # Saved vector database
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Mediora-ai.git

cd Mediora-ai
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv env

env\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv env

source env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Configure API Key

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
GEMINI_GEN_MODEL=gemini-2.5-flash
```

---

# 📚 Add Medical Documents

Place your medical PDF files inside the `docs` folder.

Example:

```text
docs/
├── Diabetes.pdf
├── Dengue.pdf
├── Asthma.pdf
├── Hypertension.pdf
├── First_aid.pdf
└── Nutrition and Health.pdf
```

---

# 🧠 Build the Knowledge Base

Run the following command:

```bash
python build_database.py
```

This will:

- Read all PDF documents
- Split documents into chunks
- Generate embeddings
- Save the vector database as `vector_store.pkl`

---

# 🚀 Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

---

# 💬 Example Questions

Try asking questions like:

- What is dengue?
- What are the symptoms of diabetes?
- How can hypertension be prevented?
- What should I do for burns?
- What causes asthma?
- What foods are good for heart health?

---

# 🔄 How It Works

1. User asks a medical question.
2. The question is converted into an embedding.
3. The system searches the medical knowledge base for the most relevant information.
4. Relevant context is sent to Google Gemini.
5. Gemini generates a context-aware answer.
6. The response is displayed in the Streamlit chatbot.

---

# 📸 Screenshots

You can add screenshots here after uploading them.

Example:

```text
screenshots/
├── home.png
├── chatbot.png
```

---

# 🚀 Future Improvements

- 🎤 Voice input
- 🔊 Voice responses
- 🌍 Multi-language support
- 📱 Mobile-friendly interface
- 🔖 Save conversation history
- 👨‍⚕️ Doctor mode
- 📊 Medical analytics dashboard
- ☁️ Cloud deployment
- 🖼️ Medical image understanding

---

# 🎯 Use Cases

- Medical students
- Healthcare professionals
- Researchers
- Academic institutions
- Medical libraries
- Educational learning

---

# ⚠️ Disclaimer

Mediora AI is designed for educational and informational purposes only.

It should **not** be used as a replacement for professional medical advice, diagnosis, or treatment.

Always consult a qualified healthcare professional for medical concerns.

---

# 👩‍💻 Author

**Sneha Jana**
**Sneha singha**

B.Tech – Computer Science & Engineering

Guru Nanak Institute of Technology (GNIT)

---

# ⭐ Support

If you found this project useful, please consider **starring ⭐ the repository** on GitHub.
