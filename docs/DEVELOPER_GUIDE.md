# 👨‍💻 Guida Sviluppatore - English Learning App

Documentazione tecnica per sviluppatori che vogliono contribuire o estendere il progetto.

## Indice

- [Setup Ambiente](#setup-ambiente)
- [Architettura Codice](#architettura-codice)
- [API Reference](#api-reference)
- [Estendere il Sistema](#estendere-il-sistema)
- [Testing](#testing)
- [Best Practices](#best-practices)
- [Contribuire](#contribuire)

## Setup Ambiente

### Prerequisiti

```bash
# Versioni richieste
Python >= 3.8
pip >= 21.0
git >= 2.0
```

### Installazione Sviluppo

```bash
# 1. Clone repository
git clone https://github.com/fedecast/LearningEnglish.git
cd LearningEnglish

# 2. Virtual environment
python -m venv venv

# Attiva (Linux/Mac)
source venv/bin/activate

# Attiva (Windows)
venv\Scripts\activate

# 3. Installa dipendenze development
pip install -r requirements.txt
pip install -r requirements-cloud.txt  # Opzionale

# 4. Installa dev tools (opzionale)
pip install black flake8 mypy pytest

# 5. Verifica installazione
python -c "import streamlit; print(streamlit.__version__)"
```

### Struttura Directory

```
LearningEnglish/
├── EnglishLearning.py          # App principale
├── hybrid_progress_manager.py  # Orchestratore backend
├── progress_manager.py         # Backend locale
├── database_manager.py         # Backend cloud
├── main.py                     # Entry point alternativo
│
├── Files/                      # Excel files libreria
├── UserData/                   # Dati utente (gitignored)
├── docs/                       # Documentazione
│   ├── ARCHITECTURE.md
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
│
├── .streamlit/
│   └── secrets.toml.example    # Template secrets
│
├── requirements.txt            # Dipendenze base
├── requirements-cloud.txt      # Dipendenze cloud
├── requirements-base.txt       # Dipendenze minime
│
├── DEPLOYMENT.md               # Guida deployment
├── PROGRESS_SYSTEM.md          # Docs sistema progresso
├── README.md                   # Documentazione principale
└── .gitignore
```

## Architettura Codice

### Moduli Principali

#### 1. EnglishLearning.py (335 LOC)

**Responsabilità:** UI e logica applicativa

**Funzioni Principali:**

```python
def main():
    """Entry point applicazione Streamlit"""
    # Setup UI
    # Load file Excel
    # Init progress manager
    # Quiz loop
    # Display stats

def normalize_text(text: str) -> str:
    """
    Normalizza testo per confronto.
    
    Args:
        text: Testo da normalizzare
        
    Returns:
        Testo lowercase e senza spazi extra
    """
    if not text:
        return ""
    return text.strip().lower()

def text_to_speech(text: str, lang: str) -> BytesIO:
    """
    Genera audio da testo usando gTTS.
    
    Args:
        text: Testo da convertire
        lang: Codice lingua ("english"/"italian")
        
    Returns:
        BytesIO con audio MP3
    """
    lang_code = 'en' if lang == 'english' else 'it'
    tts = gTTS(text=text, lang=lang_code, slow=False)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes
```

**Session State Keys:**

```python
st.session_state = {
    'progress_manager': HybridProgressManager,  # Manager attivo
    'current_file': str,                        # Nome file corrente
    'current_idx': int,                         # Indice parola
    'show_answer': bool,                        # Flag mostra risposta
    'answer_result': Optional[str],             # "correct"/"wrong"
    'input_key': int,                           # Counter per re-render
    'show_translation': bool,                   # Flag traduzione visibile
    'word_order': str                           # "Casuale"/"Sequenziale"
}
```

#### 2. hybrid_progress_manager.py (193 LOC)

**Responsabilità:** Pattern Strategy per backend selection

**Classes:**

```python
class HybridProgressManager:
    """
    Orchestratore che seleziona e delega al backend appropriato.
    
    Attributes:
        file_name (str): Nome file Excel
        backend: Istanza backend attivo
        backend_type (str): Tipo backend ("cloud_database"/"local_files"/"session_state")
    """
    
    def __init__(self, file_name: str):
        """Inizializza e seleziona backend"""
        self.file_name = file_name
        self._init_backend()
    
    def _init_backend(self):
        """Seleziona backend in base a ambiente"""
        # 1. Cloud Database (se disponibile)
        if self._is_cloud_deployment() and DATABASE_AVAILABLE:
            try:
                self.backend = DatabaseManager(self.file_name)
                if self.backend.is_cloud_enabled:
                    self.backend_type = "cloud_database"
                    return
            except Exception as e:
                st.warning(f"Fallback: {e}")
        
        # 2. Local Files
        if LOCAL_AVAILABLE and not self._is_cloud_deployment():
            try:
                self.backend = LocalProgressManager(self.file_name)
                self.backend_type = "local_files"
                return
            except Exception as e:
                st.warning(f"Fallback: {e}")
        
        # 3. Session State (sempre disponibile)
        self.backend = SessionStateManager(self.file_name)
        self.backend_type = "session_state"
    
    def _is_cloud_deployment(self) -> bool:
        """Rileva se app è su cloud"""
        indicators = [
            os.getenv("STREAMLIT_SHARING"),
            hasattr(st, 'secrets') and "SUPABASE_URL" in st.secrets,
            "streamlit.app" in os.getenv("HOSTNAME", ""),
            os.getenv("STREAMLIT_SERVER_HEADLESS") == "true"
        ]
        return any(indicators)
    
    # Metodi delegati
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        return self.backend.get_word_stats(word)
    
    def record_answer(self, word: str, is_correct: bool):
        return self.backend.record_answer(word, is_correct)
    
    def get_total_stats(self) -> Dict[str, int]:
        return self.backend.get_total_stats()
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        return self.backend.get_difficult_words(min_attempts)
    
    def reset_all_progress(self):
        return self.backend.reset_all_progress()
    
    def get_backend_info(self) -> Dict[str, str]:
        """Info sul backend attivo"""
        return {
            "backend_type": self.backend_type,
            "file_name": self.file_name,
            **getattr(self.backend, 'get_status_info', lambda: {})()
        }


class SessionStateManager:
    """Fallback manager usando Streamlit Session State"""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.storage_key = f"progress_{file_name}"
        
        if self.storage_key not in st.session_state:
            st.session_state[self.storage_key] = {}
    
    # Implementa stessa interfaccia di altri backend
    # ...
```

#### 3. progress_manager.py (144 LOC)

**Responsabilità:** Backend storage locale con file JSON

**Class:**

```python
class ProgressManager:
    """
    Gestisce progresso usando file JSON locali.
    
    Attributes:
        file_name (str): Nome file Excel
        progress_dir (str): Directory storage ("UserData")
        progress_file (str): Path file JSON
        progress (Dict): Dizionario in-memory del progresso
    """
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.progress_dir = "UserData"
        self.progress_file = os.path.join(
            self.progress_dir, 
            f"{os.path.splitext(file_name)[0]}_progress.json"
        )
        
        os.makedirs(self.progress_dir, exist_ok=True)
        self.progress = self._load_progress()
    
    def _load_progress(self) -> Dict[str, Dict[str, int]]:
        """Carica progresso da file JSON"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_progress(self):
        """Salva progresso su file JSON"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, ensure_ascii=False, indent=2)
    
    def record_answer(self, word: str, is_correct: bool):
        """Registra risposta e salva su disco"""
        word_lower = word.lower().strip()
        
        if word_lower not in self.progress:
            self.progress[word_lower] = {'correct': 0, 'wrong': 0}
        
        if is_correct:
            self.progress[word_lower]['correct'] += 1
        else:
            self.progress[word_lower]['wrong'] += 1
        
        self._save_progress()  # Salva immediatamente
    
    # Altri metodi...
```

**Formato Dati:**

```json
{
  "hello": {
    "correct": 5,
    "wrong": 2
  },
  "world": {
    "correct": 3,
    "wrong": 1
  }
}
```

#### 4. database_manager.py (259 LOC)

**Responsabilità:** Backend storage cloud con Supabase

**Class:**

```python
class DatabaseManager:
    """
    Gestisce progresso usando database PostgreSQL (Supabase).
    
    Attributes:
        file_name (str): Nome file Excel
        user_id (str): UUID utente unico
        supabase_client: Client Supabase
        is_cloud_enabled (bool): Flag connessione attiva
    """
    
    def __init__(self, file_name: str, user_id: Optional[str] = None):
        self.file_name = file_name
        self.user_id = user_id or self._get_user_id()
        self.supabase_client = None
        self.is_cloud_enabled = False
        
        self._init_supabase()
    
    def _get_user_id(self) -> str:
        """Genera/recupera UUID utente"""
        if 'user_id' not in st.session_state:
            import uuid
            st.session_state.user_id = str(uuid.uuid4())
        return st.session_state.user_id
    
    def _init_supabase(self):
        """Inizializza connessione Supabase"""
        try:
            supabase_url = st.secrets.get("SUPABASE_URL")
            supabase_key = st.secrets.get("SUPABASE_KEY")
            
            if supabase_url and supabase_key and SUPABASE_AVAILABLE:
                self.supabase_client = create_client(supabase_url, supabase_key)
                self.is_cloud_enabled = True
        except Exception as e:
            st.warning(f"Cloud DB non disponibile: {e}")
            self.is_cloud_enabled = False
    
    def record_answer(self, word: str, is_correct: bool):
        """Registra risposta nel database"""
        if not self.is_cloud_enabled:
            # Fallback a session state
            self._record_to_session_state(word, is_correct)
            return
        
        word_lower = word.lower().strip()
        
        # Get current stats
        correct, wrong = self.get_word_stats(word)
        
        # Update
        if is_correct:
            correct += 1
        else:
            wrong += 1
        
        # Save to database
        self._save_progress_to_cloud(word_lower, correct, wrong)
    
    def _save_progress_to_cloud(self, word: str, correct: int, wrong: int):
        """UPSERT nel database"""
        # Check if exists
        existing = self.supabase_client.table("progress")\
            .select("*")\
            .eq("user_id", self.user_id)\
            .eq("file_name", self.file_name)\
            .eq("word", word)\
            .execute()
        
        data = {
            "user_id": self.user_id,
            "file_name": self.file_name,
            "word": word,
            "correct_count": correct,
            "wrong_count": wrong
        }
        
        if existing.data:
            # UPDATE
            self.supabase_client.table("progress")\
                .update(data)\
                .eq("user_id", self.user_id)\
                .eq("file_name", self.file_name)\
                .eq("word", word)\
                .execute()
        else:
            # INSERT
            self.supabase_client.table("progress")\
                .insert(data)\
                .execute()
    
    # Altri metodi...
```

**Schema Database:**

```sql
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    word TEXT NOT NULL,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, file_name, word)
);

CREATE INDEX idx_progress_user_file 
ON progress(user_id, file_name);
```

## API Reference

### HybridProgressManager API

```python
# Inizializzazione
manager = HybridProgressManager("Words.xlsx")

# Get stats per parola
correct, wrong = manager.get_word_stats("hello")
# Returns: (5, 2)

# Registra risposta
manager.record_answer("hello", is_correct=True)
manager.record_answer("hello", is_correct=False)

# Statistiche totali
stats = manager.get_total_stats()
# Returns: {
#     'total_words_practiced': int,
#     'total_correct': int,
#     'total_wrong': int,
#     'total_attempts': int,
#     'accuracy_percentage': float
# }

# Parole difficili
difficult_words = manager.get_difficult_words(min_attempts=3)
# Returns: [
#     {
#         'word': str,
#         'correct': int,
#         'wrong': int,
#         'error_rate': float
#     },
#     ...
# ]

# Info backend
info = manager.get_backend_info()
# Returns: {
#     'backend_type': str,
#     'file_name': str,
#     ...
# }

# Reset progresso
manager.reset_all_progress()
```

### Backend Interface (Abstract)

Tutti i backend implementano questa interfaccia:

```python
from typing import Dict, Tuple

class ProgressBackend:
    """Interfaccia comune per tutti i backend"""
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """
        Ottiene statistiche per una parola.
        
        Args:
            word: Parola da cercare
            
        Returns:
            Tupla (correct_count, wrong_count)
        """
        raise NotImplementedError
    
    def record_answer(self, word: str, is_correct: bool):
        """
        Registra una risposta.
        
        Args:
            word: Parola
            is_correct: True se corretta, False se errata
        """
        raise NotImplementedError
    
    def get_total_stats(self) -> Dict[str, int]:
        """
        Statistiche totali.
        
        Returns:
            Dict con chiavi:
            - total_words_practiced
            - total_correct
            - total_wrong
            - total_attempts
            - accuracy_percentage
        """
        raise NotImplementedError
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        """
        Parole difficili.
        
        Args:
            min_attempts: Minimo tentativi per considerare parola
            
        Returns:
            Lista dict con 'word', 'correct', 'wrong', 'error_rate'
        """
        raise NotImplementedError
    
    def reset_all_progress(self):
        """Reset completo progresso"""
        raise NotImplementedError
    
    def get_status_info(self) -> Dict[str, str]:
        """Info opzionali sul backend"""
        return {}
```

## Estendere il Sistema

### Aggiungere Nuovo Backend

Esempio: MongoDB Backend

**Step 1: Crea nuovo file `mongodb_backend.py`**

```python
from typing import Dict, Tuple
from pymongo import MongoClient

class MongoDBBackend:
    """Backend storage usando MongoDB"""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        
        # Connect to MongoDB
        client = MongoClient(os.getenv("MONGO_URI"))
        self.db = client.learning_english
        self.collection = self.db.progress
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """Query MongoDB"""
        doc = self.collection.find_one({
            "file_name": self.file_name,
            "word": word.lower().strip()
        })
        
        if doc:
            return doc.get("correct", 0), doc.get("wrong", 0)
        return 0, 0
    
    def record_answer(self, word: str, is_correct: bool):
        """UPSERT in MongoDB"""
        word_lower = word.lower().strip()
        
        # Atomic increment
        self.collection.update_one(
            {"file_name": self.file_name, "word": word_lower},
            {
                "$inc": {
                    "correct" if is_correct else "wrong": 1
                },
                "$setOnInsert": {
                    "file_name": self.file_name,
                    "word": word_lower
                }
            },
            upsert=True
        )
    
    def get_total_stats(self) -> Dict[str, int]:
        """Aggregation pipeline"""
        pipeline = [
            {"$match": {"file_name": self.file_name}},
            {"$group": {
                "_id": None,
                "total_words": {"$sum": 1},
                "total_correct": {"$sum": "$correct"},
                "total_wrong": {"$sum": "$wrong"}
            }}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        if result:
            data = result[0]
            total_attempts = data["total_correct"] + data["total_wrong"]
            accuracy = (data["total_correct"] / total_attempts * 100) if total_attempts > 0 else 0
            
            return {
                "total_words_practiced": data["total_words"],
                "total_correct": data["total_correct"],
                "total_wrong": data["total_wrong"],
                "total_attempts": total_attempts,
                "accuracy_percentage": round(accuracy, 1)
            }
        
        return {
            "total_words_practiced": 0,
            "total_correct": 0,
            "total_wrong": 0,
            "total_attempts": 0,
            "accuracy_percentage": 0
        }
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        """Query parole difficili"""
        docs = self.collection.find({
            "file_name": self.file_name
        })
        
        difficult = []
        for doc in docs:
            correct = doc.get("correct", 0)
            wrong = doc.get("wrong", 0)
            total = correct + wrong
            
            if total >= min_attempts and wrong > correct:
                difficult.append({
                    "word": doc["word"],
                    "correct": correct,
                    "wrong": wrong,
                    "error_rate": wrong / total
                })
        
        difficult.sort(key=lambda x: x["error_rate"], reverse=True)
        return difficult
    
    def reset_all_progress(self):
        """Delete documents"""
        self.collection.delete_many({"file_name": self.file_name})
    
    def get_status_info(self) -> Dict[str, str]:
        return {
            "storage_type": "MongoDB",
            "is_persistent": "Yes",
            "collection": "progress"
        }
```

**Step 2: Modifica `hybrid_progress_manager.py`**

```python
# Import condizionale
try:
    from mongodb_backend import MongoDBBackend
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

class HybridProgressManager:
    def _init_backend(self):
        # Aggiungi MongoDB come opzione
        if MONGODB_AVAILABLE and os.getenv("MONGO_URI"):
            try:
                self.backend = MongoDBBackend(self.file_name)
                self.backend_type = "mongodb"
                return
            except Exception as e:
                st.warning(f"MongoDB fallback: {e}")
        
        # ... resto della logica esistente
```

**Step 3: Aggiorna requirements**

```txt
# requirements-mongodb.txt
pymongo>=4.0.0
```

### Aggiungere Nuova Funzionalità

Esempio: Sistema Spaced Repetition

**Step 1: Estendi schema dati**

```python
# In progress_manager.py o database_manager.py

def record_answer(self, word: str, is_correct: bool):
    """Esteso con timestamp"""
    word_lower = word.lower().strip()
    
    if word_lower not in self.progress:
        self.progress[word_lower] = {
            'correct': 0,
            'wrong': 0,
            'last_reviewed': None,  # NUOVO
            'next_review': None     # NUOVO
        }
    
    if is_correct:
        self.progress[word_lower]['correct'] += 1
    else:
        self.progress[word_lower]['wrong'] += 1
    
    # Update review times
    from datetime import datetime, timedelta
    self.progress[word_lower]['last_reviewed'] = datetime.now().isoformat()
    
    # Calculate next review (SM-2 algorithm)
    if is_correct:
        # Aumenta intervallo
        days_to_add = self._calculate_next_interval(word_lower)
    else:
        # Reset a domani
        days_to_add = 1
    
    next_review = datetime.now() + timedelta(days=days_to_add)
    self.progress[word_lower]['next_review'] = next_review.isoformat()
    
    self._save_progress()

def _calculate_next_interval(self, word: str) -> int:
    """SM-2 spaced repetition algorithm"""
    # Implementa logica SM-2
    # Basato su facilità e intervallo precedente
    pass

def get_words_due_for_review(self) -> list:
    """Nuova API: parole da ripassare oggi"""
    from datetime import datetime
    now = datetime.now()
    
    due_words = []
    for word, stats in self.progress.items():
        next_review = stats.get('next_review')
        if next_review:
            next_review_dt = datetime.fromisoformat(next_review)
            if next_review_dt <= now:
                due_words.append(word)
    
    return due_words
```

**Step 2: UI in EnglishLearning.py**

```python
# Aggiungi pulsante "Review Mode"
if st.button("📅 Modalità Ripasso"):
    st.session_state.review_mode = True

if st.session_state.get('review_mode', False):
    # Mostra solo parole da ripassare
    due_words = progress_manager.get_words_due_for_review()
    
    if due_words:
        st.info(f"📚 {len(due_words)} parole da ripassare oggi")
        # Filter words to show only due_words
    else:
        st.success("✅ Nessuna parola da ripassare oggi!")
        st.session_state.review_mode = False
```

## Testing

### Test Manuale

**Checklist Test Locale:**

```bash
# 1. Setup pulito
rm -rf UserData/
rm -rf .streamlit/secrets.toml

# 2. Avvia app
streamlit run EnglishLearning.py

# 3. Test Cases
# [ ] Carica file dalla libreria
# [ ] Rispondi correttamente a 3 parole
# [ ] Rispondi erroneamente a 2 parole
# [ ] Verifica statistiche (3 corrette, 2 errate, 60% precisione)
# [ ] Click "Ascolta" - audio funziona
# [ ] Click "Mostra traduzione" - traduzione appare
# [ ] Naviga avanti/indietro
# [ ] Reset progresso
# [ ] Chiudi e riapri app
# [ ] Verifica persistenza dati (UserData/*.json creati)
```

### Unit Testing (Esempio)

```python
# test_progress_manager.py

import pytest
import os
import json
from progress_manager import ProgressManager

@pytest.fixture
def manager():
    """Fixture per test"""
    return ProgressManager("test_words.xlsx")

def test_record_correct_answer(manager):
    """Test registrazione risposta corretta"""
    manager.record_answer("hello", is_correct=True)
    
    correct, wrong = manager.get_word_stats("hello")
    assert correct == 1
    assert wrong == 0

def test_record_wrong_answer(manager):
    """Test registrazione risposta errata"""
    manager.record_answer("hello", is_correct=False)
    
    correct, wrong = manager.get_word_stats("hello")
    assert correct == 0
    assert wrong == 1

def test_get_total_stats(manager):
    """Test statistiche totali"""
    manager.record_answer("hello", True)
    manager.record_answer("world", True)
    manager.record_answer("world", False)
    
    stats = manager.get_total_stats()
    assert stats['total_words_practiced'] == 2
    assert stats['total_correct'] == 2
    assert stats['total_wrong'] == 1
    assert stats['accuracy_percentage'] == 66.7

def test_get_difficult_words(manager):
    """Test identificazione parole difficili"""
    # Setup: parola con più errori
    manager.record_answer("difficult", False)
    manager.record_answer("difficult", False)
    manager.record_answer("difficult", False)
    manager.record_answer("difficult", True)
    
    difficult = manager.get_difficult_words(min_attempts=3)
    assert len(difficult) == 1
    assert difficult[0]['word'] == "difficult"
    assert difficult[0]['error_rate'] == 0.75

def test_persistence(manager):
    """Test salvataggio su disco"""
    manager.record_answer("hello", True)
    
    # Verifica file creato
    assert os.path.exists(manager.progress_file)
    
    # Verifica contenuto
    with open(manager.progress_file, 'r') as f:
        data = json.load(f)
    assert "hello" in data
    assert data["hello"]["correct"] == 1

def test_reset(manager):
    """Test reset progresso"""
    manager.record_answer("hello", True)
    manager.record_answer("world", False)
    
    manager.reset_all_progress()
    
    stats = manager.get_total_stats()
    assert stats['total_words_practiced'] == 0

# Run tests
# pytest test_progress_manager.py -v
```

### Integration Testing

```python
# test_integration.py

import streamlit as st
from hybrid_progress_manager import HybridProgressManager

def test_full_workflow():
    """Test workflow completo"""
    # 1. Init manager
    manager = HybridProgressManager("Words.xlsx")
    
    # 2. Verifica backend
    info = manager.get_backend_info()
    assert info['backend_type'] in ['local_files', 'session_state']
    
    # 3. Simula sessione studio
    words = ["hello", "world", "goodbye"]
    
    for i, word in enumerate(words):
        # Risposte miste
        is_correct = i % 2 == 0
        manager.record_answer(word, is_correct)
    
    # 4. Verifica statistiche
    stats = manager.get_total_stats()
    assert stats['total_words_practiced'] == 3
    assert stats['total_correct'] == 2
    assert stats['total_wrong'] == 1
```

## Best Practices

### Coding Style

**1. Python PEP 8**

```python
# ✅ Good
def calculate_accuracy(correct: int, wrong: int) -> float:
    """Calculate accuracy percentage."""
    total = correct + wrong
    if total == 0:
        return 0.0
    return (correct / total) * 100

# ❌ Bad
def calcAcc(c,w):
    t=c+w
    if t==0: return 0
    return c/t*100
```

**2. Type Hints**

```python
# ✅ Good
from typing import Dict, Tuple, Optional

def get_word_stats(self, word: str) -> Tuple[int, int]:
    """Returns (correct, wrong) counts."""
    pass

def get_total_stats(self) -> Dict[str, int]:
    """Returns statistics dictionary."""
    pass

# ❌ Bad
def get_word_stats(self, word):
    pass
```

**3. Docstrings**

```python
# ✅ Good
def record_answer(self, word: str, is_correct: bool):
    """
    Records a user answer for a word.
    
    Args:
        word: The word being practiced
        is_correct: True if answer was correct, False otherwise
        
    Side Effects:
        Updates internal progress dictionary
        Saves to disk (for local backend)
        
    Example:
        >>> manager.record_answer("hello", True)
        >>> correct, wrong = manager.get_word_stats("hello")
        >>> print(correct)  # 1
    """
    pass
```

**4. Error Handling**

```python
# ✅ Good
try:
    data = load_excel_file(path)
except FileNotFoundError:
    st.error("File not found")
    return
except pd.errors.EmptyDataError:
    st.error("File is empty")
    return
except Exception as e:
    st.error(f"Unexpected error: {e}")
    logging.exception("Failed to load file")
    return

# ❌ Bad
try:
    data = load_excel_file(path)
except:
    pass
```

### Git Workflow

**Branch Naming:**

```bash
feature/spaced-repetition
bugfix/stats-calculation
hotfix/audio-playback
docs/api-reference
```

**Commit Messages:**

```bash
# ✅ Good
git commit -m "feat: Add MongoDB backend support"
git commit -m "fix: Correct accuracy calculation for zero attempts"
git commit -m "docs: Update API reference for new methods"
git commit -m "refactor: Extract backend selection logic"

# ❌ Bad
git commit -m "update"
git commit -m "fixes"
git commit -m "wip"
```

**Pull Request Template:**

```markdown
## Description
[Describe changes]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

### Performance

**1. Lazy Loading**

```python
# ✅ Good: Load only quando necessario
@st.cache_data
def load_excel_file(path: str) -> pd.DataFrame:
    """Cache Excel loading"""
    return pd.read_excel(path)

# ❌ Bad: Load tutto all'inizio
all_files = [load_excel(f) for f in all_excel_files()]
```

**2. Database Queries**

```python
# ✅ Good: Single query con indici
SELECT * FROM progress 
WHERE user_id = ? AND file_name = ?
-- Index: (user_id, file_name)

# ❌ Bad: Multiple queries
for word in words:
    SELECT * FROM progress WHERE word = ?
```

**3. Caching**

```python
# Use Streamlit cache
@st.cache_data(ttl=3600)  # Cache 1 hour
def get_translation(word: str, from_lang: str, to_lang: str) -> str:
    """Cache traduzioni"""
    return GoogleTranslator(from_lang, to_lang).translate(word)
```

## Contribuire

### Come Contribuire

1. **Fork Repository**
   ```bash
   # Su GitHub: Click "Fork"
   ```

2. **Clone Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LearningEnglish.git
   cd LearningEnglish
   ```

3. **Crea Branch**
   ```bash
   git checkout -b feature/my-amazing-feature
   ```

4. **Implementa Changes**
   ```bash
   # Fai le modifiche
   # Testa localmente
   # Commit
   git add .
   git commit -m "feat: Add amazing feature"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/my-amazing-feature
   ```

6. **Open Pull Request**
   - Vai su GitHub
   - Click "New Pull Request"
   - Descrivi le modifiche
   - Submit

### Aree di Contribuzione

**High Priority:**
- 🐛 Bug fixes
- 📝 Documentation improvements
- ✅ Test coverage
- 🌍 i18n/Localization

**Medium Priority:**
- ✨ New features (spaced repetition, etc.)
- 🎨 UI/UX improvements
- ⚡ Performance optimizations

**Low Priority:**
- 🧪 Experimental features
- 🔬 Research/POC

### Code Review Checklist

**Per Reviewer:**

- [ ] Code follows style guide
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Performance impact considered
- [ ] Security issues checked
- [ ] Error handling appropriate

---

**Questions?**

- Open GitHub Issue
- Contact maintainers
- Check existing documentation

**Happy Coding! 🚀**
