# utils.py

import fitz  # PyMuPDF
import random  # ✅ add this
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, util

# Load models once
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")  # You can swap to flan-t5-small for speed
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
flan = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 1. Extract text from PDF or TXT
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "\n".join([page.get_text() for page in doc])
    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type. Upload a PDF or TXT.")

# 2. Split text into chunks
def split_text(text, max_words=500):
    words = text.split()
    return [' '.join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

# 3. Summarize document
def summarize_document(text):
    chunks = split_text(text)
    summaries = summarizer(chunks[:3], max_length=150, min_length=60, do_sample=False)
    combined = ' '.join([s['summary_text'] for s in summaries])
    final = summarizer(combined, max_length=150, min_length=60, do_sample=False)[0]['summary_text']
    return final

# 4. Optimized challenge question generation (all in one prompt)
import random

def generate_diverse_challenge_questions(text, num_questions=3):
    seen_embeddings = []
    questions = []
    max_attempts = num_questions * 15
    attempts = 0
    similarity_threshold = 0.75

    base_hints = [
        "Focus on assistant behavior.",
        "Focus on input formats and document structure.",
        "Focus on logic or evaluation flow.",
        "Focus on user interaction and comprehension.",
        "Focus on features like summary or answer scoring.",
        "Focus on assistant's reasoning tasks.",
        "Focus on constraints or functional requirements."
    ]

    bonus_phrases = [
        "Be creative and avoid repetition.",
        "Ensure it's distinct from previous questions.",
        "Make it logical, not surface-level.",
        "Test reasoning or document understanding."
    ]

    def is_duplicate(new_emb):
        return any(util.cos_sim(new_emb, emb).item() > similarity_threshold for emb in seen_embeddings)

    while len(questions) < num_questions and attempts < max_attempts:
        start = random.randint(0, max(0, len(text) - 1500))
        sample_text = text[start:start + 1500]

        prompt = (
            "You are a helpful assistant. Based on the document below, generate **one open-ended** question "
            "that requires **logic, reasoning, or comprehension** to answer.\n"
            "❌ Do NOT generate MCQs or yes/no questions.\n"
            "✅ Ask deep, inferential questions that test understanding of the content.\n"
            f"HINT: {random.choice(base_hints)}\nGOAL: {random.choice(bonus_phrases)}\n\n"
            f"Document:\n\"\"\"\n{sample_text}\n\"\"\""
        )

        try:
            response = flan(prompt, max_new_tokens=80, temperature=0.85, top_k=40)[0]["generated_text"].strip()
        except Exception:
            attempts += 1
            continue

        if not response or len(response.split()) < 6 or response.lower().startswith("question:"):
            attempts += 1
            continue

        new_emb = semantic_model.encode(response)
        if not is_duplicate(new_emb):
            questions.append(response)
            seen_embeddings.append(new_emb)

        attempts += 1

    if len(questions) == 0:
        questions.append("Why is it important for the assistant to reference specific document sections in its answers?")

    return questions



from transformers import pipeline
from sentence_transformers import util
import torch

def evaluate_answers(user_answers, text):
    results = []

    for qa in user_answers:
        question = qa["question"]
        user_answer = qa["answer"]

        # Expanded context window
        context = text[:4000] if len(text) > 4000 else text

        # Prompt to generate a good reference answer
        prompt = f"""
Document:
\"\"\"{context}\"\"\"

Question: {question}

What would be the best possible answer based only on the content above?
Make it complete and directly relevant.
"""

        try:
            reference = flan(prompt, max_new_tokens=150, do_sample=False)[0]['generated_text'].strip()
        except Exception as e:
            reference = "Could not generate reference answer due to error."

        # Semantic similarity
        try:
            user_emb = semantic_model.encode(user_answer, convert_to_tensor=True)
            ref_emb = semantic_model.encode(reference, convert_to_tensor=True)
            score = float(util.cos_sim(user_emb, ref_emb).item())
        except Exception:
            score = 0.0

        results.append({
            "question": question,
            "user_answer": user_answer,
            "reference_answer": reference,
            "score": round(score, 3)
        })

    return results


# 6. QA Bot: Ask with justification
def answer_question_with_justification(question, text):
    sentences = text.split(". ")
    q_emb = semantic_model.encode(question)

    # Score and keep line numbers
    scored_sentences = [
        (i, s.strip(), util.cos_sim(q_emb, semantic_model.encode(s.strip())).item())
        for i, s in enumerate(sentences)
        if len(s.strip()) > 10
    ]
    scored_sentences.sort(key=lambda x: x[2], reverse=True)

    # Top 1–3 lines as justification context
    top_sentences = [s[1] for s in scored_sentences[:3]]
    top_lines_info = [(s[0] + 1, s[1]) for s in scored_sentences[:1]]  # Top line only for precise reference

    context = ". ".join(top_sentences)

    prompt = (
        f"You are a helpful assistant. Use the provided context to answer the user's question.\n\n"
        f"Question: {question}\n\n"
        f"Context:\n\"\"\"\n{context}\n\"\"\"\n\n"
        "Answer clearly and ONLY based on this context."
    )

    try:
        answer = flan(prompt, max_new_tokens=128)[0]['generated_text'].strip()
    except Exception:
        answer = "I'm sorry, I couldn't generate an answer."

    # Line number justification
    if top_lines_info:
        line_no, matched_line = top_lines_info[0]
        justification = f"Supported by Line {line_no}: \"{matched_line.strip()}\""
    else:
        justification = context

    return answer, justification

