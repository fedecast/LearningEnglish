import streamlit as st
import pandas as pd
import random

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

def check_answer(user_answer, correct_answer):
    """Controlla se la risposta è corretta (case-insensitive, spazi ignorati)"""
    return normalize_text(user_answer) == normalize_text(correct_answer)

def main():
    st.title("🎯 English Learning App")
    
    # Upload file
    uploaded_file = st.file_uploader(
        "📁 Carica il tuo file Excel", 
        type=['xlsx', 'xls'],
        help="File con colonne 'english' e 'italian'"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Verifica colonne
            if 'english' not in df.columns or 'italian' not in df.columns:
                st.error("❌ Il file deve avere colonne 'english' e 'italian'")
                return
            
            # Inizializza sessione
            if 'current_idx' not in st.session_state:
                st.session_state.current_idx = random.randint(0, len(df)-1)
                st.session_state.show_answer = False
                st.session_state.answer_result = None
                st.session_state.score = 0
                st.session_state.attempts = 0
                st.session_state.input_key = 0
            
            # Parola corrente
            current_word = df.iloc[st.session_state.current_idx]
            english = current_word['english']
            italian = current_word['italian']
            
            # Display parola
            st.markdown(f"""
            <div class="word-display">
                <strong>{english}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Pulsanti audio e soluzione
            col1, col2 = st.columns(2)
            
            with col1:
                # Audio usando streamlit components - più affidabile
                if st.button("🔊 Ascolta", key="audio_btn"):
                    # Genera TTS usando HTML5 Speech Synthesis
                    audio_js = f"""
                    <script>
                    function playAudio() {{
                        if ('speechSynthesis' in window) {{
                            // Ferma eventuali speech precedenti
                            speechSynthesis.cancel();
                            
                            const utterance = new SpeechSynthesisUtterance('{english}');
                            utterance.lang = 'en-US';
                            utterance.rate = 0.7;
                            utterance.volume = 1.0;
                            
                            // Aggiungi callback per debug
                            utterance.onstart = function() {{
                                console.log('Speech started');
                            }};
                            utterance.onend = function() {{
                                console.log('Speech ended');
                            }};
                            utterance.onerror = function(event) {{
                                console.error('Speech error:', event);
                            }};
                            
                            speechSynthesis.speak(utterance);
                        }} else {{
                            alert('Il tuo browser non supporta la sintesi vocale');
                        }}
                    }}
                    
                    // Chiama la funzione immediatamente
                    playAudio();
                    </script>
                    """
                    st.components.v1.html(audio_js, height=0)
            
            with col2:
                if st.button("💡 Soluzione", key="solution_btn"):
                    st.session_state.show_answer = True
            
            # Input traduzione con key dinamica per permettere reset
            user_answer = st.text_input(
                "🇮🇹 La tua traduzione (premi Invio):",
                placeholder="Scrivi qui la traduzione...",
                key=f"user_input_{st.session_state.input_key}"
            )
            
            # Verifica automatica quando l'utente inserisce del testo
            if user_answer:
                is_correct = check_answer(user_answer, italian)
                
                if is_correct:
                    st.session_state.answer_result = "correct"
                    if st.session_state.attempts == 0 or st.session_state.answer_result != "correct_already_counted":
                        st.session_state.score += 1
                        st.session_state.attempts += 1
                        st.session_state.answer_result = "correct_already_counted"
                else:
                    st.session_state.answer_result = "wrong"
            
            # Mostra risultato della verifica
            if st.session_state.answer_result == "correct" or st.session_state.answer_result == "correct_already_counted":
                st.markdown("""
                <div class="correct-answer">
                    🎉 CORRETTO! 🎉
                </div>
                """, unsafe_allow_html=True)
            
            elif st.session_state.answer_result == "wrong" and user_answer:
                st.markdown("""
                <div class="wrong-answer">
                    ❌ ERRATO - Riprova o usa 💡 Soluzione
                </div>
                """, unsafe_allow_html=True)
            
            # Mostra soluzione SOLO se richiesto esplicitamente
            if st.session_state.show_answer:
                st.info(f"💡 **{italian}**")
                
                # Incrementa tentativi solo se non già fatto per questa parola
                if st.session_state.answer_result != "correct_already_counted" and user_answer:
                    st.session_state.attempts += 1
                    st.session_state.answer_result = "solution_shown"
            
            # Pulsanti azione
            col3, col4 = st.columns(2)
            
            with col3:
                # Reset input per riprovare (solo se sbagliato)
                if st.session_state.answer_result == "wrong" and user_answer:
                    if st.button("🔄 Riprova", key="retry_btn"):
                        st.session_state.input_key += 1  # Cambia key per resettare input
                        st.session_state.answer_result = None
                        st.rerun()
            
            with col4:
                # Prossima parola - sempre disponibile
                if st.button("➡️ Prossima Parola", key="next_btn"):
                    # Incrementa attempts se non già fatto
                    if st.session_state.answer_result == "wrong" and user_answer:
                        if st.session_state.answer_result != "solution_shown":
                            st.session_state.attempts += 1
                    
                    # Reset per la prossima parola
                    st.session_state.current_idx = random.randint(0, len(df)-1)
                    st.session_state.show_answer = False
                    st.session_state.answer_result = None
                    st.session_state.input_key += 1
                    st.rerun()
            
            # Statistiche nella sidebar
            if st.session_state.attempts > 0:
                accuracy = (st.session_state.score / st.session_state.attempts) * 100
                st.sidebar.metric("🎯 Precisione", f"{accuracy:.1f}%")
                st.sidebar.metric("✅ Corrette", st.session_state.score)
                st.sidebar.metric("📊 Tentativi", st.session_state.attempts)
            
            # Reset statistiche
            if st.sidebar.button("🔄 Reset Statistiche"):
                st.session_state.score = 0
                st.session_state.attempts = 0
                st.rerun()
            
        except Exception as e:
            st.error(f"❌ Errore nel caricamento: {e}")
    
    else:
        st.info("📱 Carica un file Excel per iniziare!")
        
        with st.expander("📋 Come preparare il file Excel"):
            st.markdown("""
            1. Crea un file Excel con 2 colonne:
               - **english**: parole in inglese  
               - **italian**: traduzioni in italiano
            2. Salva il file come .xlsx
            3. Caricalo usando il pulsante sopra
            
            **Come funziona:**
            - Scrivi la traduzione e premi Invio
            - Se è ERRATO ❌, puoi cliccare "🔄 Riprova" per riprovare
            - Usa "💡 Soluzione" per vedere la risposta giusta
            - Clicca "➡️ Prossima Parola" quando vuoi andare avanti
            """)

if __name__ == "__main__":
    main()