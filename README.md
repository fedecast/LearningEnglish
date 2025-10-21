# 🎯 English Learning App

Un'applicazione web interattiva per l'apprendimento dell'inglese (e altre lingue) attraverso flashcard personalizzate con sistema di tracciamento del progresso.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Indice

- [Panoramica](#-panoramica)
- [Caratteristiche](#-caratteristiche)
- [Architettura](#-architettura)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Formato File Excel](#-formato-file-excel)
- [Sistema di Progresso](#-sistema-di-progresso)
- [Deployment](#-deployment)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Guida per Sviluppatori](#-guida-per-sviluppatori)

## 🌟 Panoramica

**English Learning App** è un'applicazione web moderna e responsive per l'apprendimento delle lingue attraverso il metodo delle flashcard. L'app supporta:

- **Apprendimento bidirezionale**: Traduci da inglese a italiano e viceversa
- **Audio integrato**: Pronuncia automatica delle parole usando Google Text-to-Speech
- **Tracciamento intelligente**: Sistema di progresso che memorizza le tue performance
- **Statistiche dettagliate**: Monitora la tua precisione e identifica le parole difficili
- **Modalità flessibili**: Ordine casuale o sequenziale delle parole
- **Multi-file**: Gestisci diversi set di vocaboli con progresso separato

## ✨ Caratteristiche

### Funzionalità Core

1. **🎴 Sistema Flashcard Intelligente**
   - Caricamento file Excel personalizzati
   - Selezione da libreria predefinita (Files/)
   - Traduzione automatica con Google Translate
   - Verifica risposte con normalizzazione del testo

2. **🔊 Audio e Pronuncia**
   - Text-to-Speech integrato (gTTS)
   - Supporto multilingua (inglese, italiano)
   - Riproduzione audio on-demand

3. **📊 Sistema di Progresso Avanzato**
   - Tracciamento automatico di ogni risposta
   - Statistiche per parola (corrette/errate)
   - Statistiche globali (precisione, parole praticate)
   - Identificazione automatica parole difficili
   - Top 5 parole da ripassare

4. **💾 Storage Ibrido Multi-Backend**
   - **Locale**: File JSON per sviluppo
   - **Cloud**: Database Supabase per produzione
   - **Fallback**: Session State sempre disponibile
   - Scelta automatica del backend appropriato

5. **📱 Design Responsive**
   - Ottimizzato per mobile
   - UI intuitiva con pulsanti grandi
   - Feedback visivo immediato
   - Dark mode supportato

## 🏗️ Architettura

### Architettura a Livelli

```
┌─────────────────────────────────────────────┐
│         PRESENTAZIONE (UI)                  │
│  EnglishLearning.py - Streamlit App         │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      LOGICA BUSINESS                        │
│  HybridProgressManager - Orchestratore      │
└──────┬───────────┬───────────┬──────────────┘
       │           │           │
   ┌───▼──┐    ┌──▼───┐   ┌───▼────┐
   │Local │    │Cloud │   │Session │
   │Files │    │  DB  │   │ State  │
   └──────┘    └──────┘   └────────┘
```

### Componenti Principali

#### 1. **EnglishLearning.py** - Interfaccia Utente
- Gestione UI con Streamlit
- Rendering flashcard
- Gestione interazioni utente
- Visualizzazione statistiche
- Integrazione audio (gTTS)
- Traduzione automatica (deep-translator)

#### 2. **HybridProgressManager** - Orchestratore
Componente centrale che gestisce la logica di selezione del backend:

```python
┌─────────────────────────────────────┐
│   HybridProgressManager             │
│                                     │
│  ┌────────────────────────────┐    │
│  │ Backend Selection Logic    │    │
│  │ 1. Is Cloud Deployment?    │    │
│  │ 2. Supabase Available?     │    │
│  │ 3. Use Local Files?        │    │
│  │ 4. Fallback Session State  │    │
│  └────────────────────────────┘    │
│                                     │
│  Delegated Methods:                 │
│  • get_word_stats()                 │
│  • record_answer()                  │
│  • get_total_stats()                │
│  • get_difficult_words()            │
│  • reset_all_progress()             │
└─────────────────────────────────────┘
```

**Logica di Selezione Backend:**

```
1. Cloud Deployment + Supabase?
   └─YES→ DatabaseManager (Cloud)
   └─NO─┐
        │
2. Local Environment?
   └─YES→ ProgressManager (Local Files)
   └─NO─┐
        │
3. Fallback
   └→ SessionStateManager (Temporaneo)
```

#### 3. **DatabaseManager** - Storage Cloud
Gestisce la persistenza su database PostgreSQL (Supabase):

- **Connessione**: Usa credenziali da Streamlit Secrets
- **User ID**: Generato automaticamente per sessione
- **Schema DB**: Tabella `progress` con RLS (Row Level Security)
- **Operazioni**: CRUD complete su progresso utente
- **Fallback**: Session State se cloud non disponibile

**Schema Database:**
```sql
CREATE TABLE progress (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    word TEXT NOT NULL,
    correct_count INTEGER DEFAULT 0,
    wrong_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, file_name, word)
);
```

#### 4. **ProgressManager** - Storage Locale
Gestisce la persistenza su file system locale:

- **Directory**: `UserData/` (esclusa da Git)
- **Formato**: File JSON per ogni Excel
- **Naming**: `[NomeFile]_progress.json`
- **Struttura**:
  ```json
  {
    "word1": {"correct": 5, "wrong": 2},
    "word2": {"correct": 3, "wrong": 1}
  }
  ```
- **Vantaggi**: Veloce, semplice, nessuna configurazione necessaria

#### 5. **SessionStateManager** - Fallback
Manager minimalista che usa solo Streamlit Session State:

- **Storage**: In-memory durante la sessione
- **Persistenza**: Persa al refresh/chiusura
- **Utilizzo**: Quando nessun altro backend è disponibile
- **Affidabilità**: Sempre funzionante

### Flusso di Funzionamento

#### Flusso Principale - Sessione di Studio

```
START
  │
  ├─ Utente carica/seleziona file Excel
  │  └─ Parse Excel → Prima riga = lingua
  │                  → Altre righe = parole
  │
  ├─ Inizializzazione HybridProgressManager
  │  └─ Auto-detect backend appropriato
  │
  ├─ LOOP: Per ogni parola
  │  │
  │  ├─ Mostra parola corrente
  │  │  └─ Display statistiche parola (se esistenti)
  │  │
  │  ├─ Audio disponibile (gTTS)
  │  │  └─ Click "Ascolta" → Riproduzione
  │  │
  │  ├─ Traduzione automatica
  │  │  └─ GoogleTranslator(source, target)
  │  │
  │  ├─ Input utente
  │  │  └─ Normalize text (lowercase, trim)
  │  │
  │  ├─ Verifica risposta
  │  │  ├─ Corretto? → record_answer(word, true)
  │  │  └─ Errato?   → record_answer(word, false)
  │  │
  │  ├─ Mostra risultato (✅/❌)
  │  │
  │  └─ Azioni disponibili:
  │     ├─ Prossima parola (casuale/sequenziale)
  │     ├─ Parola precedente
  │     ├─ Riprova
  │     ├─ Mostra traduzione
  │     └─ Reinizia
  │
  └─ Visualizza Statistiche Avanzate
     ├─ Metriche globali
     ├─ Top 5 parole difficili
     └─ Opzione reset progresso
```

#### Flusso Registrazione Risposta

```
record_answer(word, is_correct)
  │
  ├─ HybridProgressManager.record_answer()
  │  └─ Delega al backend attivo
  │
  ├─ Backend = DatabaseManager?
  │  ├─YES→ Fetch current stats da DB
  │  │     └─ UPDATE/INSERT su Supabase
  │  │
  │  ├─NO─→ Backend = ProgressManager?
  │  │     ├─YES→ Update in-memory dict
  │  │     │     └─ Salva su file JSON
  │  │     │
  │  │     └─NO─→ Backend = SessionStateManager
  │  │           └─ Update st.session_state
  │
  └─ DONE
```

## 🚀 Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip (Python package manager)

### Installazione Base

```bash
# 1. Clone del repository
git clone https://github.com/fedecast/LearningEnglish.git
cd LearningEnglish

# 2. Crea ambiente virtuale (raccomandato)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Installa dipendenze
pip install -r requirements.txt
```

### Dipendenze Principali

```txt
streamlit          # Framework web
pandas             # Gestione dati Excel
openpyxl           # Lettura file Excel
deep-translator    # Traduzione automatica
gTTS               # Text-to-Speech
```

### Dipendenze Opzionali

Per il deployment cloud con database:
```bash
pip install -r requirements-cloud.txt
```

Include: `supabase>=1.0.0`

## 📖 Utilizzo

### Avvio Locale

```bash
streamlit run EnglishLearning.py
```

L'app si aprirà automaticamente nel browser su `http://localhost:8501`

### Utilizzo Step-by-Step

1. **Carica un File**
   - Opzione A: Seleziona un file dalla cartella `Files/`
   - Opzione B: Carica un tuo file Excel personalizzato

2. **Configura Sessione**
   - Scegli lingua della risposta (English/Italian)
   - Seleziona ordine parole (Casuale/Sequenziale)

3. **Studia**
   - Leggi la parola mostrata
   - Opzionale: Clicca "🔊 Ascolta" per la pronuncia
   - Digita la traduzione
   - Premi Invio per verificare

4. **Naviga**
   - Usa "➡️ Prossima" per parola successiva
   - Usa "⬅️ Precedente" per tornare indietro
   - Usa "🔄 Riprova" per riprovare la stessa parola

5. **Monitora Progresso**
   - Vedi statistiche in tempo reale in alto
   - Espandi "📊 Statistiche Avanzate" per dettagli
   - Controlla le parole difficili da ripassare

## 📄 Formato File Excel

### Struttura Richiesta

```
┌─────────────────┐
│   Colonna A     │  (UNICA COLONNA)
├─────────────────┤
│   english       │  ← Riga 1: Lingua (english/italian)
├─────────────────┤
│   hello         │  ← Riga 2+: Parole
│   goodbye       │
│   thank you     │
│   please        │
│   ...           │
└─────────────────┘
```

### Regole

1. **Una sola colonna**: Il file deve avere UNA SOLA colonna
2. **Prima riga**: Nome della lingua ("english" o "italian")
3. **Righe successive**: Una parola/frase per riga
4. **Formato**: .xlsx o .xls

### Esempio File

Scarica e usa i file di esempio nella cartella `Files/`:
- `Words.xlsx` - Vocabolario inglese base
- `Numbers.xlsx` - Numeri in inglese
- `Numeri.xlsx` - Numeri in italiano

### Creazione Nuovo File

1. Apri Excel o Google Sheets
2. Crea una colonna con:
   - Prima riga: `english` o `italian`
   - Altre righe: le tue parole
3. Salva come `.xlsx`
4. Carica nell'app

## 📊 Sistema di Progresso

### Architettura Storage

Il sistema implementa un **pattern Strategy** per lo storage:

```
┌───────────────────────────────────────┐
│   HybridProgressManager               │
│   (Context)                           │
└─────────┬─────────────────────────────┘
          │
          │ Seleziona strategia
          │
    ┌─────┴─────┬──────────┬────────────┐
    │           │          │            │
┌───▼────┐ ┌───▼────┐ ┌───▼─────┐ ┌────▼────┐
│Database│ │Progress│ │ Session │ │ Custom  │
│Manager │ │Manager │ │ State   │ │ Backend │
│(Cloud) │ │(Local) │ │ Manager │ │(Future) │
└────────┘ └────────┘ └─────────┘ └─────────┘
```

### Confronto Backend

| Feature | DatabaseManager | ProgressManager | SessionStateManager |
|---------|----------------|-----------------|---------------------|
| **Persistenza** | ✅ Permanente | ✅ Tra sessioni | ❌ Solo sessione |
| **Multi-utente** | ✅ Sì | ❌ No | ❌ No |
| **Configurazione** | 🔧 Secrets necessari | ✅ Zero config | ✅ Zero config |
| **Velocità** | 🌐 Rete dipendente | ⚡ Velocissimo | ⚡ Velocissimo |
| **Backup** | ✅ Automatico | 📁 File locali | ❌ No |
| **Scalabilità** | ✅ Illimitata | 💾 Disco locale | 💾 RAM |
| **Uso ideale** | Production/Cloud | Development/Local | Fallback |

### Funzionalità Statistiche

#### Metriche Disponibili

1. **Statistiche Globali**
   ```python
   {
       'total_words_practiced': 42,    # Parole uniche studiate
       'total_correct': 156,            # Risposte corrette totali
       'total_wrong': 38,               # Risposte errate totali
       'total_attempts': 194,           # Tentativi totali
       'accuracy_percentage': 80.4      # Precisione %
   }
   ```

2. **Statistiche per Parola**
   ```python
   get_word_stats("hello")
   # Returns: (correct_count, wrong_count)
   # Example: (5, 2) → 5 corrette, 2 errate
   ```

3. **Parole Difficili**
   ```python
   [
       {
           'word': 'difficult',
           'correct': 2,
           'wrong': 8,
           'error_rate': 0.8  # 80% errori
       },
       ...
   ]
   ```

#### Algoritmo Identificazione Parole Difficili

```python
def is_difficult(word_stats, min_attempts=3):
    """
    Una parola è considerata difficile se:
    1. Tentativi totali >= min_attempts (default: 3)
    2. Errori > Risposte Corrette
    """
    total = word_stats['correct'] + word_stats['wrong']
    if total >= min_attempts and word_stats['wrong'] > word_stats['correct']:
        return True
    return False
```

## 🌐 Deployment

### Opzioni Deployment

#### 1. 🏠 Locale (Development)

**Caratteristiche:**
- Storage: File JSON locali
- Persistenza: Tra sessioni
- Multi-utente: No
- Configurazione: Zero

**Setup:**
```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate su Windows
pip install -r requirements.txt
streamlit run EnglishLearning.py
```

**Backend utilizzato:** `ProgressManager` (File JSON)

---

#### 2. ☁️ Streamlit Cloud (Basic)

**Caratteristiche:**
- Storage: Session State
- Persistenza: No (persa al refresh)
- Multi-utente: Sì (sessioni separate)
- Configurazione: Zero

**Setup:**
1. Push codice su GitHub
2. Vai su [share.streamlit.io](https://share.streamlit.io)
3. Connetti repository
4. Deploy!

**Backend utilizzato:** `SessionStateManager`

---

#### 3. ☁️ Streamlit Cloud + Supabase (Production)

**Caratteristiche:**
- Storage: Database PostgreSQL
- Persistenza: Permanente
- Multi-utente: Sì (isolato per user_id)
- Configurazione: Secrets richiesti

**Setup:**

**A. Crea Database Supabase (Gratuito)**

1. Vai su [supabase.com](https://supabase.com)
2. Crea nuovo progetto
3. Nel SQL Editor, esegui:

```sql
-- Crea tabella progress
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

-- Indice per performance
CREATE INDEX idx_progress_user_file 
ON progress(user_id, file_name);

-- Row Level Security (opzionale ma raccomandato)
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;

-- Policy: utenti vedono solo i propri dati
CREATE POLICY "Users can manage own progress" 
ON progress 
USING (true)  -- Per semplicità, permetti tutto
WITH CHECK (true);
```

4. Vai su Settings > API
5. Copia:
   - `URL` (es: https://xxx.supabase.co)
   - `anon/public key`

**B. Deploy su Streamlit Cloud**

1. Push codice su GitHub
2. Deploy su [share.streamlit.io](https://share.streamlit.io)
3. In "Advanced settings" > "Secrets", aggiungi:

```toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

4. Salva e riavvia l'app

**Backend utilizzato:** `DatabaseManager` (Supabase)

---

### Troubleshooting Deployment

#### Problema: "Module not found: supabase"

**Causa:** requirements-cloud.txt non utilizzato

**Soluzione:**
```bash
# In Streamlit Cloud > Advanced Settings
# Cambia "Python dependencies file" a:
requirements-cloud.txt
```

#### Problema: "Database cloud non disponibile"

**Causa:** Secrets non configurati o errati

**Verifica:**
1. Secrets presenti in Streamlit Cloud
2. URL e KEY corretti da Supabase
3. Tabella `progress` creata

**Test locale:**
```python
# Crea .streamlit/secrets.toml
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "your-key"

# Poi testa
streamlit run EnglishLearning.py
```

#### Problema: App lenta con database

**Causa:** Troppe query al database

**Ottimizzazione:**
- Le query sono già ottimizzate con indici
- Considera cache locale (futura feature)

## 📁 Struttura del Progetto

```
LearningEnglish/
│
├── 📄 EnglishLearning.py          # App principale Streamlit
│   ├── UI Components
│   ├── Business Logic
│   └── Integration Points
│
├── 📄 hybrid_progress_manager.py  # Orchestratore backend
│   ├── Backend Selection Logic
│   ├── HybridProgressManager class
│   └── SessionStateManager class (fallback)
│
├── 📄 progress_manager.py         # Storage locale
│   └── ProgressManager class
│       ├── JSON file operations
│       └── Local UserData/ management
│
├── 📄 database_manager.py         # Storage cloud
│   └── DatabaseManager class
│       ├── Supabase integration
│       ├── PostgreSQL operations
│       └── User isolation
│
├── 📄 main.py                     # Entry point (placeholder)
│
├── 📂 Files/                      # Libreria file Excel
│   ├── Words.xlsx
│   ├── Numbers.xlsx
│   ├── Numeri.xlsx
│   └── Unknown.xlsx
│
├── 📂 UserData/                   # Storage locale (gitignored)
│   ├── Words_progress.json
│   ├── Numbers_progress.json
│   └── ...
│
├── 📂 .streamlit/
│   └── secrets.toml.example       # Template secrets
│
├── 📂 documents/
│   └── README.md                  # Docs secondarie
│
├── 📄 requirements.txt            # Dipendenze base
├── 📄 requirements-base.txt       # Dipendenze minime
├── 📄 requirements-cloud.txt      # Dipendenze + Supabase
│
├── 📄 DEPLOYMENT.md               # Guida deployment dettagliata
├── 📄 PROGRESS_SYSTEM.md          # Docs sistema progresso
│
├── 📄 .gitignore                  # File esclusi da Git
│   └── UserData/                  # Dati utente esclusi
│
└── 📄 README.md                   # Questo file
```

### Descrizione Moduli

#### Core Application
- **EnglishLearning.py** (335 righe)
  - Entry point applicazione
  - Gestione completa UI
  - Integrazione servizi esterni (gTTS, GoogleTranslator)
  - Logica flashcard
  - Rendering statistiche

#### Progress System
- **hybrid_progress_manager.py** (193 righe)
  - Pattern Strategy per storage
  - Auto-detection ambiente (local/cloud)
  - Delegazione chiamate al backend appropriato
  - SessionStateManager integrato come fallback

- **progress_manager.py** (144 righe)
  - Storage file JSON locale
  - CRUD operazioni su UserData/
  - Gestione statistiche
  - Identificazione parole difficili

- **database_manager.py** (259 righe)
  - Integrazione Supabase
  - Operazioni PostgreSQL
  - Gestione user_id
  - Fallback a Session State

#### Configuration
- **requirements*.txt**
  - `requirements.txt`: Configurazione standard
  - `requirements-base.txt`: Solo essenziale (no DB)
  - `requirements-cloud.txt`: Con Supabase

## 👨‍💻 Guida per Sviluppatori

### Setup Ambiente Sviluppo

```bash
# 1. Clone e setup
git clone https://github.com/fedecast/LearningEnglish.git
cd LearningEnglish

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install development dependencies
pip install -r requirements.txt

# 4. (Opzionale) Install cloud dependencies per test
pip install -r requirements-cloud.txt

# 5. Run app
streamlit run EnglishLearning.py
```

### Aggiungere un Nuovo Backend

Il sistema è progettato per essere estendibile. Per aggiungere un nuovo backend:

**1. Crea una nuova classe Backend**

```python
# custom_backend.py

class CustomBackend:
    """Nuovo backend storage personalizzato."""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
        # Tua inizializzazione
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        """Implementa: ritorna (correct, wrong)"""
        pass
    
    def record_answer(self, word: str, is_correct: bool):
        """Implementa: salva risposta"""
        pass
    
    def get_total_stats(self) -> Dict[str, int]:
        """Implementa: ritorna statistiche totali"""
        pass
    
    def get_difficult_words(self, min_attempts: int = 3) -> list:
        """Implementa: ritorna parole difficili"""
        pass
    
    def reset_all_progress(self):
        """Implementa: reset completo"""
        pass
    
    def get_status_info(self) -> Dict[str, str]:
        """Opzionale: info sul backend"""
        return {"storage_type": "Custom Backend"}
```

**2. Modifica HybridProgressManager**

```python
# hybrid_progress_manager.py

from custom_backend import CustomBackend

class HybridProgressManager:
    def _init_backend(self):
        # Aggiungi tua logica
        if self._should_use_custom_backend():
            try:
                self.backend = CustomBackend(self.file_name)
                self.backend_type = "custom"
                return
            except Exception as e:
                st.warning(f"Fallback da custom backend: {e}")
        
        # ... resto della logica esistente
    
    def _should_use_custom_backend(self) -> bool:
        """Logica per decidere quando usare custom backend."""
        # Es: check variabile ambiente
        return os.getenv("USE_CUSTOM_BACKEND") == "true"
```

### Struttura Dati

#### Session State Keys

```python
st.session_state = {
    # Progress System
    'progress_manager': HybridProgressManager,
    'current_file': str,  # Nome file Excel corrente
    
    # Quiz State
    'current_idx': int,  # Indice parola corrente
    'show_answer': bool,
    'answer_result': str,  # "correct"/"wrong"/None
    'input_key': int,  # Per forzare re-render input
    'show_translation': bool,
    'word_order': str,  # "Casuale"/"Sequenziale"
    
    # Fallback Storage (se DatabaseManager senza cloud)
    'local_progress': {
        'Words.xlsx': {
            'hello': {'correct': 5, 'wrong': 2},
            'goodbye': {'correct': 3, 'wrong': 1}
        }
    },
    
    # User ID (per DatabaseManager)
    'user_id': str  # UUID generato
}
```

#### JSON Progress Format (ProgressManager)

```json
{
  "hello": {
    "correct": 5,
    "wrong": 2
  },
  "goodbye": {
    "correct": 3,
    "wrong": 1
  },
  "difficult_word": {
    "correct": 1,
    "wrong": 8
  }
}
```

### API Reference

#### HybridProgressManager

```python
manager = HybridProgressManager(file_name="Words.xlsx")

# Ottieni statistiche parola
correct, wrong = manager.get_word_stats("hello")
# Returns: (5, 2)

# Registra risposta
manager.record_answer("hello", is_correct=True)
manager.record_answer("hello", is_correct=False)

# Statistiche totali
stats = manager.get_total_stats()
# Returns: {
#     'total_words_practiced': 42,
#     'total_correct': 156,
#     'total_wrong': 38,
#     'total_attempts': 194,
#     'accuracy_percentage': 80.4
# }

# Parole difficili
difficult = manager.get_difficult_words(min_attempts=3)
# Returns: [
#     {'word': 'difficult', 'correct': 2, 'wrong': 8, 'error_rate': 0.8},
#     ...
# ]

# Info backend
info = manager.get_backend_info()
# Returns: {
#     'backend_type': 'cloud_database',
#     'file_name': 'Words.xlsx',
#     ...
# }

# Reset progresso
manager.reset_all_progress()
```

### Testing

**Test Manuale:**

1. **Test Backend Locale:**
```bash
# Assicurati di essere in ambiente locale
streamlit run EnglishLearning.py

# Verifica:
# - Cartella UserData/ creata
# - File JSON creati dopo risposte
# - Statistiche persistono tra sessioni
```

2. **Test Backend Cloud:**
```bash
# Setup secrets
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "your-key"
EOF

# Run
streamlit run EnglishLearning.py

# Verifica:
# - Info Storage mostra "Database Cloud"
# - Dati salvati in Supabase
# - User ID generato
```

3. **Test Fallback:**
```bash
# Rinomina progress_manager.py
mv progress_manager.py progress_manager.py.bak

# Run
streamlit run EnglishLearning.py

# Verifica:
# - Info Storage mostra "Session State"
# - App funziona comunque
# - Dati persi al refresh
```

### Best Practices

1. **Non modificare file Excel originali**
   - Tutto il progresso va in storage separato
   - Files/ directory è read-only

2. **Gestione Errori**
   - Ogni backend gestisce propri errori
   - Fallback sempre disponibile
   - Messaggi utente user-friendly

3. **Performance**
   - File JSON: lettura/scrittura minimali
   - Database: query ottimizzate con indici
   - Session State: in-memory, velocissimo

4. **Sicurezza**
   - Secrets mai in codice
   - UserData/ in .gitignore
   - RLS su database (opzionale)

### Contribuire

1. Fork repository
2. Crea branch feature (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing`)
5. Apri Pull Request

### Roadmap Future

- [ ] Sistema spaced repetition (algoritmo SM-2)
- [ ] Export/import progresso
- [ ] Modalità revisione parole difficili
- [ ] Grafici progresso nel tempo
- [ ] Supporto immagini nelle flashcard
- [ ] API REST per integrazione esterna
- [ ] App mobile nativa (React Native)
- [ ] Modalità multiplayer/competizione

## 📝 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi file LICENSE per dettagli.

## 🙏 Credits

- **Streamlit** - Framework UI
- **Supabase** - Database Backend
- **Google Translate** - Traduzioni
- **gTTS** - Text-to-Speech
- **Pandas** - Data manipulation

## 📧 Contatti

Per domande, suggerimenti o segnalazioni bug:
- Apri una [Issue](https://github.com/fedecast/LearningEnglish/issues)
- Contatta: [GitHub Profile](https://github.com/fedecast)

---

**Made with ❤️ for language learners**