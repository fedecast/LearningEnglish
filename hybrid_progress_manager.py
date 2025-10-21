"""
Manager ibrido che supporta sia storage locale che cloud.
Si adatta automaticamente all'ambiente di esecuzione.
"""

import os
import streamlit as st
from typing import Dict, Tuple

# Import condizionali
try:
    from database_manager import DatabaseManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

try:
    from progress_manager import ProgressManager as LocalProgressManager
    LOCAL_AVAILABLE = True
except ImportError:
    LOCAL_AVAILABLE = False

class HybridProgressManager:
    """
    Manager che sceglie automaticamente tra storage locale e cloud.
    
    Priorità:
    1. Se in cloud con Supabase configurato → Database cloud
    2. Se locale → File JSON locali  
    3. Fallback → Session State
    """
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.backend = None
        self.backend_type = "unknown"
        
        # Inizializza il backend appropriato
        self._init_backend()
    
    def _init_backend(self):
        """Seleziona e inizializza il backend di storage appropriato."""
        
        # 1. Prova Database Cloud (per deployment)
        if DATABASE_AVAILABLE and self._is_cloud_deployment():
            try:
                self.backend = DatabaseManager(self.file_name)
                if self.backend.is_cloud_enabled:
                    self.backend_type = "cloud_database"
                    return
            except Exception as e:
                st.warning(f"Fallback da database cloud: {e}")
        
        # 2. Prova Storage Locale (per sviluppo)
        if LOCAL_AVAILABLE and not self._is_cloud_deployment():
            try:
                self.backend = LocalProgressManager(self.file_name)
                self.backend_type = "local_files"
                return
            except Exception as e:
                st.warning(f"Fallback da storage locale: {e}")
        
        # 3. Fallback a Session State
        self.backend = SessionStateManager(self.file_name)
        self.backend_type = "session_state"
    
    def _is_cloud_deployment(self) -> bool:
        """Rileva se l'app è deployata su cloud."""
        # Indicatori di deployment cloud
        try:
            cloud_indicators = [
                os.getenv("STREAMLIT_SHARING"),  # Streamlit Sharing
                hasattr(st, 'secrets') and "SUPABASE_URL" in st.secrets,
                "streamlit.app" in os.getenv("HOSTNAME", ""),
                os.getenv("STREAMLIT_SERVER_HEADLESS") == "true"
            ]
            return any(cloud_indicators)
        except Exception:
            # Se c'è un errore nell'accesso ai secrets, assumiamo sia locale
            return False
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """Delega al backend attivo."""
        return self.backend.get_word_stats(word)
    
    def record_answer(self, word: str, is_correct: bool):
        """Delega al backend attivo."""
        return self.backend.record_answer(word, is_correct)
    
    def get_total_stats(self) -> Dict[str, int]:
        """Delega al backend attivo."""
        return self.backend.get_total_stats()
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        """Delega al backend attivo."""
        return self.backend.get_difficult_words(min_attempts)
    
    def reset_all_progress(self):
        """Delega al backend attivo."""
        return self.backend.reset_all_progress()
    
    def get_backend_info(self) -> Dict[str, str]:
        """Restituisce informazioni sul backend attivo."""
        base_info = {
            "backend_type": self.backend_type,
            "file_name": self.file_name
        }
        
        # Aggiungi info specifiche del backend se disponibili
        if hasattr(self.backend, 'get_status_info'):
            base_info.update(self.backend.get_status_info())
        
        return base_info

class SessionStateManager:
    """Fallback manager che usa solo Streamlit Session State."""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.storage_key = f"progress_{file_name}"
        
        if self.storage_key not in st.session_state:
            st.session_state[self.storage_key] = {}
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        word_lower = word.lower().strip()
        progress = st.session_state[self.storage_key]
        
        if word_lower in progress:
            stats = progress[word_lower]
            return stats.get('correct', 0), stats.get('wrong', 0)
        return 0, 0
    
    def record_answer(self, word: str, is_correct: bool):
        word_lower = word.lower().strip()
        progress = st.session_state[self.storage_key]
        
        if word_lower not in progress:
            progress[word_lower] = {'correct': 0, 'wrong': 0}
        
        if is_correct:
            progress[word_lower]['correct'] += 1
        else:
            progress[word_lower]['wrong'] += 1
    
    def get_total_stats(self) -> Dict[str, int]:
        progress = st.session_state[self.storage_key]
        
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
        progress = st.session_state[self.storage_key]
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
        st.session_state[self.storage_key] = {}
    
    def get_status_info(self) -> Dict[str, str]:
        return {
            "storage_type": "Session State",
            "is_persistent": "No (perso al refresh)",
            "storage_key": self.storage_key
        }