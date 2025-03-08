import streamlit as st
import pandas as pd
import time

# Load the questions from df.csv
@st.cache_data
def load_questions():
    return pd.read_csv("data/real_episode_data.csv")

df = load_questions()

# Initialize session state variables
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "waiting_for_answer" not in st.session_state:
    st.session_state.waiting_for_answer = False
if "buzz_pressed" not in st.session_state:
    st.session_state.buzz_pressed = False

# Function to handle the buzzer press
def press_buzzer():
    if not st.session_state.waiting_for_answer:
        st.session_state.buzz_pressed = True
        st.session_state.waiting_for_answer = True
        time.sleep(3)  # Wait 3 seconds
        st.session_state.show_answer = True
        st.session_state.waiting_for_answer = False

# Function to move to the next question
def next_question():
    st.session_state.show_answer = False
    st.session_state.buzz_pressed = False
    st.session_state.current_index = (st.session_state.current_index + 1) % len(df)

# Get current question
category = df.iloc[st.session_state.current_index]['category']
question = df.iloc[st.session_state.current_index]['puzzle_front']
answer = df.iloc[st.session_state.current_index]['puzzle_back']

# UI Layout
st.title("🔔 Buzzer Quiz Game")

st.subheader(f"**Category:** {category}")
st.write(f"**Question:** {question}")

# Buzzer Button (only enabled if not waiting for answer)
if st.button("🔴 Press to Buzz", disabled=st.session_state.waiting_for_answer):
    press_buzzer()

# Show answer after 3 seconds
if st.session_state.show_answer:
    st.write(f"**Answer:** {answer}")
    st.button("➡️ Next", on_click=next_question)  # Show "Next" button after answer appears
else:
    st.write("**Answer:** ⏳ (Revealed 3 seconds after buzzing...)")
