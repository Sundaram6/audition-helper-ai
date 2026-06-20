import streamlit as st
from google import genai
import os

if "analysis" not in st.session_state:
    st.session_state.analysis = None


def build_prompt(
    audition_material,
    audition_type,
    analysis_style,
    analysis_depth
):

    return f"""
You are simultaneously:

1. A senior casting director.
2. An acting coach.
3. A script analyst.
4. A self-tape consultant.

Analysis Style:
{analysis_style}

Analysis Depth:
{analysis_depth}

If Analysis Depth is:

Quick Audition:
- Give concise notes
- Focus only on performance
- Maximum 300 words

Detailed:
- Full analysis
- Character breakdown
- Scene analysis
- Performance notes

Masterclass:
- Deep acting analysis
- Character psychology
- Subtext
- Emotional arc
- Performance strategy
- Casting director perspective

Audition Type:
{audition_type}

AUDITION MATERIAL:
{audition_material}

Provide:

CHARACTER BREAKDOWN
- Who Am I?
- Background
- Social Status
- Key Relationships
- Five Words That Define This Character
- Character Animal
- Why This Animal?

SCENE ANALYSIS
- Objective
- Obstacle
- Stakes
- Tactics
- Subtext

EMOTIONAL ARC

AUDITION NOTES

CASTING DIRECTOR NOTES

QUICK PREPARATION
"""


# ---------------- UI ---------------- #

st.title("🎬 Audition Helper AI")


audition_type = st.selectbox(
    "Audition Type",
    [
        "Film",
        "OTT",
        "TV Serial",
        "Commercial",
        "Voice Over",
        "Theatre Monologue",
        "Theatre Scene"
    ]
)


analysis_depth = st.selectbox(
    "Analysis Depth",
    [
        "Quick Audition",
        "Detailed",
        "Masterclass"
    ]
)

audition_material = st.text_area(
    "Paste your audition material here",
    height=300
)

# ---- Safe API key resolution ----
# Priority: 1) env variable  2) streamlit secrets  3) sidebar input
def get_default_api_key():
    """Safely retrieve API key without crashing if secrets don't exist."""
    # Check environment variable first
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    # Safely check Streamlit secrets
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""

default_key = get_default_api_key()

with st.sidebar:
    api_key = st.text_input(
        "Gemini API Key",
        value=default_key,
        type="password",
        placeholder="Paste your Gemini API key here"
    )

# ---- Initialize Gemini client ----
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.sidebar.success("✅ Gemini Connected")
    except Exception as e:
        st.sidebar.error(f"Error initializing Gemini client: {e}")
else:
    st.sidebar.warning("⚠️ Enter your Gemini API Key to proceed.")

st.write("Characters typed:", len(audition_material))

if st.button("🎬 Analyze Audition"):
    if client is None:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    elif not audition_material.strip():
        st.error("Please paste your audition material before analyzing.")
    else:
        with st.spinner("🎭 Analyzing audition..."):
            try:
                prompt = build_prompt(
                    audition_material,
                    audition_type,
                    analysis_style,
                    analysis_depth
                )

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                st.session_state.analysis = response.text
            except Exception as e:
                st.error(f"Analysis failed: {e}")

if st.session_state.analysis:
    st.subheader("🎭 Analysis")
    st.write(st.session_state.analysis)

    st.download_button(
        label="📄 Download Analysis",
        data=st.session_state.analysis,
        file_name="audition_analysis.txt",
        mime="text/plain"
    )