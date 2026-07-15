# 🩺 Mediora AI

> **Your AI-Powered Medical Knowledge Assistant**

Mediora AI is a Retrieval-Augmented Generation (RAG) chatbot that enables users to ask medical questions in natural language and receive accurate, context-aware answers based on a curated collection of medical PDF documents. Inspired by NotebookLM, Mediora AI searches across multiple medical references and generates responses using Google's Gemini AI.

---

## ✨ Features

* 📚 Supports multiple medical PDF documents
* 🤖 AI-powered question answering using Google Gemini
* 🔍 Semantic search with vector embeddings
* 🧠 Retrieval-Augmented Generation (RAG)
* 📄 Source-aware responses from uploaded PDFs
* ⚡ Fast retrieval using Chroma Vector Database
* 💬 Interactive chatbot interface
* ➕ Easily expand the knowledge base by adding new PDFs

---

## 🛠️ Tech Stack

| Technology             | Purpose               |
| ---------------------- | --------------------- |
| Python                 | Backend               |
| LangChain              | RAG Pipeline          |
| Google Gemini          | Large Language Model  |
| ChromaDB               | Vector Database       |
| HuggingFace Embeddings | Document Embeddings   |
| PyPDF                  | PDF Processing        |
| python-dotenv          | Environment Variables |

---

## 📂 Project Structure

```text
Mediora-AI/
│
├── medical_pdfs/          # Medical PDF documents
│
├── vector_store/          # Chroma vector database
│
├── ingest.py              # Builds the vector database
├── chatbot.py             # Chatbot application
├── config.py              # Project configuration
├── utils.py               # Helper functions
│
├── requirements.txt
├── .env
├── README.md
│
└── LICENSE
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mediora-ai.git
cd mediora-ai
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv myenv
myenv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Configure API Key

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## 📚 Add Medical Documents

Place all your medical PDF files inside:

```text
medical_pdfs/
```

Example:

```text
medical_pdfs/
├── Anatomy.pdf
├── Physiology.pdf
├── Pharmacology.pdf
├── Pathology.pdf
├── Microbiology.pdf
├── Surgery.pdf
└── Medicine.pdf
```

---

## 🧠 Build the Knowledge Base

Run:

```bash
python ingest.py
```

This will:

* Read all PDFs
* Split documents into chunks
* Generate embeddings
* Store vectors in ChromaDB

---

## 💬 Start the Chatbot

Run:

```bash
python chatbot.py
```

Example:

```text
Ask your question:

> What are the symptoms of dengue fever?
```

Example response:

```text
Dengue fever commonly presents with:

• High fever
• Severe headache
• Pain behind the eyes
• Muscle and joint pain
• Skin rash
• Mild bleeding

Source:
Medicine.pdf (Page 124)
```

---

## 📌 Future Enhancements

* 🌐 Streamlit web interface
* 📱 Responsive UI
* 🎤 Voice input and output
* 🖼️ Medical image understanding
* 📝 Conversation history
* ⭐ Bookmark important responses
* 📊 Analytics dashboard
* 👨‍⚕️ Doctor mode
* 🌍 Multi-language support
* 🔒 User authentication
* ☁️ Cloud deployment

---

## 🎯 Use Cases

* Medical students
* Healthcare professionals
* Researchers
* Academic institutions
* Medical libraries
* Knowledge management
* Clinical reference

---

## ⚠️ Disclaimer

Mediora AI is designed for educational and informational purposes only. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making medical decisions.

---

## 👩‍💻 Author

**Sneha Singha**

B.Tech – Computer Science & Engineering

Guru Nanak Institute of Technology (GNIT)

---

## 📜 License

This project is licensed under the MIT License.

---

# ⭐ If you find this project useful, consider giving it a star on GitHub!
