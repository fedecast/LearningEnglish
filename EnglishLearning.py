import streamlit as st
import pandas as pd
import random
from deep_translator import GoogleTranslator

# Configurazione pagina per mobile
st.set_page_config(
    page_title="English Learning",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS per mobile
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        margin: 5px 0;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
        height: 50px;
    }
    .word-display {
        font-size: 24px;
        text-align: center;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        margin: 20px 0;
    }
    .correct-answer {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
    .wrong-answer {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def normalize_text(text):
    """Normalizza il testo per il confronto: minuscolo, senza spazi extra"""
    if not text:
        return ""
    return text.strip().lower()

def main():
    st.title("🎯 English Learning App")

    uploaded_file = st.file_uploader(
        "📁 Carica il tuo file Excel",
        type=['xlsx', 'xls'],
        help="File con una colonna: prima riga la lingua, poi le parole"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, header=None)
            if df.shape[1] != 1:
                st.error("❌ Il file deve avere UNA sola colonna")
                return

            # Prima riga: lingua
            source_lang = df.iloc[0, 0].strip().lower()
            words = df.iloc[1:, 0].dropna().tolist()

            # Lingue disponibili
            lang_options = ["english", "italian"]
            answer_lang = st.selectbox("Scegli la lingua della risposta:", lang_options, index=1 if source_lang == "english" else 0)

            # Scelta ordine parole
            order_options = ["Casuale", "Sequenziale"]
            word_order = st.selectbox("Ordine delle parole:", order_options, index=0)

            # Inizializza sessione
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = random.randint(0, len(words)-1) if word_order == "Casuale" else 0
                st.session_state.show_answer = False
                st.session_state.answer_result = None
                st.session_state.score = 0
                st.session_state.attempts = 0
                st.session_state.input_key = 0
                st.session_state.show_translation = False
                st.session_state.word_order = word_order

            # Parola corrente
            current_word = words[st.session_state.current_idx]

            st.markdown(f"""
            <div class="word-display">
                <strong>{current_word}</strong>
            </div>
            """, unsafe_allow_html=True)

            # Scegli la lingua di destinazione
            dest_lang = "en" if answer_lang == "english" else "it"
            src_lang = "en" if source_lang == "english" else "it"
            translation = GoogleTranslator(source=src_lang, target=dest_lang).translate(current_word)
            possible_answers = [normalize_text(translation)]

            # Input utente
            user_answer = st.text_input(
                f"La tua traduzione in {answer_lang} (premi Invio):",
                placeholder="Scrivi qui la traduzione...",
                key=f"user_input_{st.session_state.input_key}"
            )

            # Verifica risposta
            if user_answer:
                is_correct = normalize_text(user_answer) in possible_answers
                st.session_state.answer_result = "correct" if is_correct else "wrong"
                if is_correct:
                    st.session_state.show_translation = True

            # Mostra risultato
            if st.session_state.answer_result == "correct":
                st.markdown("""
                <div class="correct-answer">
                    🎉 CORRETTO! 🎉
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.answer_result == "wrong" and user_answer:
                st.markdown("""
                <div class="wrong-answer">
                    ❌ ERRATO - Riprova o consulta le traduzioni
                </div>
                """, unsafe_allow_html=True)

            # Mostra traduzione solo se corretta o richiesta
            if st.session_state.show_translation:
                st.info(f"💡 Traduzione trovata: {translation}")

            # Pulsanti azione
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("➡️ Prossima Parola", key="next_btn"):
                    if word_order == "Casuale":
                        st.session_state.current_idx = random.randint(0, len(words)-1)
                    else:
                        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(words)
                    st.session_state.show_answer = False
                    st.session_state.answer_result = None
                    st.session_state.input_key += 1
                    st.session_state.show_translation = False
                    st.rerun()
            with col2:
                if st.button("🔄 Riprova", key="retry_btn"):
                    st.session_state.input_key += 1
                    st.session_state.answer_result = None
                    st.rerun()
            with col3:
                if st.button("👁️ Mostra traduzione", key="show_btn"):
                    st.session_state.show_translation = True
                    st.rerun()

        except Exception as e:
            st.error(f"❌ Errore nel caricamento: {e}")

    else:
        st.info("📱 Carica un file Excel per iniziare!")
        with st.expander("📋 Come preparare il file Excel"):
            st.markdown("""
            1. Crea un file Excel con UNA sola colonna:
               - Prima riga: la lingua ("english" o "italian")
               - Righe successive: le parole
            2. Salva il file come .xlsx
            3. Caricalo usando il pulsante sopra
            """)

if __name__ == "__main__":
    main()