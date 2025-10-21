"""
Database Manager per il deployment cloud con Supabase.
Gestisce il progresso dell'utente utilizzando un database PostgreSQL remoto.
"""

import os
import json
from typing import Dict, Tuple, Optional
import streamlit as st

# Import condizionale per non bloccare l'app locale se non c'è supabase
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class DatabaseManager:
    def __init__(self, file_name: str, user_id: Optional[str] = None):
        """
        Inizializza il gestore database cloud.
        
        Args:
            file_name: Nome del file Excel (es. "Words.xlsx")
            user_id: ID utente unico (se None, usa session state)
        """
        self.file_name = file_name
        self.user_id = user_id or self._get_user_id()
        self.supabase_client = None
        self.is_cloud_enabled = False
        
        # Tenta di inizializzare Supabase
        self._init_supabase()
    
    def _get_user_id(self) -> str:
        """Genera o recupera un ID utente univoco dalla sessione."""
        if 'user_id' not in st.session_state:
            import uuid
            st.session_state.user_id = str(uuid.uuid4())
        return st.session_state.user_id
    
    def _init_supabase(self):
        """Inizializza la connessione a Supabase se le credenziali sono disponibili."""
        try:
            # Prova a leggere le credenziali da secrets o variabili d'ambiente
            supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
            
            if supabase_url and supabase_key and SUPABASE_AVAILABLE:
                self.supabase_client = create_client(supabase_url, supabase_key)
                self.is_cloud_enabled = True
                self._ensure_table_exists()
            else:
                self.is_cloud_enabled = False
        except Exception as e:
            st.warning(f"Database cloud non disponibile, usando Session State locale: {e}")
            self.is_cloud_enabled = False
    
    def _ensure_table_exists(self):
        """Crea la tabella se non esiste (solo per demo - in produzione usare migrations)."""
        if not self.supabase_client:
            return
        
        try:
            # Verifica se la tabella esiste provando a fare una query
            self.supabase_client.table("progress").select("*").limit(1).execute()
        except Exception:
            # Se la query fallisce, probabilmente la tabella non esiste
            # In un deployment reale, useresti le migrations di Supabase
            pass
    
    def _get_progress_from_cloud(self) -> Dict[str, Dict[str, int]]:
        """Carica il progresso dal database cloud."""
        if not self.is_cloud_enabled:
            return {}
        
        try:
            response = self.supabase_client.table("progress").select("*").eq(
                "user_id", self.user_id
            ).eq("file_name", self.file_name).execute()
            
            if response.data:
                # Converte i record del database in formato dictionary
                progress = {}
                for record in response.data:
                    word = record["word"].lower().strip()
                    progress[word] = {
                        "correct": record["correct_count"],
                        "wrong": record["wrong_count"]
                    }
                return progress
            return {}
        except Exception as e:
            st.error(f"Errore nel caricamento dal database: {e}")
            return {}
    
    def _save_progress_to_cloud(self, word: str, correct: int, wrong: int):
        """Salva o aggiorna il progresso nel database cloud."""
        if not self.is_cloud_enabled:
            return
        
        try:
            # Controlla se esiste già un record per questa parola
            existing = self.supabase_client.table("progress").select("*").eq(
                "user_id", self.user_id
            ).eq("file_name", self.file_name).eq("word", word.lower().strip()).execute()
            
            data = {
                "user_id": self.user_id,
                "file_name": self.file_name,
                "word": word.lower().strip(),
                "correct_count": correct,
                "wrong_count": wrong
            }
            
            if existing.data:
                # Aggiorna record esistente
                self.supabase_client.table("progress").update(data).eq(
                    "user_id", self.user_id
                ).eq("file_name", self.file_name).eq("word", word.lower().strip()).execute()
            else:
                # Inserisci nuovo record
                self.supabase_client.table("progress").insert(data).execute()
                
        except Exception as e:
            st.error(f"Errore nel salvataggio sul database: {e}")
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """
        Ottiene le statistiche per una parola.
        
        Args:
            word: La parola da controllare
            
        Returns:
            Tupla (risposte_corrette, risposte_errate)
        """
        if self.is_cloud_enabled:
            progress = self._get_progress_from_cloud()
        else:
            # Fallback a session state per uso locale
            if 'local_progress' not in st.session_state:
                st.session_state.local_progress = {}
            progress = st.session_state.local_progress.get(self.file_name, {})
        
        word_lower = word.lower().strip()
        if word_lower in progress:
            stats = progress[word_lower]
            return stats.get('correct', 0), stats.get('wrong', 0)
        return 0, 0
    
    def record_answer(self, word: str, is_correct: bool):
        """
        Registra una risposta per una parola.
        
        Args:
            word: La parola per cui registrare la risposta
            is_correct: True se la risposta è corretta, False altrimenti
        """
        word_lower = word.lower().strip()
        
        if self.is_cloud_enabled:
            # Ottieni stats attuali e aggiorna
            correct, wrong = self.get_word_stats(word)
            if is_correct:
                correct += 1
            else:
                wrong += 1
            self._save_progress_to_cloud(word_lower, correct, wrong)
        else:
            # Fallback a session state per uso locale
            if 'local_progress' not in st.session_state:
                st.session_state.local_progress = {}
            if self.file_name not in st.session_state.local_progress:
                st.session_state.local_progress[self.file_name] = {}
            
            if word_lower not in st.session_state.local_progress[self.file_name]:
                st.session_state.local_progress[self.file_name][word_lower] = {'correct': 0, 'wrong': 0}
            
            if is_correct:
                st.session_state.local_progress[self.file_name][word_lower]['correct'] += 1
            else:
                st.session_state.local_progress[self.file_name][word_lower]['wrong'] += 1
    
    def get_total_stats(self) -> Dict[str, int]:
        """Ottiene le statistiche totali."""
        if self.is_cloud_enabled:
            progress = self._get_progress_from_cloud()
        else:
            if 'local_progress' not in st.session_state:
                st.session_state.local_progress = {}
            progress = st.session_state.local_progress.get(self.file_name, {})
        
        total_correct = sum(stats.get('correct', 0) for stats in progress.values())
        total_wrong = sum(stats.get('wrong', 0) for stats in progress.values())
        total_words = len(progress)
        total_attempts = total_correct + total_wrong
        
        accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            'total_words_practiced': total_words,
            'total_correct': total_correct,
            'total_wrong': total_wrong,
            'total_attempts': total_attempts,
            'accuracy_percentage': round(accuracy, 1)
        }
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        """Ottiene le parole più difficili."""
        if self.is_cloud_enabled:
            progress = self._get_progress_from_cloud()
        else:
            if 'local_progress' not in st.session_state:
                st.session_state.local_progress = {}
            progress = st.session_state.local_progress.get(self.file_name, {})
        
        difficult_words = []
        
        for word, stats in progress.items():
            correct = stats.get('correct', 0)
            wrong = stats.get('wrong', 0)
            total = correct + wrong
            
            if total >= min_attempts and wrong > correct:
                error_rate = wrong / total
                difficult_words.append({
                    'word': word,
                    'correct': correct,
                    'wrong': wrong,
                    'error_rate': error_rate
                })
        
        difficult_words.sort(key=lambda x: x['error_rate'], reverse=True)
        return difficult_words
    
    def reset_all_progress(self):
        """Reset di tutto il progresso."""
        if self.is_cloud_enabled:
            try:
                self.supabase_client.table("progress").delete().eq(
                    "user_id", self.user_id
                ).eq("file_name", self.file_name).execute()
            except Exception as e:
                st.error(f"Errore nel reset del database: {e}")
        else:
            if 'local_progress' in st.session_state and self.file_name in st.session_state.local_progress:
                del st.session_state.local_progress[self.file_name]
    
    def get_status_info(self) -> Dict[str, str]:
        """Restituisce informazioni sullo stato del database."""
        return {
            "storage_type": "Database Cloud (Supabase)" if self.is_cloud_enabled else "Session State Locale",
            "is_persistent": "Sì" if self.is_cloud_enabled else "No (solo durante la sessione)",
            "user_id": self.user_id[:8] + "..." if self.user_id else "N/A"
        }