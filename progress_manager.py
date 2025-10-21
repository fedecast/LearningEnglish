"""
Modulo per gestire il progresso dell'utente nell'apprendimento delle parole.
Salva i dati localmente senza modificare i file originali su Git.
"""

import json
import os
from typing import Dict, Tuple

class ProgressManager:
    def __init__(self, file_name: str):
        """
        Inizializza il gestore del progresso per un file specifico.
        
        Args:
            file_name: Nome del file Excel (es. "Words.xlsx")
        """
        self.file_name = file_name
        self.progress_dir = "UserData"
        self.progress_file = os.path.join(
            self.progress_dir, 
            f"{os.path.splitext(file_name)[0]}_progress.json"
        )
        
        # Crea la directory se non esiste
        os.makedirs(self.progress_dir, exist_ok=True)
        
        # Carica il progresso esistente
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict[str, Dict[str, int]]:
        """Carica il progresso dal file JSON."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_progress(self):
        """Salva il progresso nel file JSON."""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """
        Ottiene le statistiche per una parola.
        
        Args:
            word: La parola da controllare
            
        Returns:
            Tupla (risposte_corrette, risposte_errate)
        """
        word_lower = word.lower().strip()
        if word_lower in self.progress:
            stats = self.progress[word_lower]
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
        
        if word_lower not in self.progress:
            self.progress[word_lower] = {'correct': 0, 'wrong': 0}
        
        if is_correct:
            self.progress[word_lower]['correct'] += 1
        else:
            self.progress[word_lower]['wrong'] += 1
        
        self._save_progress()
    
    def get_total_stats(self) -> Dict[str, int]:
        """
        Ottiene le statistiche totali di tutti i progressi.
        
        Returns:
            Dizionario con le statistiche totali
        """
        total_correct = sum(stats.get('correct', 0) for stats in self.progress.values())
        total_wrong = sum(stats.get('wrong', 0) for stats in self.progress.values())
        total_words = len(self.progress)
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
        """
        Ottiene le parole più difficili (con più errori che risposte corrette).
        
        Args:
            min_attempts: Numero minimo di tentativi per considerare una parola
            
        Returns:
            Lista di parole difficili ordinate per rapporto errori/totale
        """
        difficult_words = []
        
        for word, stats in self.progress.items():
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
        
        # Ordina per tasso di errore decrescente
        difficult_words.sort(key=lambda x: x['error_rate'], reverse=True)
        return difficult_words
    
    def reset_word_progress(self, word: str):
        """Reset del progresso per una specifica parola."""
        word_lower = word.lower().strip()
        if word_lower in self.progress:
            del self.progress[word_lower]
            self._save_progress()
    
    def reset_all_progress(self):
        """Reset di tutto il progresso."""
        self.progress = {}
        self._save_progress()