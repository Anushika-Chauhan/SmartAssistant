import streamlit as st
import base64
import os
from utils import (
    extract_text, summarize_document,
    generate_diverse_challenge_questions,
    evaluate_answers, answer_question_with_justification
)

# === Dynamic Background Setter ===
def set_background(image_path, opacity=0.9):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    ext = os.path.splitext(image_path)[1][1:]
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, {opacity}), rgba(255, 255, 255, {opacity})),
                    url("data:image/{ext};base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .highlight-box {{
        background-color: rgba(255, 255, 255, 0.88);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# === Floating Image (Ask Me only) ===
def render_corner_image(image_path, width=150):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    ext = os.path.splitext(image_path)[1][1:]
    st.markdown(
        f"""
        <div style="position: fixed; bottom: 20px; right: 20px; z-index: 999;">
            <img src="data:image/{ext};base64,{encoded}" width="{width}">
        </div>
        """,
        unsafe_allow_html=True
    )

# === Streamlit Config ===
st.set_page_config(page_title="Smart Research Assistant", layout="wide")

# === Default Mode (before upload or selection) ===
if "mode" not in st.session_state:
    st.session_state.mode = "Initial"

# === Background Based on Mode ===
if st.session_state.mode == "Challenge Me":
    set_background("C:/Users/anike/OneDrive/Desktop/challenge-background-with-colorful-style_23-2147674602.avif", opacity=0.82)
elif st.session_state.mode == "Ask a Question":
    set_background("C:/Users/anike/OneDrive/Desktop/ask me.webp", opacity=0.85)
else:
    set_background("C:/Users/anike/OneDrive/Desktop/main.png", opacity=0.95)

# === Cache Helpers ===
@st.cache_data(show_spinner=False)
def cached_extract_text(file_path):
    return extract_text(file_path)

@st.cache_data(show_spinner=False)
def cached_summarize(text):
    return summarize_document(text)

@st.cache_data(show_spinner=False)
def cached_generate_questions(text):
    return generate_diverse_challenge_questions(text, num_questions=3)

# === Title and Upload ===
st.title("📚 Smart Assistant for Research Summarization")
uploaded_file = st.file_uploader("Upload your document (.pdf or .txt)", type=["pdf", "txt"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = cached_extract_text(uploaded_file.name)
    summary = cached_summarize(text)

    # === Summary Box ===
    with st.container():
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.subheader("📌 Summary of Document")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)

    # === Mode Switch Buttons ===
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🧠 Challenge Me"):
                st.session_state.mode = "Challenge Me"
        with c2:
            if st.button("🤖 Ask a Question"):
                st.session_state.mode = "Ask a Question"

    mode = st.session_state.mode
    st.markdown(f"### Selected Mode: {mode}")

    # === Challenge Me Mode ===
    if mode == "Challenge Me":
        st.subheader("🧠 Generate & Answer Challenge Questions")
        if st.button("Generate Questions"):
            with st.spinner("Generating challenge questions..."):
                st.session_state.questions = cached_generate_questions(text)

        if "questions" in st.session_state:
            user_answers = []
            for i, q in enumerate(st.session_state.questions, 1):
                with st.container():
                    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                    st.markdown(f"**Q{i}: {q}**")
                    ans = st.text_area(f"Your Answer to Q{i}", key=f"ans_{i}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    user_answers.append({"question": q, "answer": ans})

            if st.button("Evaluate Answers"):
                with st.spinner("Evaluating..."):
                    results = evaluate_answers(user_answers, text)
                st.subheader("📊 Evaluation Results")
                for i, r in enumerate(results, 1):
                    with st.container():
                        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                        st.markdown(f"**Q{i}: {r['question']}**")
                        st.write(f"- Your Answer: {r['user_answer']}")
                        st.write(f"- Reference Answer: {r['reference_answer']}")
                        st.write(f"- Score: `{r['score']}`")
                        st.markdown('</div>', unsafe_allow_html=True)

    # === Ask a Question Mode ===
    elif mode == "Ask a Question":
        st.subheader("🤖 Ask Any Question from the Document")
        user_q = st.text_input("Ask your question here:")
        if user_q:
            with st.spinner("Searching and answering..."):
                answer, justification = answer_question_with_justification(user_q, text)

            with st.container():
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.markdown("**Answer:**")
                st.write(answer)
                st.markdown("**Justification (Context):**")
                st.write(justification)
                st.markdown('</div>', unsafe_allow_html=True)

        # Show corner image in Ask Me
        render_corner_image("C:/Users/anike/OneDrive/Desktop/ask me.png")
