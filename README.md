
# 📚 Smart Assistant for Research Summarization

A GenAI-powered assistant that reads and understands documents (PDF/TXT) to:
- Answer user questions with contextual accuracy
- Generate logical challenge questions
- Evaluate user responses with detailed justifications

---

## 🧠 Objective

This project was developed as part of an AI internship assignment to demonstrate:
- Deep comprehension of documents
- Reasoning and evaluation capabilities through question generation and answer analysis
- A clean, interactive user interface built using Streamlit

---

## 🚀 Features

- Upload PDF or TXT files  
- Auto-generate concise document summaries (≤150 words)  
- Ask questions related to the document content  
- Receive logic-based challenge questions generated automatically  
- Get instant evaluation and justification for your answers  
- Grounded and justified answers to all user queries  
- Responsive backgrounds and image-rich UI for enhanced user experience  
- Runs locally with Streamlit — no cloud dependency

---

## 🏗️ Architecture

![Architecture](assests/architecture.png)

---

## 🔁 Workflow

![Workflow](assests/IMG-20250714-WA0017.jpg)

---

## 🖥️ Output Samples

![Output1](assests/1.png)  
![Output2](assests/2.png)  
![Output3](assests/3.png)  
![Output5](assests/5.png)
![Output4](assests/4.png)  
  
![Output6](assests/6.png)  

---

## 🛠️ Tech Stack

- Python  
- Streamlit for the web UI  
- FLAN-T5 (or similar) for question answering and reasoning  
- PyMuPDF / PDFReader for PDF text extraction  
- HuggingFace Transformers & SentenceTransformers for NLP tasks  

---



## 📂 How to Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/Anushika-Chauhan/SmartAssistant.git
   cd SmartAssistant


2. **Create and activate a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

5. **Using the app**

   * Upload your PDF or TXT document
   * View the summary generated automatically
   * Ask questions or answer automatically generated challenge questions
   * Receive instant answers, evaluations, and justifications
### 📽️ Project Demo

[![Watch the demo](https://raw.githubusercontent.com/Anushika-Chauhan/SmartAssistant/refs/heads/master/assests/demo.webp)](https://drive.google.com/file/d/1wuMUXtMcB_35s3NUSSPWF1mONHjQBMDS/view?usp=sharing)

> 🎬 Click the image to watch a full video demonstration of the Smart Assistant in action.



## 🙋‍♀️ Contact

If you have any questions, suggestions, or just want to connect, feel free to reach out:

**Anushika Chauhan**  
📧 Email: [anuchauhan1569@gmail.com](mailto:anuchauhan1569@gmail.com)  
🔗 GitHub: [github.com/Anushika-Chauhan](https://github.com/Anushika-Chauhan)  
🌐 LinkedIn: [linkedin.com/in/anushika-chauhan](https://www.linkedin.com/in/anushika-chauhan-0b8365284)

Looking forward to hearing from you! 😊





