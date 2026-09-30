import time
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
        "Gemini API Key",
        type="password",
        placeholder="AIzaSy..."
    )
    st.sidebar.markdown(
        "Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)."
    )
    st.sidebar.markdown("---")
    st.sidebar.caption("Data is processed in memory and sent directly to Google Gemini.")

    # Header
    st.markdown('<h1 class="cinematic-title">Smart Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="cinematic-subtitle">Elevate your hiring process with AI-driven insights.</p>', unsafe_allow_html=True)

    # Layout using columns for input
    col1, col2 = st.columns(2)

    with col1:
        # Use native container so the CSS targets it correctly as a block
        with st.container():
            st.write("### 📄 Upload Resumes (Batch)")
            uploaded_files = st.file_uploader(
                "Upload PDF or DOCX files",
                type=["pdf", "docx"],
                accept_multiple_files=True,
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
    if st.button("🚀 Analyze Batch", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
        elif not uploaded_files:
            st.warning("Please upload at least one resume file to proceed.")
        elif not job_description.strip():
            st.warning("Please paste a job description to proceed.")
        else:
            total_files = len(uploaded_files)
            progress_bar = st.progress(0)
            status_text = st.empty()

            all_results = []

            for i, uploaded_file in enumerate(uploaded_files):
                status_text.write(f"Analyzing {uploaded_file.name} ({i+1}/{total_files})...")
                try:
                    # 1. Parse Resume
                    file_bytes = uploaded_file.read()
                    filename = uploaded_file.name
                    resume_text = extract_text(file_bytes, filename)

                    # 2. AI Analysis

                    if i > 0:
                        # Graceful rate limit handling
                        time.sleep(2)

                    results = analyze_resume_match(
                        resume_text=resume_text,
                        job_description=job_description,
                        api_key=api_key
                    )

                    # Store filename in results for reference if needed
                    results['filename'] = filename
                    all_results.append(results)

                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")

                # Update progress
                progress_bar.progress((i + 1) / total_files)

            status_text.write("Analysis Complete!")
            st.write("---")

            # --- Categorized Dashboard ---
            top_matches = []
            moderate_matches = []
            low_matches = []

            for res in all_results:
                score = res.get('match_score', 0)
                if score > 70:
                    top_matches.append(res)
                elif 50 <= score <= 70:
                    moderate_matches.append(res)
                else:
                    low_matches.append(res)

            tab1, tab2, tab3 = st.tabs([
                f"🌟 Top Matches (>70%) [{len(top_matches)}]",
                f"👍 Moderate (50-70%) [{len(moderate_matches)}]",
                f"❌ Low Match (<50%) [{len(low_matches)}]"
            ])

            with tab1:
                if not top_matches:
                    st.info("No candidates scored above 70%.")
                else:
                    for res in sorted(top_matches, key=lambda x: x.get('match_score', 0), reverse=True):
                        with st.container():
                            c_name = res.get('candidate_name', 'Unknown')
                            c_email = res.get('candidate_email', 'Unknown')
                            score = res.get('match_score', 0)

                            col_info, col_score = st.columns([3, 1])
                            with col_info:
                                st.markdown(f"### {c_name}")
                                if c_email != 'Unknown':
                                    st.markdown(f"📧 <a href='mailto:{c_email}'>{c_email}</a>", unsafe_allow_html=True)

                                links = res.get('social_links', [])
                                if links:
                                    # Create a series of link badges
                                    link_html = " ".join([f"<a href='{link}' target='_blank' style='display:inline-block; margin-right:8px; padding:2px 8px; background:rgba(0,210,255,0.2); border-radius:12px; color:#00d2ff; text-decoration:none; font-size:0.9rem;'>🔗 {link.split('//')[-1].split('/')[0]}</a>" for link in links])
                                    st.markdown(f"<div style='margin-top: 8px;'>{link_html}</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown("<div style='margin-top: 8px; color: #a0a0b0; font-size:0.9rem;'>No social links found</div>", unsafe_allow_html=True)

                            with col_score:
                                st.markdown(f"<div style='text-align: right;'><span class='score-text' style='font-size:2.5rem;'>{score}%</span></div>", unsafe_allow_html=True)

                            st.write("")
                            st.markdown("**AI Summary:** " + res.get('short_summary', ''))

                            mc, msc = st.columns(2)
                            with mc:
                                st.markdown("**✅ Matched Skills:**")
                                st.write(", ".join(res.get('matched_skills', [])) or "None")
                            with msc:
                                st.markdown("**⚠️ Missing Skills:**")
                                st.write(", ".join(res.get('missing_skills', [])) or "None")

            with tab2:
                if not moderate_matches:
                    st.info("No candidates scored between 50% and 70%.")
                else:
                    for res in sorted(moderate_matches, key=lambda x: x.get('match_score', 0), reverse=True):
                        with st.container():
                            c_name = res.get('candidate_name', 'Unknown')
                            c_email = res.get('candidate_email', 'Unknown')
                            score = res.get('match_score', 0)

                            st.markdown(f"#### {c_name} — {score}%")
                            if c_email != 'Unknown':
                                st.markdown(f"📧 <a href='mailto:{c_email}'>{c_email}</a>", unsafe_allow_html=True)

                            links = res.get('social_links', [])
                            if links:
                                link_html = " ".join([f"<a href='{link}' target='_blank' style='display:inline-block; margin-right:8px; padding:2px 8px; background:rgba(0,210,255,0.2); border-radius:12px; color:#00d2ff; text-decoration:none; font-size:0.8rem;'>🔗 {link.split('//')[-1].split('/')[0]}</a>" for link in links])
                                st.markdown(f"<div style='margin-bottom: 8px;'>{link_html}</div>", unsafe_allow_html=True)
                            else:
                                st.markdown("<div style='margin-bottom: 8px; color: #a0a0b0; font-size:0.8rem;'>No social links found</div>", unsafe_allow_html=True)

                            st.write("**Matched:** " + (", ".join(res.get('matched_skills', [])) or "None"))

                            with st.expander("View Details (Missing Skills & Summary)"):
                                st.write("**Missing:** " + (", ".join(res.get('missing_skills', [])) or "None"))
                                st.write("**Summary:** " + res.get('short_summary', ''))

            with tab3:
                if not low_matches:
                    st.info("No candidates scored below 50%.")
                else:
                    # Minimal table-like view
                    for res in sorted(low_matches, key=lambda x: x.get('match_score', 0), reverse=True):
                        c_name = res.get('candidate_name', 'Unknown')
                        c_email = res.get('candidate_email', 'Unknown')

                        email_link = f"<a href='mailto:{c_email}'>{c_email}</a>" if c_email != 'Unknown' else "No email"
                        st.markdown(f"- **{c_name}** | 📧 {email_link}", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
