import streamlit as st
import os
import json
import time
import config

try:
    from prompts import (
        PROMPT_TRIAGE,
        PROMPT_MATCHING_360,
        PROMPT_EXECUTIVE_SUMMARY,
        PROMPT_FEEDBACK
    )
    from utils import (
        read_document,
        find_links,
        get_github_context,
        get_portfolio_context,
        call_gemini_api,
        save_to_db
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

st.set_page_config(
    page_title="Inter-sight | AI-Powered Recruiting",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🎯"
)

# Custom CSS with Swipe Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(-45deg, #1a1a2e, #16213e, #0f3460, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }

    h1 {
        background: linear-gradient(120deg, #00d4ff, #7b2ff7, #f107a3);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        font-weight: 700;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 0;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    .traffic-light {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 20px 0;
        padding: 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50px;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .traffic-light-dot {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px currentColor;
    }

    .traffic-light-dot.active {
        transform: scale(1.5);
        animation: glow 1.5s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px currentColor; }
        50% { box-shadow: 0 0 40px currentColor; }
    }

    /* SWIPE ANIMATIONS */
    .candidate-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 30px;
        padding: 30px;
        border: 2px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4);
        animation: slideIn 0.5s ease;
        margin: 20px 0;
        transition: all 0.3s ease;
        position: relative;
    }

    .candidate-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
        border-color: rgba(0, 212, 255, 0.5);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Swipe animations */
    @keyframes swipeRight {
        to {
            transform: translateX(150%) rotate(20deg);
            opacity: 0;
        }
    }

    @keyframes swipeLeft {
        to {
            transform: translateX(-150%) rotate(-20deg);
            opacity: 0;
        }
    }

    @keyframes swipeUp {
        to {
            transform: translateY(-150%) scale(0.8);
            opacity: 0;
        }
    }

    .swipe-right {
        animation: swipeRight 0.5s ease-out forwards;
    }

    .swipe-left {
        animation: swipeLeft 0.5s ease-out forwards;
    }

    .swipe-up {
        animation: swipeUp 0.5s ease-out forwards;
    }

    .match-percentage {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(120deg, #00ff87, #60efff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 255, 135, 0.5);
    }

    .stButton > button {
        border-radius: 50px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover:before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5) !important;
    }

    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }

    /* Button colors */
    div[data-testid="column"]:nth-child(1) button {
        background: linear-gradient(135deg, #ff4757, #ff6348) !important;
        color: white !important;
    }

    div[data-testid="column"]:nth-child(1) button:hover {
        background: linear-gradient(135deg, #ff6348, #ff4757) !important;
    }

    div[data-testid="column"]:nth-child(2) button {
        background: linear-gradient(135deg, #ffa502, #ffdd59) !important;
        color: #1a1a2e !important;
    }

    div[data-testid="column"]:nth-child(2) button:hover {
        background: linear-gradient(135deg, #ffdd59, #ffa502) !important;
    }

    div[data-testid="column"]:nth-child(3) button {
        background: linear-gradient(135deg, #2ed573, #7bed9f) !important;
        color: white !important;
    }

    div[data-testid="column"]:nth-child(3) button:hover {
        background: linear-gradient(135deg, #7bed9f, #2ed573) !important;
    }

    .stAlert {
        border-radius: 15px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
    }

    .element-container div[data-testid="stMarkdownContainer"] p {
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(0, 212, 255, 0.3) !important;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }

    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
        transform: scale(1.02);
    }

    [data-testid="stFileUploader"] {
        border-radius: 20px !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 212, 255, 0.5) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    .stProgress > div > div {
        background: linear-gradient(90deg, #00d4ff, #7b2ff7) !important;
        border-radius: 10px !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: scale(1.05);
        border-color: rgba(0, 212, 255, 0.5);
    }

    img {
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    img:hover {
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6) !important;
    }

    .stSpinner > div {
        border-top-color: #00d4ff !important;
    }

    hr {
        margin: 30px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    }

    /* Success/Error message animations */
    .stSuccess, .stError, .stInfo, .stWarning {
        animation: slideInRight 0.5s ease;
    }

    @keyframes slideInRight {
        from {
            transform: translateX(100px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'candidates' not in st.session_state:
    st.session_state.candidates = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'on_hold_candidates' not in st.session_state:
    st.session_state.on_hold_candidates = []
if 'generated_feedback' not in st.session_state:
    st.session_state.generated_feedback = {}
if 'swipe_direction' not in st.session_state:
    st.session_state.swipe_direction = None

UPLOAD_DIR = "./uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Sidebar
with st.sidebar:
    st.markdown("# 🎯 Inter-sight")
    st.markdown("---")

    if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your-api-key-here":
        st.error("⚠️ API Key not configured")
    else:
        st.success("✅ API Connected")

    st.markdown("---")
    st.markdown("### ⚙️ Configuration")

    blind_mode = st.toggle(
        "🕶️ Blind Mode",
        value=True,
        help="Remove bias by hiding candidate names"
    )

    if blind_mode:
        st.info("👁️ Blind Mode: Active\n\nFocus on Risk, Potential & Evidence")

    st.markdown("---")
    st.markdown("### 📊 The 3 Pillars")
    st.markdown("🚨 **Risk**: Red flags detection")
    st.markdown("💎 **Potential**: Hidden gems")
    st.markdown("✅ **Evidence**: Skill proof")

# Main Header
st.markdown("# Inter-sight")
st.markdown('<p class="subtitle">Stop guessing. Start hiring with evidence.</p>', unsafe_allow_html=True)

# STEP 1: Upload
with st.expander("📋 STEP 1: Configure Job & Upload CVs", expanded=True):
    job_text = st.text_area(
        "🎯 Job Description",
        height=100,
        placeholder="Seeking Sr. Python Developer with AWS experience..."
    )

    culture_text = st.text_area(
        "🏢 Company Culture",
        height=100,
        placeholder="We value innovation, proactivity, and continuous learning..."
    )

    uploaded_files = st.file_uploader(
        "📄 Upload CVs (PDF or DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Analysis", use_container_width=True):
            if not config.GOOGLE_API_KEY or config.GOOGLE_API_KEY == "your-api-key-here":
                st.error("❌ Please configure your API Key")
            elif not job_text or not culture_text or not uploaded_files:
                st.error("❌ Please fill all fields and upload CVs")
            else:
                st.session_state.candidates = []
                st.session_state.current_index = 0
                st.session_state.on_hold_candidates = []
                st.session_state.generated_feedback = {}

                progress_bar = st.progress(0, "🔄 Starting analysis...")
                total_files = len(uploaded_files)

                for i, file in enumerate(uploaded_files):
                    start_time = time.time()
                    progress_text = f"🔍 Analyzing {file.name} ({i + 1}/{total_files})..."
                    progress_bar.progress((i + 1) / total_files, text=progress_text)

                    timestamp = int(start_time)
                    save_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.name}")

                    try:
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                    except Exception as e:
                        st.error(f"Error saving {file.name}: {e}")
                        continue

                    cv_text = read_document(file)
                    if cv_text.startswith("Error:"):
                        st.error(f"Could not read {file.name}")
                        continue

                    found_links = find_links(cv_text)

                    triage_prompt = PROMPT_TRIAGE.format(
                        job_description=job_text,
                        cv_text=cv_text
                    )
                    triage_json_str = call_gemini_api(triage_prompt)

                    try:
                        triage_json = json.loads(triage_json_str)
                    except json.JSONDecodeError:
                        st.error(f"Parsing error for {file.name}")
                        continue

                    if "error" in triage_json:
                        st.error(f"Stage 1 error: {triage_json['error']}")
                        continue

                    job_category = triage_json.get("job_category", "Other")
                    urls_to_analyze = triage_json.get("urls_to_analyze", [])

                    external_context = "N/A"
                    if urls_to_analyze:
                        first_url = urls_to_analyze[0]
                        if job_category == "Tech" and "github" in first_url.lower():
                            external_context = get_github_context(first_url)
                        elif job_category == "Design" and (
                                "behance" in first_url.lower() or "dribbble" in first_url.lower()):
                            external_context = get_portfolio_context(first_url)

                    analysis_360_prompt = PROMPT_MATCHING_360.format(
                        job_and_culture_text=f"{job_text}\n{culture_text}",
                        cv_text=cv_text,
                        external_context=external_context
                    )
                    analysis_360_str = call_gemini_api(analysis_360_prompt)

                    try:
                        analysis_360 = json.loads(analysis_360_str)
                    except json.JSONDecodeError:
                        st.error(f"Stage 2 parsing error for {file.name}")
                        continue

                    if "error" in analysis_360:
                        st.error(f"Stage 2 error: {analysis_360['error']}")
                        continue

                    save_to_db(
                        filename=file.name,
                        filepath=save_path,
                        analysis_json=analysis_360,
                        feedback_email=None,
                        status='analyzed'
                    )

                    st.session_state.candidates.append({
                        "id": f"{timestamp}_{file.name}",
                        "filename": file.name,
                        "analysis_360": analysis_360,
                        "full_context": {
                            "cv_text": cv_text,
                            "culture_text": culture_text,
                            "job_title": job_text.split('\n')[0] if job_text else "Position",
                            "company_name": culture_text.split('\n')[0] if culture_text else "Company"
                        }
                    })

                progress_bar.success(f"✅ {len(st.session_state.candidates)} candidates ready!")
                time.sleep(1)
                st.rerun()

st.markdown("---")

# STEP 2: Swipe Interface
st.markdown("## 👥 STEP 2: Candidate Review")

if not st.session_state.candidates:
    st.info("👆 Upload CVs in Step 1 to begin reviewing candidates")
elif st.session_state.current_index >= len(st.session_state.candidates):
    st.success("🎉 All candidates reviewed!")
    st.balloons()
else:
    current_candidate = st.session_state.candidates[st.session_state.current_index]
    analysis = current_candidate["analysis_360"]

    color_map = {
        "green": "#2ed573",
        "yellow": "#ffa502",
        "red": "#ff4757",
        "grey": "#6c757d"
    }
    traffic_light = analysis.get("traffic_light", "red")
    traffic_light_color = color_map.get(traffic_light, "grey")

    st.markdown(f"**Candidate {st.session_state.current_index + 1} of {len(st.session_state.candidates)}**")

    # Traffic Light Display
    st.markdown(f"""
    <div class="traffic-light">
        <div class="traffic-light-dot {'active' if traffic_light == 'green' else ''}" 
             style="background-color: {color_map['green']};"></div>
        <div class="traffic-light-dot {'active' if traffic_light == 'yellow' else ''}" 
             style="background-color: {color_map['yellow']};"></div>
        <div class="traffic-light-dot {'active' if traffic_light == 'red' else ''}" 
             style="background-color: {color_map['red']};"></div>
    </div>
    """, unsafe_allow_html=True)

    # Swipe animation CSS
    swipe_class = ""
    if st.session_state.swipe_direction == "left":
        swipe_class = "swipe-left"
    elif st.session_state.swipe_direction == "right":
        swipe_class = "swipe-right"
    elif st.session_state.swipe_direction == "up":
        swipe_class = "swipe-up"

    # Candidate Card with swipe animation
    st.markdown(f'<div class="candidate-card {swipe_class}">', unsafe_allow_html=True)

    col_avatar, col_content = st.columns([1, 2])

    with col_avatar:
        if blind_mode:
            st.image(
                f"https://ui-avatars.com/api/?name=CV&background={traffic_light_color[1:]}&color=FFFFFF&size=200&rounded=true&bold=true&font-size=0.5"
            )
        else:
            initials = "".join([n[0] for n in current_candidate['filename'].replace("_", " ").split()[:2]]).upper()
            st.image(
                f"https://ui-avatars.com/api/?name={initials}&background={traffic_light_color[1:]}&color=FFFFFF&size=200&rounded=true&bold=true"
            )

        st.markdown(f'<div class="match-percentage">{analysis.get("overall_match_accuracy", 0)}%</div>',
                    unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.6);'>Match Score</p>",
                    unsafe_allow_html=True)

    with col_content:
        st.markdown("### 🎯 Analyst Verdict")
        st.info(analysis.get('analyst_summary', 'No summary available'))

        st.markdown("### 💼 Technical Fit")
        if analysis.get('evidence_pillar', {}).get('technical_fit'):
            for skill in analysis['evidence_pillar']['technical_fit']:
                st.markdown(f"**{skill['skill']}**: {skill['fit_score_%']}%")
                st.caption(f"Evidence: {skill['cv_evidence']}")
        else:
            st.caption("_No technical evidence found_")

    if analysis.get('potential_pillar', {}).get('green_flags'):
        st.markdown("### 💎 Hidden Gems")
        for gem in analysis['potential_pillar']['green_flags']:
            st.success(f"**{gem.get('hidden_gem', 'Potential')}**: {gem['detail']}")

    if analysis.get('risk_pillar', {}).get('red_flags'):
        st.markdown("### 🚨 Red Flags")
        for alert in analysis['risk_pillar']['red_flags']:
            st.error(f"**{alert.get('alert', 'Risk')}**: {alert['detail']}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Action Buttons
    st.markdown("")
    col_left, col_center, col_right = st.columns(3)

    with col_left:
        if st.button("⬅️ Reject", use_container_width=True, key="reject"):
            st.session_state.swipe_direction = "left"
            time.sleep(0.5)
            with st.spinner("Generating feedback..."):
                feedback_prompt = PROMPT_FEEDBACK.format(
                    candidate_name=current_candidate['filename'].split('.')[0],
                    job_title=current_candidate['full_context']['job_title'],
                    company_name=current_candidate['full_context']['company_name'],
                    analysis_json=json.dumps(analysis)
                )
                feedback_email = call_gemini_api(feedback_prompt)
                st.session_state.generated_feedback[current_candidate['id']] = feedback_email
            st.session_state.current_index += 1
            st.session_state.swipe_direction = None
            st.rerun()

    with col_center:
        if st.button("⏸️ On Hold", use_container_width=True, key="hold"):
            st.session_state.swipe_direction = "up"
            time.sleep(0.5)
            st.session_state.on_hold_candidates.append(current_candidate)
            st.session_state.current_index += 1
            st.session_state.swipe_direction = None
            st.rerun()

    with col_right:
        if st.button("✅ Accept", use_container_width=True, key="accept"):
            st.session_state.swipe_direction = "right"
            time.sleep(0.5)
            st.session_state.current_index += 1
            st.session_state.swipe_direction = None
            st.rerun()

# STEP 3: On Hold Review
if st.session_state.on_hold_candidates and st.session_state.current_index >= len(st.session_state.candidates):
    st.markdown("---")
    st.markdown("## ⏸️ STEP 3: Final Decision")
    st.info("Review candidates on hold and make a final decision")

    for i, candidate in enumerate(st.session_state.on_hold_candidates):
        analysis = candidate["analysis_360"]
        with st.expander(f"**{candidate['filename']}** - {analysis.get('overall_match_accuracy', 0)}% Match"):
            st.info(analysis.get('analyst_summary', 'N/A'))

            if st.button(f"📄 Request Executive Summary", key=f"info_{i}"):
                with st.spinner("Generating summary..."):
                    summary_prompt = PROMPT_EXECUTIVE_SUMMARY.format(
                        analysis_json=json.dumps(analysis),
                        culture_text=candidate['full_context']['culture_text']
                    )
                    executive_summary = call_gemini_api(summary_prompt)
                    st.markdown(executive_summary)

            col_no, col_yes = st.columns(2)
            with col_no:
                if st.button("❌ Final Reject", key=f"no_{i}", use_container_width=True):
                    st.session_state.on_hold_candidates.pop(i)
                    st.rerun()
            with col_yes:
                if st.button("✅ Final Accept", key=f"yes_{i}", use_container_width=True):
                    st.session_state.on_hold_candidates.pop(i)
                    st.rerun()

# STEP 4: Feedback Emails
if st.session_state.generated_feedback:
    st.markdown("---")
    st.markdown("## 📧 Generated Feedback Emails")
    for candidate_id, email_body in st.session_state.generated_feedback.items():
        with st.expander(f"Email for {candidate_id}"):
            email_key = f"email_{candidate_id.replace('.', '_')}"
            st.text_area("Email Body", email_body, height=200, key=email_key)