import streamlit as st
from src.resume_parser import extract_text
from src.ai_analyzer import analyze_resume_match

def apply_custom_css():
    st.markdown(
        """
        <style>
        /* Cinematic Gradient Title */
        .cinematic-title {
            font-size: 4rem !important;
            font-weight: 800 !important;
            background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px !important;
            padding-bottom: 10px;
            text-align: center;
        }

        .cinematic-subtitle {
            text-align: center;
            color: #a0a0b0;
            font-size: 1.2rem;
            margin-bottom: 40px;
            font-weight: 300;
        }

        /* Target Streamlit containers to act as Glassmorphism Cards */
        [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background: rgba(21, 21, 30, 0.6) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding: 25px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        }

        /* Glowing Primary Button */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
            transition: all 0.3s ease 0s;
        }

        div.stButton > button:first-child:hover {
            box-shadow: 0 6px 20px rgba(0, 210, 255, 0.6);
            transform: translateY(-2px);
            color: white;
        }

        /* Score text styling */
        .score-text {
            font-size: 3rem;
            font-weight: bold;
            color: #00d2ff;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        /* General Spacing */
        .stProgress > div > div > div > div {
            background-color: #00d2ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="Smart Resume Analyzer",
        page_icon="🤖",
        layout="wide"
    )

    apply_custom_css()

    # Sidebar for API Key
    st.sidebar.title("⚙️ Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )
    st.sidebar.markdown(
        "Get your API key from [OpenAI](https://platform.openai.com/account/api-keys)."
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Data is processed in memory and sent directly to OpenAI.")

    # Header
    st.markdown('<h1 class="cinematic-title">Smart Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cinematic-subtitle">Elevate your hiring process with AI-driven insights.</p>', unsafe_allow_html=True)

    # Layout using columns for input
    col1, col2 = st.columns(2)

    with col1:
        # Use native container so the CSS targets it correctly as a block
        with st.container():
            st.write("### 📄 Upload Resume")
            uploaded_file = st.file_uploader(
                "Upload a PDF or DOCX file",
                type=["pdf", "docx"],
                label_visibility="collapsed"
            )

    with col2:
        with st.container():
            st.write("### 💼 Job Description")
            job_description = st.text_area(
                "Paste the job description here",
                height=150,
                placeholder="E.g., We are looking for a Software Engineer with experience in Python...",
                label_visibility="collapsed"
            )

    st.write("") # Spacer

    # Analysis Trigger
    if st.button("🚀 Analyze Match", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar.")
        elif not uploaded_file:
            st.warning("Please upload a resume file to proceed.")
        elif not job_description.strip():
            st.warning("Please paste a job description to proceed.")
        else:
            with st.spinner("Analyzing with AI..."):
                try:
                    # 1. Parse Resume
                    file_bytes = uploaded_file.read()
                    filename = uploaded_file.name
                    resume_text = extract_text(file_bytes, filename)

                    # 2. AI Analysis
                    results = analyze_resume_match(
                        resume_text=resume_text,
                        job_description=job_description,
                        api_key=api_key
                    )

                    # 3. Display Results in a glass card container
                    st.write("")
                    with st.container():
                        st.markdown(f'<p class="score-text">{results["score"]}%</p>', unsafe_allow_html=True)
                        st.markdown("<p style='text-align: center; color: #a0a0b0;'>Match Score</p>", unsafe_allow_html=True)

                        st.progress(results['score'] / 100)

                        st.markdown("---")
                        st.markdown("### 💡 AI Insights")
                        st.write(results['explanation'])
                        st.markdown("---")

                        col_match, col_miss = st.columns(2)
                        with col_match:
                            st.markdown("#### 🟢 Matched Skills")
                            if results['matched_skills']:
                                for skill in results['matched_skills']:
                                    st.markdown(f"- {skill}")
                            else:
                                st.write("None found.")

                        with col_miss:
                            st.markdown("#### 🔴 Missing Skills")
                            if results['missing_skills']:
                                for skill in results['missing_skills']:
                                    st.markdown(f"- {skill}")
                            else:
                                st.write("None found.")

                    # Display extracted text in an expander at the bottom
                    with st.expander("🔍 View Extracted Resume Text"):
                        st.text(resume_text)

                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
