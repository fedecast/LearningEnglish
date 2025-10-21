# 🏗️ Architettura - English Learning App

Documentazione approfondita dell'architettura del sistema.

## Indice

- [Panoramica Architetturale](#panoramica-architetturale)
- [Pattern e Principi](#pattern-e-principi)
- [Diagrammi](#diagrammi)
- [Componenti Dettagliati](#componenti-dettagliati)
- [Flussi Operativi](#flussi-operativi)
- [Decisioni Architetturali](#decisioni-architetturali)

## Panoramica Architetturale

L'applicazione segue un'architettura a **3 livelli** (Three-Tier Architecture):

```
┌──────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                   │
│              (EnglishLearning.py)                    │
│                                                      │
│  • Streamlit UI Components                          │
│  • User Input Handling                              │
│  • Rendering & Visualization                        │
│  • External Services Integration (gTTS, Translator) │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ API Calls
                     │
┌────────────────────▼─────────────────────────────────┐
│                 BUSINESS LOGIC LAYER                 │
│           (HybridProgressManager)                    │
│                                                      │
│  • Backend Selection Strategy                        │
│  • Business Rules Enforcement                        │
│  • Data Validation                                   │
│  • Orchestration                                     │
└────────────────────┬─────────────────────────────────┘
                     │
                     │ Storage Operations
                     │
┌────────────────────▼─────────────────────────────────┐
│                 DATA ACCESS LAYER                    │
│      (DatabaseManager, ProgressManager,              │
│            SessionStateManager)                      │
│                                                      │
│  • Data Persistence                                  │
│  • CRUD Operations                                   │
│  • Query Optimization                                │
│  • Transaction Management                            │
└──────────────────────────────────────────────────────┘
```

## Pattern e Principi

### 1. Strategy Pattern

**Problema:** Necessità di supportare diversi backend storage senza modificare il codice client.

**Soluzione:** Implementazione del pattern Strategy con `HybridProgressManager` come Context.

```
┌─────────────────────────────────────┐
│   <<interface>>                     │
│   ProgressBackend                   │
├─────────────────────────────────────┤
│ + get_word_stats(word)              │
│ + record_answer(word, is_correct)   │
│ + get_total_stats()                 │
│ + get_difficult_words()             │
│ + reset_all_progress()              │
└──────────────▲──────────────────────┘
               │
               │ implements
               │
   ┌───────────┼───────────┬──────────────────┐
   │           │           │                  │
┌──▼────┐ ┌───▼────┐ ┌────▼──────┐ ┌────────▼────┐
│Database│ │Progress│ │  Session  │ │   Custom    │
│Manager │ │Manager │ │   State   │ │   Backend   │
│        │ │        │ │  Manager  │ │  (extensible)│
└────────┘ └────────┘ └───────────┘ └─────────────┘
```

**Vantaggi:**
- ✅ Open/Closed Principle: Aperto all'estensione, chiuso alla modifica
- ✅ Facile aggiungere nuovi backend
- ✅ Client code non cambia
- ✅ Runtime selection del backend

### 2. Dependency Injection

**Implementazione:** HybridProgressManager inietta il backend appropriato.

```python
# Invece di:
if cloud:
    backend = DatabaseManager()
else:
    backend = ProgressManager()
backend.save()

# Usiamo:
manager = HybridProgressManager()  # Auto-seleziona backend
manager.record_answer()            # Delega automaticamente
```

### 3. Fail-Safe Architecture

**Principio:** L'applicazione deve sempre funzionare, anche in condizioni avverse.

```
Tentativi di Inizializzazione Backend:

1° Tentativo: Cloud Database
   ├─ Successo? → Usa DatabaseManager
   └─ Fallimento? → Prossimo tentativo
                  
2° Tentativo: Local Storage
   ├─ Successo? → Usa ProgressManager
   └─ Fallimento? → Prossimo tentativo
                  
3° Tentativo: Session State (SEMPRE disponibile)
   └─ Usa SessionStateManager
```

**Garanzia:** L'app **non può** fallire l'inizializzazione.

### 4. Single Responsibility Principle

Ogni componente ha una singola responsabilità:

| Componente | Responsabilità |
|------------|----------------|
| EnglishLearning.py | UI e interazione utente |
| HybridProgressManager | Selezione e orchestrazione backend |
| DatabaseManager | Persistenza cloud |
| ProgressManager | Persistenza locale |
| SessionStateManager | Persistenza temporanea |

### 5. Interface Segregation

Tutti i backend implementano la stessa interfaccia minimale:

```python
class ProgressBackendInterface:
    def get_word_stats(self, word: str) -> Tuple[int, int]: pass
    def record_answer(self, word: str, is_correct: bool): pass
    def get_total_stats(self) -> Dict[str, int]: pass
    def get_difficult_words(self, min_attempts: int) -> list: pass
    def reset_all_progress(self): pass
```

Nessun backend è costretto ad implementare metodi che non usa.

## Diagrammi

### Diagramma dei Componenti

```
┌────────────────────────────────────────────────────────┐
│                   Browser Client                       │
│                                                        │
│  ┌──────────────────────────────────────────────┐    │
│  │         Streamlit App UI                     │    │
│  │                                               │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │
│  │  │Flashcard │  │Statistics│  │  Audio   │  │    │
│  │  │Component │  │ Display  │  │  Player  │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  │    │
│  └──────────────────┬────────────────────────────┘    │
│                     │                                  │
└─────────────────────┼──────────────────────────────────┘
                      │
         ┌────────────▼────────────────┐
         │   EnglishLearning.py        │
         │                             │
         │  ┌────────────────────┐    │
         │  │ Business Logic     │    │
         │  │ • File Loading     │    │
         │  │ • Quiz Management  │    │
         │  │ • Answer Validation│    │
         │  └──────────┬─────────┘    │
         │             │               │
         │  ┌──────────▼─────────┐    │
         │  │ External Services  │    │
         │  │ • GoogleTranslator │    │
         │  │ • gTTS             │    │
         │  └────────────────────┘    │
         └──────────┬──────────────────┘
                    │
         ┌──────────▼──────────────────┐
         │ HybridProgressManager       │
         │                             │
         │  Backend Selection Logic    │
         └──────┬───────┬──────┬───────┘
                │       │      │
      ┌─────────▼┐  ┌──▼───┐ ┌▼─────────────┐
      │Database  │  │Prog  │ │SessionState  │
      │Manager   │  │Mgr   │ │Manager       │
      └────┬─────┘  └──┬───┘ └──┬───────────┘
           │           │        │
      ┌────▼─────┐ ┌──▼────┐ ┌─▼──────────┐
      │Supabase  │ │JSON   │ │st.session  │
      │PostgreSQL│ │Files  │ │_state      │
      └──────────┘ └───────┘ └────────────┘
```

### Diagramma Sequenza - Registrazione Risposta

```
User        EnglishLearning    HybridProgress    Backend        Storage
 │                 │                 │              │              │
 ├─Input Answer────►                 │              │              │
 │                 │                 │              │              │
 │                 ├─Validate────────┤              │              │
 │                 │                 │              │              │
 │                 ├─record_answer───►              │              │
 │                 │  (word, true)   │              │              │
 │                 │                 │              │              │
 │                 │                 ├─Delegate─────►              │
 │                 │                 │              │              │
 │                 │                 │              ├─get_stats────►
 │                 │                 │              │              │
 │                 │                 │              ◄─(5,2)────────┤
 │                 │                 │              │              │
 │                 │                 │              ├─save(6,2)────►
 │                 │                 │              │              │
 │                 │                 │              ◄─OK───────────┤
 │                 │                 │              │              │
 │                 │                 ◄─OK───────────┤              │
 │                 │                 │              │              │
 │                 ◄─Stats Updated───┤              │              │
 │                 │                 │              │              │
 │◄─Show Result────┤                 │              │              │
 │   (✅ Correct)  │                 │              │              │
```

### Diagramma Stato - Quiz Flow

```
                   ┌─────────────┐
                   │  START APP  │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │Select File  │
                   │(Excel)      │
                   └──────┬──────┘
                          │
                   ┌──────▼──────────┐
                   │Init Progress    │
                   │Manager          │
                   └──────┬──────────┘
                          │
              ┌───────────▼───────────┐
              │                       │
         ┌────▼────┐           ┌─────▼──────┐
         │Display  │           │Load Word   │
         │Word     │◄──────────┤Stats       │
         └────┬────┘           └────────────┘
              │
              │ User Types Answer
              │
         ┌────▼────┐
         │Validate │
         │Answer   │
         └────┬────┘
              │
         ┌────▼─────────┐
         │              │
    ┌────▼────┐    ┌───▼────┐
    │Correct  │    │Wrong   │
    │✅       │    │❌      │
    └────┬────┘    └───┬────┘
         │             │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │Record       │
         │Answer       │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │Update       │
         │Stats        │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │Show         │
         │Feedback     │
         └──────┬──────┘
                │
         ┌──────▼──────────┐
         │User Action?     │
         └─┬───┬────┬────┬─┘
           │   │    │    │
      Next │   │    │    │ Retry
           │   │    │    │
           └───┼────┼────┼──► (Loop Back)
           Prev│    │Reset
               │    │
               └────┘
```

## Componenti Dettagliati

### EnglishLearning.py

**Responsabilità:**
- Rendering interfaccia utente
- Gestione eventi utente
- Coordinamento servizi esterni
- Logica quiz/flashcard

**Dipendenze Esterne:**
```python
streamlit         # UI Framework
pandas            # Excel parsing
deep_translator   # Google Translate API
gTTS              # Text-to-Speech
```

**Dipendenze Interne:**
```python
hybrid_progress_manager  # Progress tracking
```

**API Esposte:**
```python
def main():
    """Entry point dell'applicazione"""
    
def normalize_text(text: str) -> str:
    """Normalizza testo per comparazione"""
    
def text_to_speech(text: str, lang: str) -> BytesIO:
    """Genera audio dal testo"""
```

**Session State Managed:**
```python
st.session_state = {
    'progress_manager': HybridProgressManager,
    'current_file': str,
    'current_idx': int,
    'show_answer': bool,
    'answer_result': str | None,
    'input_key': int,
    'show_translation': bool,
    'word_order': str
}
```

### HybridProgressManager

**Responsabilità:**
- Selezione automatica backend appropriato
- Delegazione operazioni al backend attivo
- Gestione fallback

**Algoritmo Selezione Backend:**
```python
def _init_backend(self):
    # Priority 1: Cloud Database
    if self._is_cloud_deployment() and self._supabase_available():
        return DatabaseManager()
    
    # Priority 2: Local Files
    if not self._is_cloud_deployment() and self._local_storage_available():
        return ProgressManager()
    
    # Priority 3: Session State (Always works)
    return SessionStateManager()
```

**Detection Cloud Deployment:**
```python
def _is_cloud_deployment(self) -> bool:
    indicators = [
        os.getenv("STREAMLIT_SHARING"),
        hasattr(st, 'secrets') and "SUPABASE_URL" in st.secrets,
        "streamlit.app" in os.getenv("HOSTNAME", ""),
        os.getenv("STREAMLIT_SERVER_HEADLESS") == "true"
    ]
    return any(indicators)
```

**Metodi Delegati:**
- `get_word_stats(word)` → Delega al backend
- `record_answer(word, is_correct)` → Delega al backend
- `get_total_stats()` → Delega al backend
- `get_difficult_words(min_attempts)` → Delega al backend
- `reset_all_progress()` → Delega al backend

### DatabaseManager (Cloud Backend)

**Responsabilità:**
- Connessione a Supabase PostgreSQL
- Operazioni CRUD su tabella progress
- Gestione user_id univoco
- Isolation dati per utente

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

**Operazioni Principali:**

1. **Read (GET)**
```python
def _get_progress_from_cloud(self) -> Dict:
    response = self.supabase_client.table("progress")\
        .select("*")\
        .eq("user_id", self.user_id)\
        .eq("file_name", self.file_name)\
        .execute()
    return self._parse_response(response)
```

2. **Create/Update (UPSERT)**
```python
def _save_progress_to_cloud(self, word, correct, wrong):
    existing = self._check_existing(word)
    if existing:
        self.supabase_client.table("progress")\
            .update({...})\
            .eq("user_id", self.user_id)\
            .eq("word", word)\
            .execute()
    else:
        self.supabase_client.table("progress")\
            .insert({...})\
            .execute()
```

3. **Delete**
```python
def reset_all_progress(self):
    self.supabase_client.table("progress")\
        .delete()\
        .eq("user_id", self.user_id)\
        .eq("file_name", self.file_name)\
        .execute()
```

**Error Handling:**
- Connection errors → Fallback to Session State
- Query errors → Log e notifica utente
- Missing credentials → Graceful degradation

### ProgressManager (Local Backend)

**Responsabilità:**
- Persistenza file JSON locali
- Operazioni su directory UserData/
- File system I/O

**Struttura Directory:**
```
UserData/
├── Words_progress.json
├── Numbers_progress.json
└── [FileName]_progress.json
```

**Formato JSON:**
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

**Operazioni File:**

1. **Load**
```python
def _load_progress(self) -> Dict:
    if os.path.exists(self.progress_file):
        with open(self.progress_file, 'r') as f:
            return json.load(f)
    return {}
```

2. **Save**
```python
def _save_progress(self):
    with open(self.progress_file, 'w') as f:
        json.dump(self.progress, f, indent=2)
```

**Vantaggi:**
- ✅ Zero configurazione
- ✅ Performance eccellenti
- ✅ Persistenza tra sessioni
- ✅ Facile debug (JSON leggibile)

**Svantaggi:**
- ❌ Non multi-utente
- ❌ No sincronizzazione cloud
- ❌ Solo locale

### SessionStateManager (Fallback Backend)

**Responsabilità:**
- Storage in-memory
- Fallback ultimo ricorso
- Garantire funzionamento sempre

**Storage Key:**
```python
storage_key = f"progress_{file_name}"
st.session_state[storage_key] = {
    "word1": {"correct": 5, "wrong": 2},
    ...
}
```

**Caratteristiche:**
- ⚡ Velocissimo (in-memory)
- ✅ Zero dipendenze
- ✅ Sempre disponibile
- ❌ Non persistente

**Uso Tipico:**
- Primo avvio prima setup storage
- Errori backend principali
- Demo/testing rapido

## Flussi Operativi

### Flusso Completo - Prima Sessione

```
1. Utente apre app
   └─> Streamlit inizializza session_state
   
2. Utente seleziona Words.xlsx
   └─> Load Excel con pandas
       └─> Parse: first row = language, rest = words
   
3. Init HybridProgressManager("Words.xlsx")
   └─> _init_backend()
       ├─ Check: is cloud deployment? NO
       ├─ Check: local storage available? YES
       └─> Create ProgressManager instance
           └─> Check: UserData/Words_progress.json exists? NO
               └─> Create empty dict {}
   
4. Display first word
   └─> get_word_stats("hello")
       └─> ProgressManager.get_word_stats("hello")
           └─> Returns: (0, 0) # First time
   
5. User types "ciao" and hits Enter
   └─> Validate: normalize("ciao") == normalize("ciao") ✅
       └─> record_answer("hello", True)
           └─> ProgressManager.record_answer("hello", True)
               └─> Update dict: {"hello": {"correct": 1, "wrong": 0}}
               └─> Save to UserData/Words_progress.json
   
6. Display stats
   └─> get_total_stats()
       └─> Calculate from dict
       └─> Returns: {
           'total_words_practiced': 1,
           'total_correct': 1,
           'total_wrong': 0,
           'accuracy_percentage': 100.0
       }
   
7. User clicks "Next"
   └─> Load next word and repeat from step 4
```

### Flusso - Deployment Cloud con Database

```
1. App deployed on Streamlit Cloud
   └─> Environment variables:
       - STREAMLIT_SHARING = true
       - Secrets configured (SUPABASE_URL, SUPABASE_KEY)
   
2. User opens app
   └─> HybridProgressManager init
       └─> _is_cloud_deployment() → TRUE
       └─> Check Supabase credentials → FOUND
       └─> Create DatabaseManager instance
           └─> Connect to Supabase
           └─> Generate user_id (UUID)
           └─> Store in session_state
   
3. First answer recorded
   └─> record_answer("hello", True)
       └─> DatabaseManager.record_answer()
           └─> Query existing: SELECT * WHERE user_id AND word
           └─> Not found → INSERT
           └─> SQL: INSERT INTO progress VALUES (
               user_id='abc-123',
               file_name='Words.xlsx',
               word='hello',
               correct_count=1,
               wrong_count=0
           )
   
4. User refreshes page
   └─> New session_state
   └─> Same user_id (retrieved from previous session)
   └─> get_word_stats("hello")
       └─> Query: SELECT * WHERE user_id='abc-123' AND word='hello'
       └─> Returns: (1, 0) # Data persisted! ✅
```

### Flusso - Error Recovery

```
Scenario: Database connection fails during session

1. User using DatabaseManager
   └─> Cloud deployment, Supabase configured
   
2. Network issue → Connection lost
   └─> record_answer() called
       └─> DatabaseManager._save_progress_to_cloud()
           └─> Exception: ConnectionError
           └─> Catch exception
           └─> Log error: st.error("Errore salvataggio database")
           └─> Fallback to session state:
               └─> Save in st.session_state.local_progress
   
3. User continues using app
   └─> Data saved in session state temporarily
   └─> Warning shown: "Usando storage temporaneo"
   
4. Connection restored
   └─> Automatic retry on next operation
   └─> Sync data from session state to database (future feature)
```

## Decisioni Architetturali

### ADR-001: Multi-Backend Strategy Pattern

**Context:** Necessità di supportare diversi ambienti (local dev, cloud prod) senza modifiche codice.

**Decision:** Implementare Strategy Pattern con selezione automatica runtime.

**Consequences:**
- ✅ Zero configurazione per utente
- ✅ Stesso codice in tutti gli ambienti
- ✅ Facile aggiungere nuovi backend
- ⚠️ Complessità iniziale aumentata

**Alternatives Considered:**
- ❌ Single backend (troppo rigido)
- ❌ Manual selection (user friction)
- ❌ Separate codebases per ambiente (maintenance nightmare)

### ADR-002: File JSON per Storage Locale

**Context:** Bisogno di persistenza locale semplice e veloce.

**Decision:** Usare file JSON in directory UserData/.

**Consequences:**
- ✅ Human-readable
- ✅ Zero dipendenze (built-in json module)
- ✅ Performance eccellenti per use case
- ⚠️ Non adatto per milioni di records

**Alternatives Considered:**
- ❌ SQLite (overkill per caso d'uso)
- ❌ Pickle (non human-readable)
- ❌ CSV (parsing più complesso)

### ADR-003: Supabase per Cloud Database

**Context:** Necessità database cloud gratuito e facile.

**Decision:** Usare Supabase PostgreSQL.

**Consequences:**
- ✅ Free tier generoso
- ✅ PostgreSQL completo
- ✅ Real-time capabilities (future use)
- ✅ Built-in auth (future use)
- ⚠️ Vendor lock-in

**Alternatives Considered:**
- ❌ Firebase (meno powerful per queries)
- ❌ MongoDB Atlas (learning curve)
- ❌ AWS RDS (not free)

### ADR-004: Streamlit Session State Fallback

**Context:** Garantire app sempre funzionante.

**Decision:** Session State come fallback ultimo.

**Consequences:**
- ✅ Zero point of failure
- ✅ Sempre disponibile
- ✅ No external dependencies
- ⚠️ Dati non persistenti

**Alternatives Considered:**
- ❌ Nessun fallback (app potrebbe rompersi)
- ❌ Error page (poor UX)

### ADR-005: Separate Directory per User Data

**Context:** Non inquinare repository Git con dati utente.

**Decision:** Directory UserData/ in .gitignore.

**Consequences:**
- ✅ Repository pulito
- ✅ Privacy utente
- ✅ File Excel originali immutati
- ✅ Facile backup (copy directory)

**Alternatives Considered:**
- ❌ Modify Excel files (Git pollution)
- ❌ Single file per tutto (hard to manage)
- ❌ Database anche per local (overkill)

## Estensibilità

### Aggiungere Nuovo Backend

Esempio: Redis Cache Backend

```python
# redis_backend.py

import redis
from typing import Dict, Tuple

class RedisBackend:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.redis = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=6379
        )
        self.key_prefix = f"progress:{file_name}:"
    
    def get_word_stats(self, word: str) -> Tuple[int, int]:
        key = f"{self.key_prefix}{word}"
        data = self.redis.hgetall(key)
        return (
            int(data.get(b'correct', 0)),
            int(data.get(b'wrong', 0))
        )
    
    def record_answer(self, word: str, is_correct: bool):
        key = f"{self.key_prefix}{word}"
        field = 'correct' if is_correct else 'wrong'
        self.redis.hincrby(key, field, 1)
    
    # ... altri metodi
```

Poi in `HybridProgressManager`:

```python
def _init_backend(self):
    # Aggiungi dopo cloud check
    if self._redis_available():
        try:
            self.backend = RedisBackend(self.file_name)
            self.backend_type = "redis_cache"
            return
        except Exception as e:
            st.warning(f"Redis fallback: {e}")
    
    # ... resto logica esistente
```

### Metriche e Monitoring

Per aggiungere tracking analytics:

```python
# analytics.py

class AnalyticsTracker:
    def track_answer(self, word, is_correct, time_taken):
        # Invia a Google Analytics, Mixpanel, etc.
        pass
    
    def track_session_duration(self, duration):
        pass

# In HybridProgressManager
def record_answer(self, word, is_correct):
    # Esistente
    self.backend.record_answer(word, is_correct)
    
    # Nuovo: tracking
    if hasattr(self, 'analytics'):
        self.analytics.track_answer(word, is_correct, time_taken)
```

## Performance Considerations

### Benchmarks

**Local JSON Backend:**
- Read operation: ~1ms
- Write operation: ~2ms
- Stats calculation: ~0.5ms per 100 words

**Cloud Database Backend:**
- Read operation: ~50-200ms (network latency)
- Write operation: ~100-300ms
- Stats calculation: ~50ms (server-side)

**Session State Backend:**
- Read operation: ~0.1ms
- Write operation: ~0.1ms
- Stats calculation: ~0.5ms per 100 words

### Ottimizzazioni

1. **Batch Operations (Future)**
```python
def record_answers_batch(self, answers: List[Tuple[str, bool]]):
    # Single transaction per multiple answers
    pass
```

2. **Caching (Future)**
```python
@lru_cache(maxsize=100)
def get_word_stats(self, word: str):
    # Cache results, invalidate on write
    pass
```

3. **Async Operations (Future)**
```python
async def record_answer_async(self, word, is_correct):
    # Non-blocking save for better UX
    pass
```

## Security Considerations

1. **Credentials Management**
   - ✅ Secrets in Streamlit Secrets
   - ✅ Never in code
   - ✅ .gitignore for local secrets

2. **Data Isolation**
   - ✅ User ID per separare dati
   - ✅ RLS in database (optional)
   - ✅ No shared storage

3. **Input Validation**
   - ✅ Text normalization
   - ✅ SQL injection protected (ORM)
   - ✅ File path validation

4. **Rate Limiting (Future)**
   - Limitare API calls
   - Throttling su database operations

---

**Maintained by:** Development Team  
**Last Updated:** 2024  
**Version:** 1.0
