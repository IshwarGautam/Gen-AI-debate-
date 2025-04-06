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

# Load CSS Styling
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
        type_writer(pro, role="pro") 
        prev = pro

        con = generate_argument("con", topic, prev)
        type_writer(con, role="con")  
        prev = con

def type_writer(text, role, delay=0.05):
    placeholder = st.empty()
    full_text = ""

    if role == 'pro':
        background_color = '#e0ffe0' 
        alignment = 'flex-start' 
        avatar = "🟢🤖"
    else:
        background_color = '#ffe0e0' 
        alignment = 'flex-end'
        avatar = "🔴🦊"

    chat_container = f'<div class="chat-row" style="display: flex; justify-content: {alignment};">'
    chat_bubble = f'<div class="avatar">{avatar}</div><div class="chat-bubble" style="background-color:{background_color};">'
    
    for word in text.split():
        full_text += word + " "
        placeholder.markdown(
            f'{chat_container}{chat_bubble}{full_text}</div></div>',
            unsafe_allow_html=True
        )
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