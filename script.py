import streamlit as st
import random

# --- LOGIQUE DE JEU ---
def check_guess(secret, guess):
    right_place = sum(s == g for s, g in zip(secret, guess))
    from collections import Counter
    common = sum((Counter(secret) & Counter(guess)).values())
    wrong_place = common - right_place
    return right_place, wrong_place

def handle_submit():
    guess = st.session_state.current_guess
    length = st.session_state.code_length
    if len(guess) == length and guess.isdigit():
        r, w = check_guess(st.session_state.secret, guess)
        # On ajoute le résultat en haut de la liste pour la lisibilité
        st.session_state.history.insert(0, {"Essai": len(st.session_state.history) + 1, "Devinette": guess, "Bien placés": r, "Mal placés": w})
        if r == length:
            st.session_state.won = True
    st.session_state.current_guess = ""

# --- CONFIGURATION UI ---
st.set_page_config(page_title="Mastermind Simple", layout="centered")

# --- INITIALISATION ---
if "history" not in st.session_state: st.session_state.history = []
if "won" not in st.session_state: st.session_state.won = False
if "code_length" not in st.session_state: st.session_state.code_length = 4
if "secret" not in st.session_state: st.session_state.secret = "".join([str(random.randint(0, 9)) for _ in range(4)])

# --- BARRE LATÉRALE (NAVIGATION & SETTINGS) ---
with st.sidebar:
    st.title("🎮 Mastermind")
    page = st.radio("Menu", ["Jouer", "Règles"])
    st.divider()
    if page == "Jouer":
        mode = st.radio("Mode", ["Ordinateur", "Ami"])
        st.session_state.code_length = st.number_input("Longueur du code", 3, 6, 4)
        if st.button("🔄 Nouvelle Partie"):
            st.session_state.history = []
            st.session_state.won = False
            st.session_state.secret = "" if mode == "Ami" else "".join([str(random.randint(0, 9)) for _ in range(st.session_state.code_length)])
            st.rerun()

# --- PAGE : RÈGLES ---
if page == "Règles":
    st.header("📖 Règles du jeu")
    st.write("""
    - **But** : Deviner le code secret en un minimum d'essais.
    - **Bien placés** : Chiffres corrects à la bonne position.
    - **Mal placés** : Chiffres corrects mais à la mauvaise position.
    """)
    st.info("Astuce : Tapez votre code et appuyez sur **Entrée** pour valider instantanément.")

# --- PAGE : JOUER ---
else:
    # Cas du mode "Ami" (définition du code secret)
    if not st.session_state.secret:
        st.subheader("🔐 Définition du code")
        secret_input = st.text_input("Entrez le code secret (masqué) :", type="password")
        if st.button("Valider le code"):
            if len(secret_input) == st.session_state.code_length and secret_input.isdigit():
                st.session_state.secret = secret_input
                st.rerun()
        st.stop()

    # Dashboard de jeu
    st.header("🎯 Devinez le code")
    
    # Affichage des stats en colonnes
    col_a, col_b = st.columns(2)
    col_a.metric("Nombre d'essais", len(st.session_state.history))
    if st.session_state.history:
        dernier = st.session_state.history[0]
        col_b.metric("Dernier score", f"{dernier['Bien placés']} BP / {dernier['Mal placés']} MP")

    st.divider()

    # Zone de saisie
    if not st.session_state.won:
        st.text_input(f"Entrez {st.session_state.code_length} chiffres :", key="current_guess", on_change=handle_submit)
    else:
        st.success(f"🎊 Bravo ! Vous avez trouvé le code : {st.session_state.secret}")
        if st.button("Rejouer"):
            st.session_state.history = []
            st.session_state.won = False
            st.session_state.secret = ""
            st.rerun()

    # Historique simple
    if st.session_state.history:
        st.subheader("📜 Historique")
        st.table(st.session_state.history)
