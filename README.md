# 🔎 Advanced Multi-Modal RAG Pipeline 🚀

**End-to-End Retrieval-Augmented Generation for Text, Tables & Images**

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/your-repo-name?style=for-the-badge\&logo=github)](https://github.com/yourusername/your-repo-name/stargazers)
[![License](https://img.shields.io/github/license/yourusername/your-repo-name?style=for-the-badge\&color=blue)](./LICENSE)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge\&logo=python)
![OpenAI](https://img.shields.io/badge/Powered%20By-OpenAI-GPT4o-ff69b4?style=for-the-badge\&logo=openai)
![Status](https://img.shields.io/badge/Build-Stable-success?style=for-the-badge)
![Contributions welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge\&logo=github)

> A next-generation **RAG pipeline** that goes far beyond standard text-based retrieval — enabling intelligent, multi-modal understanding of **documents, tables, and visual data**. With hybrid search, page-level citations, and seamless LLM integration, this project delivers state-of-the-art knowledge extraction and reasoning directly inside a Jupyter Notebook.

---

## 🧠 Overview

This repository contains a fully-functional **Retrieval-Augmented Generation (RAG)** pipeline designed for **multi-modal document intelligence**. It reads and reasons over unstructured text, tabular data, and even embedded images — providing **context-aware answers** with precise citations.

🔍 **What makes it special?**

* Understands **text, tables, and figures** in documents
* Uses **hybrid retrieval (BM25 + embeddings)** for smarter search
* Generates **traceable answers with page-level citations**
* Vision-enabled **LLM reasoning on charts, diagrams, and images**

---

## ✨ Core Features

| Feature                         | Description                                                           |
| ------------------------------- | --------------------------------------------------------------------- |
| 📚 **Multi-Modal Intelligence** | Extracts and understands text, tables, and images from PDFs.          |
| 👁️ **Vision + LLM**            | Uses GPT-4o’s vision capabilities for charts, diagrams, and figures.  |
| 🔍 **Hybrid Search**            | Combines BM25 keyword retrieval with semantic vector search.          |
| 📑 **Grounded Generation**      | Answers include citations with page numbers and content types.        |
| 🧪 **Interactive UI**           | Query, upload, and process docs directly from Jupyter UI.             |
| 🛡️ **Guardrails & Logging**    | Includes logging, moderation, and audit-ready retrieval traceability. |

---

## 🏗️ Architecture Diagram

```
PDFs / Docs ─► Ingestion & Parsing ─► Chunking & Embedding ─► Hybrid Retrieval ─► LLM Generation
      │                      │                     │                     │
      │                      │                     │                     └─► Context-aware Answers + Citations
      │                      │                     │
      └─► Text / Tables / Images ─► Vector DB ─► Query Engine ─► UI Layer
```

---

## ⚙️ Tech Stack

| Component            | Tool                                    |
| -------------------- | --------------------------------------- |
| **Language**         | Python 3.9+                             |
| **LLM & Embeddings** | OpenAI GPT-4o, `text-embedding-3-small` |
| **Framework**        | LangChain                               |
| **Vector Store**     | ChromaDB                                |
| **PDF Parsing**      | PyMuPDF                                 |
| **Keyword Search**   | `rank-bm25`                             |
| **UI**               | Jupyter Notebook + `ipywidgets`         |

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Python 3.9+
* [OpenAI API Key](https://platform.openai.com/)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 3️⃣ Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Set Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY="sk-..."
```

---

## 🧪 How to Use

1. **📁 Add Documents:** Place PDFs inside the `data/` folder.
2. **🚀 Launch Notebook:**

   ```bash
   jupyter notebook "Your_RAG_Notebook_Name.ipynb"
   ```
3. **⚙️ Run Pipeline:** Execute cells sequentially to parse, embed, and retrieve.
4. **💬 Query the System:** Use the interactive UI to ingest new docs and ask questions.

---

## 📸 Demo Screenshots

Here’s a quick look at the RAG pipeline in action 👇

| 📄 Document Parsing                 | 🔎 Query Processing             | 🧠 Answer Generation              |
| ----------------------------------- | ------------------------------- | --------------------------------- |
| ![Parsing](assets/demo_parsing.png) | ![Query](assets/demo_query.png) | ![Answer](assets/demo_answer.png) |

> 💡 *Tip:* Store screenshots in an `assets/` folder at the root of your repository to make this section shine on GitHub.

---

## 🤝 Contributing

We ❤️ contributions!
If you’d like to improve this project:

1. Fork the repo
2. Create a new branch (`feature/your-feature`)
3. Submit a pull request 🚀

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

---

## 🌟 Future Roadmap

* [ ] 🧠 Fine-tune embeddings for domain-specific retrieval
* [ ] 🧮 Add structured query support (SQL + LLM)
* [ ] ☁️ Deploy as a FastAPI / Streamlit web app
* [ ] 🧪 Extend to video & audio document ingestion

---

## 💡 Why This Matters

Most RAG systems only understand text. This project breaks that barrier — integrating **visual reasoning, tabular understanding, and semantic retrieval** into one seamless pipeline. It’s a foundation for the next generation of **enterprise AI search engines, document assistants, and knowledge copilots.**

