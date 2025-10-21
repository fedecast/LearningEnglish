# ⚡ Quick Start - English Learning App

Guida rapida per iniziare in 5 minuti.

## 📦 Installazione Rapida

### Opzione 1: Usa l'App Online (Più Veloce)

1. Vai all'URL dell'app deployata
2. Inizia subito a studiare!

### Opzione 2: Esegui Localmente

```bash
# 1. Clone repository
git clone https://github.com/fedecast/LearningEnglish.git
cd LearningEnglish

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Avvia app
streamlit run EnglishLearning.py
```

App disponibile su: `http://localhost:8501`

## 🚀 Primo Utilizzo

### Step 1: Carica un File

Due opzioni:

**A. Usa file dalla libreria** (Raccomandato)
```
📂 Scegli un file: [Words.xlsx ▼]
```

**B. Carica tuo file**
```
📁 Carica il tuo file Excel: [Sfoglia...]
```

### Step 2: Configura

```
Lingua risposta: [Italian ▼]  ← Lingua in cui risponderai
Ordine parole:   [Casuale ▼]  ← Casuale o Sequenziale
```

### Step 3: Studia!

1. **Leggi** la parola mostrata
2. **Digita** la traduzione
3. **Premi** Invio
4. **Ricevi** feedback immediato (✅/❌)

## 💡 Tips Essenziali

### Per Principianti

1. **Inizia con "Words.xlsx"** (vocabolario base)
2. **Usa ordine Sequenziale** prima volta
3. **Clicca 🔊 Ascolta** per pronuncia
4. **Non usare "Mostra"** troppo presto (almeno 2-3 tentativi)

### Per Utenti Avanzati

1. **Modalità Casuale** per sfida extra
2. **Monitora statistiche** in tempo reale
3. **Focus su parole difficili** (vedi Statistiche Avanzate)
4. **Crea file personalizzati** per argomenti specifici

## 📊 Monitorare Progresso

### Statistiche in Tempo Reale

Visibili in alto:
```
📊 42 parole • 156✅ • 38❌ • 80.4%
```

### Statistiche Dettagliate

Click su "📊 Statistiche Avanzate" per:
- Metriche complete
- Top 5 parole difficili
- Opzione reset

## 📄 Creare Tuo File Excel

### Formato Richiesto

```
Colonna A:
─────────────
english       ← Riga 1: lingua
hello         ← Riga 2+: parole
goodbye
thank you
```

### Steps

1. Apri Excel/Google Sheets
2. Colonna A, Riga 1: `english` o `italian`
3. Colonna A, Riga 2+: Le tue parole
4. Salva come `.xlsx`
5. Carica nell'app

## 🎯 Workflow Consigliato

### Sessione Giornaliera (15 min)

```
1. Apri app
   ↓
2. Seleziona file corrente
   ↓
3. Studia 10-20 parole
   ↓
4. Controlla statistiche
   ↓
5. Ripassa parole difficili
   ↓
6. Chiudi app (progresso salvato!)
```

### Piano Settimanale

- **Lun-Mer-Ven**: Nuovo materiale (Words.xlsx)
- **Mar-Gio**: Ripasso parole difficili
- **Sab**: Test completo (modalità casuale)
- **Dom**: Riposo o leggero ripasso

## ⚙️ Configurazione Opzionale

### Setup Completo (Con Database Cloud)

Per progresso persistente online:

1. **Crea account Supabase** (gratuito)
   - Vai su [supabase.com](https://supabase.com)
   - Crea nuovo progetto

2. **Configura database**
   - Esegui SQL da `DEPLOYMENT.md`

3. **Aggiungi secrets su Streamlit Cloud**
   ```toml
   SUPABASE_URL = "https://xxx.supabase.co"
   SUPABASE_KEY = "your-key"
   ```

4. **Deploy!**

## 🆘 Risoluzione Problemi Rapida

### Problema: File non caricabile

✅ **Soluzione:** Verifica formato
- Una sola colonna
- Prima riga = lingua
- Tipo file .xlsx

### Problema: Audio non funziona

✅ **Soluzione:** 
- Controlla connessione internet
- Verifica volume dispositivo
- Permetti audio nel browser

### Problema: Statistiche perse al refresh

✅ **Soluzione:**
- **Locale**: Normale, dati in UserData/
- **Cloud senza DB**: Usa Supabase per persistenza
- **Temporaneo**: Accettabile per testing

### Problema: App lenta

✅ **Soluzione:**
- Connessione internet lenta (traduzioni online)
- Chiudi tab inutilizzate
- Usa file più piccoli (<50 parole)

## 📚 Documentazione Completa

Per informazioni dettagliate:

- **README.md** - Panoramica completa
- **USER_GUIDE.md** - Guida utente approfondita
- **ARCHITECTURE.md** - Architettura tecnica
- **DEVELOPER_GUIDE.md** - Guida sviluppatori
- **DEPLOYMENT.md** - Guida deployment cloud

## 🎓 Risorse di Apprendimento

### File Excel Disponibili

| File | Contenuto | Difficoltà |
|------|-----------|------------|
| Words.xlsx | Vocabolario base inglese | ⭐ Facile |
| Numbers.xlsx | Numeri in inglese | ⭐ Facile |
| Numeri.xlsx | Numeri in italiano | ⭐ Facile |

### Creare File Personalizzati

**Idee per file:**
- `Basic_Verbs.xlsx` - Verbi comuni
- `Travel_Phrases.xlsx` - Frasi per viaggi
- `Business_English.xlsx` - Inglese business
- `Food_Vocabulary.xlsx` - Cibo e cucina
- `Colors_Animals.xlsx` - Colori e animali

## ⏱️ Benchmark Performance

### Quanto tempo serve?

| Attività | Tempo |
|----------|-------|
| Installazione locale | 2-3 minuti |
| Prima sessione studio | 15 minuti |
| Studiare 20 parole | 10-15 minuti |
| Ripassare parole difficili | 5 minuti |
| Setup database cloud | 15-20 minuti |

### Obiettivi Realistici

- **Settimana 1**: 50 parole nuove, 70% precisione
- **Settimana 2**: 100 parole totali, 80% precisione
- **Settimana 3**: 150 parole totali, 85% precisione
- **Mese 1**: 200+ parole, 90% precisione

## 🎯 Next Steps

Dopo aver completato questa guida:

1. ✅ **Installa e avvia l'app**
2. ✅ **Completa prima sessione** (10 parole)
3. ✅ **Monitora statistiche**
4. 📖 **Leggi USER_GUIDE.md** per funzionalità avanzate
5. 🚀 **Crea routine di studio quotidiana**

## 🤝 Supporto

**Hai domande?**

- 📖 Consulta [USER_GUIDE.md](USER_GUIDE.md)
- 🐛 Apri [GitHub Issue](https://github.com/fedecast/LearningEnglish/issues)
- 💬 Contatta maintainers

---

**Buono Studio! 📚🎓**

*La consistenza è la chiave del successo. Inizia oggi!*
