# Configurazione Streamlit Cloud

## Per abilitare il database cloud:

1. Vai su https://supabase.com e crea un progetto gratuito
2. Nel tuo progetto Supabase, vai su Settings > API
3. Copia URL e anon key
4. Nel tuo app Streamlit Cloud, aggiungi questi secrets:

```toml
[secrets]
SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_KEY = "eyJ..."
```

## Schema Database (SQL da eseguire in Supabase):

```sql
-- Crea la tabella progress
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

-- Crea un indice per performance
CREATE INDEX idx_progress_user_file 
ON progress(user_id, file_name);

-- Abilita Row Level Security (opzionale ma raccomandato)
ALTER TABLE progress ENABLE ROW LEVEL SECURITY;

-- Policy per permettere agli utenti di vedere solo i loro dati
CREATE POLICY "Users can view own progress" 
ON progress FOR SELECT 
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub');

CREATE POLICY "Users can insert own progress" 
ON progress FOR INSERT 
WITH CHECK (user_id = current_setting('request.jwt.claims', true)::json->>'sub');

CREATE POLICY "Users can update own progress" 
ON progress FOR UPDATE 
USING (user_id = current_setting('request.jwt.claims', true)::json->>'sub');
```

## Modalità di Funzionamento:

### 🏠 Locale (Sviluppo)
- Usa file JSON in `UserData/`
- Dati persistenti tra le sessioni
- Nessuna configurazione necessaria

### ☁️ Cloud (Streamlit Cloud)
- Usa Supabase PostgreSQL
- Dati persistenti globalmente
- Richiede configurazione secrets

### 🔄 Fallback
- Usa Session State di Streamlit
- Dati persi al refresh
- Sempre disponibile come ultima risorsa

## Deployment:

1. **Push del codice su GitHub**
2. **Deploy su Streamlit Cloud**
3. **Configura i secrets** (opzionale per database)
4. **L'app funziona automaticamente!**