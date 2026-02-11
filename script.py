import streamlit as st
import random
import pandas as pd


# --- GAME LOGIC ---
def check_guess(secret, guess):
    right_place = sum(s == g for s, g in zip(secret, guess))
    from collections import Counter
    common = sum((Counter(secret) & Counter(guess)).values())
    wrong_place = common - right_place
    score = (right_place * 2) + wrong_place
    return right_place, wrong_place, score


# --- CALLBACK FOR ENTER KEY ---
def handle_submit():
    guess = st.session_state.current_guess
    length = st.session_state.code_length

    if len(guess) == length and guess.isdigit():
        r, w, s = check_guess(st.session_state.secret, guess)
        st.session_state.history.append({"Guess": guess, "Right": r, "Wrong": w, "Score": s})
        if r == length:
            st.session_state.won = True

    # Clear input for next turn
    st.session_state.current_guess = ""


# --- UI SETUP ---
st.set_page_config(page_title="Mastermind Pro", layout="wide")
st.title("🎯 Mastermind: Multi-Mode Dashboard")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "won" not in st.session_state:
    st.session_state.won = False
if "code_length" not in st.session_state:
    st.session_state.code_length = 4
if "secret" not in st.session_state:
    st.session_state.secret = ""

# --- SIDEBAR (Mode Selection) ---
with st.sidebar:
    st.header("⚙️ Game Setup")
    mode = st.radio("Who sets the number?", ["Computer", "A Friend"])
    st.session_state.code_length = st.number_input("Code Length", 3, 8, 4)

    if st.button("🆕 Start New Game"):
        st.session_state.history = []
        st.session_state.won = False
        if mode == "Computer":
            st.session_state.secret = "".join([str(random.randint(0, 9)) for _ in range(st.session_state.code_length)])
        else:
            st.session_state.secret = ""  # Reset for manual entry
        st.rerun()

# --- MODE 2: MANUAL SETUP ---
if not st.session_state.secret:
    st.info("👋 Waiting for the secret code to be set...")
    with st.container():
        secret_input = st.text_input("Friend: Enter the secret code here (Hidden):", type="password")
        if st.button("Lock Code & Start"):
            if len(secret_input) == st.session_state.code_length and secret_input.isdigit():
                st.session_state.secret = secret_input
                st.rerun()
            else:
                st.error(f"Error: Secret must be {st.session_state.code_length} digits.")
    st.stop()  # Don't show the game until the code is set

# --- MAIN GAME DASHBOARD ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⌨️ Guessing Area")
    if not st.session_state.won:
        st.text_input(
            f"Enter {st.session_state.code_length} digits:",
            key="current_guess",
            on_change=handle_submit
        )
        st.caption("Press ENTER to submit instantly.")
    else:
        st.success(f"🏆 Victory! The code was {st.session_state.secret}")
        if st.button("Play Again"):
            st.session_state.history = []
            st.session_state.won = False
            st.session_state.secret = ""  # Triggers fresh setup
            st.rerun()

with col2:
    st.subheader("📊 Analytics")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.line_chart(df["Score"])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No data yet. Make your first guess!")