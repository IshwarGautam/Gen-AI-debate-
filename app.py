# pip install openai streamlit python-dotenv
import os
import time
import openai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="AI Debate Bot", page_icon="🤖")

# Title and description
st.title("🧠 AI Debate Bot")
st.write("Enter a topic below and let two AI bots argue it out!")

# Generate Argument
def generate_argument(role, topic, prev_response):
    prompt = f"""
    You are a skilled debater on the {'PRO' if role == 'pro' else 'CON'} side of the topic: "{topic}". 
    {'Your opponent said: ' + prev_response if prev_response else ''} 
    Reply with a strong, persuasive, and respectful argument (max 1 sentence).
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_debate(topic, rounds):
    prev = None
    for i in range(rounds):
        st.markdown(f"### 🔁 Round {i + 1}")

        pro = generate_argument("pro", topic, prev)
        type_writer(f"PRO: {pro}") 
        prev = pro

        con = generate_argument("con", topic, prev)
        type_writer(f"CON: {con}")  
        prev = con

def type_writer(text, delay=0.05):
    placeholder = st.empty()
    full_text = ""
    
    for word in text.split():
        full_text += word + " "
        placeholder.markdown(full_text)
        time.sleep(delay)
    return full_text.strip()

def main():
    # Get user input
    topic = st.text_input("🎯 Debate Topic", "Gen AI is important topic for student.")
    rounds = st.slider("🌀 Number of Debate Rounds", 1, 5, 2)

    if st.button("🗣️ Start Debate") and topic:
        generate_debate(topic, rounds)

if __name__ == "__main__":
    # streamlit run app.py
    main()