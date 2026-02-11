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

def handle_submit():
    guess = st.session_state.current_guess
    length = st.session_state.code_length
    if len(guess) == length and guess.isdigit():
        r, w, s = check_guess(st.session_state.secret, guess)
        st.session_state.history.append({"Guess": guess, "Right": r, "Wrong": w, "Score": s})
        if r == length:
            st.session_state.won = True
    st.session_state.current_guess = ""

# --- UI SETUP ---
st.set_page_config(page_title="Mastermind Pro", layout="wide")

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎮 Mastermind Pro")
    page = st.radio("Go to:", ["Play Game", "How to Play"])
    st.divider()
    
    if page == "Play Game":
        st.header("⚙️ Settings")
        mode = st.radio("Opponent", ["Computer", "A Friend"])
        st.session_state.code_length = st.number_input("Code Length", 3, 8, 4)
        if st.button("🆕 New Game"):
            st.session_state.history = []
            st.session_state.won = False
            st.session_state.secret = "" if mode == "A Friend" else "".join([str(random.randint(0, 9)) for _ in range(st.session_state.code_length)])
            st.rerun()

# --- INITIALIZE STATE ---
if "history" not in st.session_state: st.session_state.history = []
if "won" not in st.session_state: st.session_state.won = False
if "code_length" not in st.session_state: st.session_state.code_length = 4
if "secret" not in st.session_state: st.session_state.secret = "1234"

# --- PAGE 1: HOW TO PLAY ---
if page == "How to Play":
    st.title("📖 How to Play Mastermind")
    
    st.markdown("""
    Mastermind is a code-breaking game for two players. One player becomes the **Codebreaker**, 
    and the other becomes the **Codemaker**.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.info("### 🎯 Your Goal\nGuess the secret combination of numbers in the fewest tries possible.")
        st.write("### 🧩 The Feedback")
        st.write("**Right Place:** A digit is correct and in the correct position.")
        st.write("**Wrong Place:** A digit is correct, but it belongs in a different position.")
    
    with col2:
        st.write("### 💡 Example")
        st.code("Secret: 1 2 3 4\nGuess:  1 4 8 9")
        st.success("Result: 1 Right Place (the '1'), 1 Wrong Place (the '4')")

    

    st.markdown("---")
    st.subheader("🛠️ Using the Dashboard")
    st.write("1. **Select Mode:** Play against the AI or let a friend set the code.")
    st.write("2. **Type Fast:** Use your keyboard. Pressing **Enter** submits the guess and clears the box automatically.")
    st.write("3. **Track Trends:** Watch the performance chart. A rising line means you are getting 'warmer'!")

# --- PAGE 2: PLAY GAME ---
elif page == "Play Game":
    if not st.session_state.secret:
        st.info("👋 Waiting for the secret code...")
        secret_input = st.text_input("Friend: Enter the secret code (Hidden):", type="password")
        if st.button("Lock Code"):
            if len(secret_input) == st.session_state.code_length and secret_input.isdigit():
                st.session_state.secret = secret_input
                st.rerun()
        st.stop()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("⌨️ Guessing Area")
        if not st.session_state.won:
            st.text_input(f"Enter {st.session_state.code_length} digits:", key="current_guess", on_change=handle_submit)
        else:
            st.success(f"🏆 Victory! The code was {st.session_state.secret}")

    with col2:
        st.subheader("📊 Analytics")
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.line_chart(df["Score"])
            st.dataframe(df, use_container_width=True)
