import streamlit as st
from google import genai


def build_prompt(audition_material, medium, analysis_style):

    return f"""
You are simultaneously:

1. A senior casting director.
2. An acting coach.
3. A script analyst.
4. A self-tape consultant.

Analysis Style:
{analysis_style}

Medium:
{medium}

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



st.title("🎬 Audition Helper AI")

medium = st.selectbox(
    "Medium",
    [
        "Film",
        "OTT",
        "Commercial",
        "TV Serial",
        "Theatre"
    ]
)

analysis_style = st.select_slider(
    "Analysis Style",
    options=[
        "Strict",
        "Balanced",
        "Creative"
    ],
    value="Balanced"
)


audition_material = st.text_area(
    "Paste your audition material here",
    height=300
)

with st.sidebar:
    api_key = st.text_input(
        "Gemini API Key",
        type="password"
    )

if api_key:
    client = genai.Client(api_key=api_key)
    st.success("Connected")
else:
    client = None

st.write("Selected Medium:", medium)
st.write("Characters typed:", len(audition_material))

if st.button("Analyze Audition"):
    with st.spinner("🎬 Analyzing audition..."):
        if client is None:
            st.error("Please enter a valid Gemini API Key first.")
        else:
            prompt = build_prompt(
                audition_material,
                medium,
                analysis_style
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.write(response.text)
            st.download_button(
                label="📄 Download Analysis",
                data=response.text,
                file_name="audition_analysis.txt",
                mime="text/plain"
            )
            analysis_depth = st.selectbox(
    "Analysis Depth",
    [
        "Quick Audition",
        "Detailed",
        "Masterclass"
    ]
)
audition_type = st.selectbox(
    "Audition Type",
    [
        "Film",
        "OTT",
        "TV Serial",
        "Commercial",
        "Voice Over"
    ]
)