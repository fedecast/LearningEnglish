import streamlit as st
import pandas as pd
import random
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import os
from hybrid_progress_manager import HybridProgressManager

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
    .progress-stats {
        background-color: #e8f4fd;
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 14px;
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

def text_to_speech(text, lang):
    """Genera audio dal testo usando gTTS"""
    try:
        # Determina il codice lingua per gTTS
        lang_code = 'en' if lang == 'english' else 'it'
        tts = gTTS(text=text, lang=lang_code, slow=False)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception as e:
        st.error(f"Errore nella generazione audio: {e}")
        return None

def main():
    st.title("🎯 English Learning App")

    # --- Selettore file dalla cartella Files ---
    files_dir = "Files"
    excel_files = [f for f in os.listdir(files_dir) if f.endswith(('.xlsx', '.xls'))]
    selected_file = st.selectbox("📂 Scegli un file dalla cartella Files:", [""] + excel_files)

    # --- Caricamento manuale ---
    uploaded_file = st.file_uploader(
        "📁 Carica il tuo file Excel",
        type=['xlsx', 'xls'],
        help="File con una colonna: prima riga la lingua, poi le parole"
    )

    # --- Scegli il file da usare ---
    file_to_use = None
    if selected_file:
        file_to_use = os.path.join(files_dir, selected_file)
    elif uploaded_file is not None:
        file_to_use = uploaded_file

    if file_to_use:
        try:
            # Se file_to_use è un path, apri con open; se è UploadedFile, passa direttamente
            if isinstance(file_to_use, str):
                df = pd.read_excel(file_to_use, header=None)
            else:
                df = pd.read_excel(file_to_use, header=None)
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

            # Inizializza il gestore del progresso
            if 'progress_manager' not in st.session_state or st.session_state.get('current_file') != selected_file:
                file_name = selected_file if selected_file else "uploaded_file.xlsx"
                st.session_state.progress_manager = HybridProgressManager(file_name)
                st.session_state.current_file = selected_file

            progress_manager = st.session_state.progress_manager

            # Mostra info backend (solo per debug/info)
            backend_info = progress_manager.get_backend_info()
            with st.expander("ℹ️ Info Storage", expanded=False):
                st.json(backend_info)

            # Mostra statistiche generali
            total_stats = progress_manager.get_total_stats()
            if total_stats['total_attempts'] > 0:
                st.markdown(f"""
                <div class="progress-stats">
                    📊 <strong>Statistiche:</strong> {total_stats['total_words_practiced']} parole praticate • 
                    {total_stats['total_correct']} corrette • {total_stats['total_wrong']} errate • 
                    Precisione: {total_stats['accuracy_percentage']}%
                </div>
                """, unsafe_allow_html=True)

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
            
            # Ottieni statistiche per la parola corrente
            correct_count, wrong_count = progress_manager.get_word_stats(current_word)
            word_attempts = correct_count + wrong_count

            st.markdown(f"""
            <div class="word-display">
                <strong>{current_word}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostra statistiche della parola se ci sono tentativi precedenti
            if word_attempts > 0:
                st.markdown(f"""
                <div class="progress-stats">
                    📈 Questa parola: ✅ {correct_count} • ❌ {wrong_count} • Tentativi: {word_attempts}
                </div>
                """, unsafe_allow_html=True)
            
            # Pulsante per ascoltare la parola
            if st.button("🔊 Ascolta", key="listen_btn"):
                audio_bytes = text_to_speech(current_word, source_lang)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3')

            # Scegli la lingua di destinazione
            dest_lang = "en" if answer_lang == "english" else "it"
            src_lang = "en" if source_lang == "english" else "it"
            try:
                translation = GoogleTranslator(source=src_lang, target=dest_lang).translate(current_word)
            except Exception as e:
                st.warning(f"⚠️ Impossibile ottenere la traduzione online. Usa 'Mostra traduzione' per vedere la risposta corretta.")
                translation = current_word  # Fallback
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
                
                # Registra la risposta nel sistema di progresso
                progress_manager.record_answer(current_word, is_correct)
                
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
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬅️ Precedente", key="prev_btn"):
                    if word_order == "Casuale":
                        st.session_state.current_idx = random.randint(0, len(words)-1)
                    else:
                        st.session_state.current_idx = (st.session_state.current_idx - 1) % len(words)
                    st.session_state.show_answer = False
                    st.session_state.answer_result = None
                    st.session_state.input_key += 1
                    st.session_state.show_translation = False
                    st.rerun()
            with col2:
                if st.button("➡️ Prossima", key="next_btn"):
                    if word_order == "Casuale":
                        st.session_state.current_idx = random.randint(0, len(words)-1)
                    else:
                        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(words)
                    st.session_state.show_answer = False
                    st.session_state.answer_result = None
                    st.session_state.input_key += 1
                    st.session_state.show_translation = False
                    st.rerun()
            
            col3, col4, col5 = st.columns(3)
            with col3:
                if st.button("🔄 Riprova", key="retry_btn"):
                    st.session_state.input_key += 1
                    st.session_state.answer_result = None
                    st.rerun()
            with col4:
                if st.button("👁️ Mostra traduzione", key="show_btn"):
                    st.session_state.show_translation = True
                    st.rerun()
            with col5:
                if st.button("🔁 Reinizia", key="restart_btn"):
                    if word_order == "Casuale":
                        st.session_state.current_idx = random.randint(0, len(words)-1)
                    else:
                        st.session_state.current_idx = 0
                    st.session_state.show_answer = False
                    st.session_state.answer_result = None
                    st.session_state.input_key += 1
                    st.session_state.show_translation = False
                    st.rerun()

            # Sezione statistiche avanzate (in expander)
            with st.expander("📊 Statistiche Avanzate"):
                if total_stats['total_attempts'] > 0:
                    col_stat1, col_stat2 = st.columns(2)
                    
                    with col_stat1:
                        st.metric("Parole Praticate", total_stats['total_words_practiced'])
                        st.metric("Risposte Corrette", total_stats['total_correct'])
                    
                    with col_stat2:
                        st.metric("Risposte Errate", total_stats['total_wrong'])
                        st.metric("Precisione", f"{total_stats['accuracy_percentage']}%")
                    
                    # Parole difficili
                    difficult_words = progress_manager.get_difficult_words()
                    if difficult_words:
                        st.subheader("🔴 Parole da ripassare")
                        for i, word_data in enumerate(difficult_words[:5]):  # Top 5
                            error_rate = word_data['error_rate'] * 100
                            st.write(f"{i+1}. **{word_data['word']}** - "
                                   f"Errori: {error_rate:.1f}% "
                                   f"({word_data['wrong']}/{word_data['correct']+word_data['wrong']})")
                    
                    # Pulsante reset progresso
                    if st.button("🔄 Reset Progresso Completo", type="secondary"):
                        progress_manager.reset_all_progress()
                        st.success("Progresso resettato!")
                        st.rerun()
                else:
                    st.info("Inizia a praticare per vedere le statistiche!")

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