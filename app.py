import streamlit as st
from src.resume_parser import extract_text

def main():
    st.set_page_config(
        page_title="Smart Resume Analyzer",
        page_icon="📄",
        layout="wide"
    )

    st.title("Smart Resume Analyzer")
    st.subheader("Compare a resume with a job description to analyze the match.")
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
        if not uploaded_file:
            st.warning("Please upload a resume file to proceed.")
        elif not job_description.strip():
            st.warning("Please paste a job description to proceed.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    # 1. Parse Resume
                    file_bytes = uploaded_file.read()
                    filename = uploaded_file.name
                    resume_text = extract_text(file_bytes, filename)

                    st.success("Resume parsed successfully!")

                    # Display extracted text in an expander
                    with st.expander("View Extracted Resume Text"):
                        st.text(resume_text)

                    # Placeholder message for upcoming features
                    st.info("ℹ️ Advanced analysis (Skill Extraction, Matching, and Scoring) will be implemented in future sessions.")

                except Exception as e:
                    st.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main()
