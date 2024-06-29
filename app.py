import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType
import os

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Yoga Assistant🧘")
st.markdown("Welcome to Yoga Assistant, your personal yoga companion. Tailored to your experience level, goals, and schedule, Yoga Assistant helps you achieve your wellness objectives, whether you're just starting out or are highly experienced one.")
st.markdown("            1) Experience level (beginner, intermediate, advanced).")
st.markdown("            2) Specific goals (flexibility, strength, relaxation, etc).")
st.markdown("            3) Amount of time you could allocate for a yoga session.")
input = st.text_input(" Please enter the above details:",placeholder=f"""Type here""")

open_ai_text_completion_model = OpenAIModel(
    api_key=st.secrets["apikey"],
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)


def generation(input):
    generator_agent = Agent(
        role="Expert YOGA INSTRUCTOR and PERSONAL TRAINER",
        prompt_persona=f"Your task is to DESIGN a CUSTOMIZED YOGA SEQUENCE and provide TIPS and MODIFICATIONS tailored to the user's experience, goals, and available time.")
    prompt = f"""
You are an Expert YOGA INSTRUCTOR and PERSONAL TRAINER. Your task is to DESIGN a CUSTOMIZED YOGA SEQUENCE and provide TIPS and MODIFICATIONS tailored to the user's experience, goals, and available time.

Here's your step-by-step guide:

1. Analyze information from the user about their YOGA EXPERIENCE level (beginner, intermediate, advanced), the user's SPECIFIC GOALS for their yoga practice (flexibility, strength, relaxation, etc) and the user to specify the AMOUNT OF TIME they have available for each yoga session.

2. Based on the information provided, CREATE a yoga sequence that MATCHES the user's skill level and goals.

3. For each POSE in the sequence, OFFER TIPS on how to perform it correctly and SAFELY.

4. PROVIDE MODIFICATIONS for each pose to accommodate different levels of flexibility or any physical limitations.

5. INCLUDE BREATHING TECHNIQUES that complement the physical practice and enhance the overall experience.

6. ENCOURAGE the user with AFFIRMATIVE directives like "do maintain even breathing" and "do focus on your alignment."

7. SUGGEST a ROUTINE for how often they should practice this sequence to achieve their goals effectively.
 """

    generator_agent_task = Task(
        name="Generation",
        model=open_ai_text_completion_model,
        agent=generator_agent,
        instructions=prompt,
        default_input=input,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
    ).execute()

    return generator_agent_task 
   
if st.button("Assist!"):
    solution = generation(input)
    st.markdown(solution)

with st.expander("ℹ️ - About this App"):
    st.markdown("""
    This app uses Lyzr Automata Agent . For any inquiries or issues, please contact Lyzr.

    """)
    st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width=True)
    st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width=True)
    st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width=True)
    st.link_button("Slack",
                   url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw',
                   use_container_width=True)