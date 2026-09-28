import streamlit as st
from src.resume_parser import extract_text
from src.ai_analyzer import analyze_resume_match

def main():
    st.set_page_config(
        page_title="Smart Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )

    # Sidebar for API Key
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )
    st.sidebar.markdown(
        "Get your API key from [OpenAI](https://platform.openai.com/account/api-keys)."
    )

    st.title("Smart Resume Analyzer")
    st.subheader("Compare a resume with a job description using AI.")
    st.markdown("---")

    # Layout using columns for input
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 1. Upload Resume")
        uploaded_file = st.file_uploader(
            "Upload a PDF or DOCX file",
            type=["pdf", "docx"]
        )

    with col2:
        st.write("### 2. Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=200,
            placeholder="E.g., We are looking for a Software Engineer with experience in Python..."
        )

    st.markdown("---")

    # Analysis Trigger
    if st.button("Analyze Resume", type="primary", use_container_width=True):
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

                    # 3. Display Results
                    st.success("Analysis Complete!")

                    st.write(f"### Match Score: {results['score']}/100")
                    st.progress(results['score'] / 100)

                    st.markdown("### Analysis Explanation")
                    st.info(results['explanation'])

                    col_match, col_miss = st.columns(2)
                    with col_match:
                        st.write("#### 🟢 Matched Skills")
                        if results['matched_skills']:
                            for skill in results['matched_skills']:
                                st.markdown(f"- {skill}")
                        else:
                            st.write("None found.")

                    with col_miss:
                        st.write("#### 🔴 Missing Skills")
                        if results['missing_skills']:
                            for skill in results['missing_skills']:
                                st.markdown(f"- {skill}")
                        else:
                            st.write("None found.")

                    # Display extracted text in an expander at the bottom
                    with st.expander("View Extracted Resume Text"):
                        st.text(resume_text)

                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
