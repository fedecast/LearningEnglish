# 📚 Guida Utente - English Learning App

Guida completa all'utilizzo dell'applicazione per l'apprendimento dell'inglese.

## Indice

- [Introduzione](#introduzione)
- [Primi Passi](#primi-passi)
- [Interfaccia Utente](#interfaccia-utente)
- [Funzionalità](#funzionalità)
- [Modalità di Studio](#modalità-di-studio)
- [Statistiche e Progresso](#statistiche-e-progresso)
- [Gestione File](#gestione-file)
- [Tips e Trucchi](#tips-e-trucchi)
- [FAQ](#faq)
- [Risoluzione Problemi](#risoluzione-problemi)

## Introduzione

**English Learning App** è un'applicazione web per l'apprendimento delle lingue attraverso il metodo delle flashcard digitali. L'app ti aiuta a:

- 📖 Memorizzare nuove parole
- 🎯 Migliorare la precisione delle traduzioni
- 📊 Monitorare i tuoi progressi
- 🔊 Imparare la pronuncia corretta
- 🎓 Identificare le parole difficili da ripassare

## Primi Passi

### Accesso all'App

1. **Locale (Sviluppo)**
   ```bash
   streamlit run EnglishLearning.py
   ```
   L'app si aprirà su `http://localhost:8501`

2. **Online (Produzione)**
   - Vai all'URL fornito (es: https://yourapp.streamlit.app)
   - Nessuna registrazione richiesta
   - Inizia subito a studiare

### Prima Sessione di Studio

1. **Carica un File**
   - Usa il menu a tendina "📂 Scegli un file dalla cartella Files:"
   - Oppure carica il tuo file con "📁 Carica il tuo file Excel"

2. **Configura Preferenze**
   - Seleziona lingua delle risposte (English/Italian)
   - Scegli ordine parole (Casuale/Sequenziale)

3. **Inizia a Studiare**
   - Leggi la parola mostrata
   - Digita la traduzione
   - Premi Invio per verificare

## Interfaccia Utente

### Layout Principale

```
┌──────────────────────────────────────┐
│    🎯 English Learning App           │
├──────────────────────────────────────┤
│                                      │
│  📂 Scegli file: [Words.xlsx ▼]     │
│  📁 Carica file: [Sfoglia...]        │
│                                      │
│  Lingua risposta: [Italian ▼]       │
│  Ordine parole:   [Casuale ▼]       │
│                                      │
├──────────────────────────────────────┤
│  📊 Statistiche: 42 parole • 156✅  │
│                  38❌ • 80.4%        │
├──────────────────────────────────────┤
│                                      │
│        ┌──────────────────┐          │
│        │     HELLO        │          │
│        └──────────────────┘          │
│                                      │
│  📈 Questa parola: ✅5 • ❌2         │
│                                      │
│  🔊 [Ascolta]                        │
│                                      │
│  La tua traduzione: _______________  │
│                                      │
│  [⬅️ Precedente]  [➡️ Prossima]     │
│  [🔄 Riprova] [👁️ Mostra] [🔁 Reset]│
│                                      │
└──────────────────────────────────────┘
```

### Elementi dell'Interfaccia

#### 1. Header
- **Titolo App**: Nome e logo dell'applicazione
- **File Selector**: Seleziona file dalla libreria
- **File Uploader**: Carica i tuoi file personalizzati

#### 2. Configurazione
- **Lingua Risposta**: Inglese o Italiano
- **Ordine Parole**: Casuale o Sequenziale

#### 3. Statistiche Globali (Banner Superiore)
```
📊 Statistiche: 42 parole • 156✅ • 38❌ • 80.4%
```
- **Parole praticate**: Numero totale parole studiate
- **Corrette (✅)**: Risposte corrette totali
- **Errate (❌)**: Risposte errate totali
- **Precisione (%)**: Percentuale di accuratezza

#### 4. Card Parola
```
┌──────────────────┐
│     HELLO        │
└──────────────────┘
```
Grande e leggibile, con sfondo grigio chiaro.

#### 5. Statistiche Parola
```
📈 Questa parola: ✅5 • ❌2 • Tentativi: 7
```
Mostra le tue performance sulla parola corrente.

#### 6. Controlli Audio
- **🔊 Ascolta**: Riproduce la pronuncia della parola

#### 7. Input Risposta
```
La tua traduzione in italian: _________________
                             (Scrivi qui...)
```
Campo di testo per inserire la tua risposta.

#### 8. Feedback Visivo
- **✅ CORRETTO!** (Verde): Risposta corretta
- **❌ ERRATO** (Rosso): Risposta errata

#### 9. Pulsanti Navigazione
- **⬅️ Precedente**: Parola precedente
- **➡️ Prossima**: Parola successiva
- **🔄 Riprova**: Riprova la stessa parola
- **👁️ Mostra traduzione**: Rivela la risposta
- **🔁 Reinizia**: Torna alla prima parola

#### 10. Statistiche Avanzate (Expander)
Clicca su "📊 Statistiche Avanzate" per vedere:
- Metriche dettagliate
- Top 5 parole difficili
- Pulsante reset progresso

## Funzionalità

### 1. Caricamento File

#### Opzione A: File dalla Libreria
1. Usa il menu "📂 Scegli un file dalla cartella Files:"
2. Seleziona uno dei file disponibili:
   - **Words.xlsx**: Vocabolario inglese base
   - **Numbers.xlsx**: Numeri in inglese
   - **Numeri.xlsx**: Numeri in italiano
   - **Unknown.xlsx**: Set personalizzato

#### Opzione B: File Personalizzato
1. Clicca su "📁 Carica il tuo file Excel"
2. Seleziona file .xlsx o .xls dal tuo computer
3. Il file deve seguire il formato richiesto (vedi sezione Gestione File)

### 2. Studio delle Parole

#### Workflow Base
```
1. Leggi la parola → 2. Pensa alla traduzione
    ↓
3. Digita risposta → 4. Premi Invio
    ↓
5. Ricevi feedback → 6. Vai alla prossima
    ↓
    └──────────────────┘ (Loop)
```

#### Metodi di Verifica
- **Invio**: Premi Enter dopo aver digitato
- **Normalizzazione**: Maiuscole/minuscole e spazi ignorati
- **Confronto**: Risposta confrontata con traduzione Google

### 3. Audio e Pronuncia

#### Come Usare l'Audio
1. Clicca sul pulsante **🔊 Ascolta**
2. Attendi il caricamento (~1 secondo)
3. L'audio si riproduce automaticamente
4. Ripeti per ascoltare di nuovo

#### Supporto Lingue
- **Inglese**: Pronuncia americana standard
- **Italiano**: Pronuncia italiana standard

### 4. Navigazione tra Parole

#### Modalità Casuale
- Parole mostrate in ordine random
- Migliore per varietà e sorpresa
- Previene memorizzazione dell'ordine

#### Modalità Sequenziale
- Parole in ordine del file Excel
- Migliore per studio sistematico
- Facile sapere dove sei

#### Controlli Navigazione
- **➡️ Prossima**: Prossima parola (casuale o sequenziale)
- **⬅️ Precedente**: Parola precedente
- **🔁 Reinizia**: Torna all'inizio

### 5. Sistema di Aiuto

#### Durante lo Studio
1. **🔄 Riprova**: Reset input, riprova stesso quiz
2. **👁️ Mostra traduzione**: Rivela risposta corretta
3. **🔊 Ascolta**: Pronuncia per aiuto contestuale

#### Quando Usare gli Aiuti
- **Riprova**: Hai fatto un errore di battitura
- **Mostra**: Dopo 2-3 tentativi falliti
- **Ascolta**: Non ricordi la parola, ascolta per aiuto

## Modalità di Studio

### 1. Studio Sistematico (Sequenziale)

**Quando usarlo:**
- Primo contatto con nuovo vocabolario
- Vuoi coprire tutto il materiale
- Preferisci ordine prevedibile

**Come impostare:**
1. Ordine parole: **Sequenziale**
2. Inizia dalla prima parola
3. Procedi in ordine fino alla fine

**Pro:**
- ✅ Nessuna parola saltata
- ✅ Facile riprendere dove hai lasciato
- ✅ Senso di progressione

**Contro:**
- ⚠️ Può diventare noioso
- ⚠️ Memorizzazione dell'ordine

### 2. Studio Variato (Casuale)

**Quando usarlo:**
- Ripasso di parole già studiate
- Vuoi maggiore sfida
- Evitare monotonia

**Come impostare:**
1. Ordine parole: **Casuale**
2. Ogni click "Prossima" = parola random

**Pro:**
- ✅ Varietà e sorpresa
- ✅ Previene memorizzazione ordine
- ✅ Più coinvolgente

**Contro:**
- ⚠️ Potresti vedere stessa parola ripetuta
- ⚠️ Difficile tracciare copertura

### 3. Studio Intensivo (Parole Difficili)

**Quando usarlo:**
- Prima di un test/esame
- Hai parole con bassa precisione
- Vuoi migliorare punti deboli

**Come fare:**
1. Apri "📊 Statistiche Avanzate"
2. Guarda sezione "🔴 Parole da ripassare"
3. Annota le top 5 parole difficili
4. Studia quelle specificamente

**Esempio:**
```
🔴 Parole da ripassare
1. **difficult** - Errori: 80% (8/10)
2. **necessary** - Errori: 75% (6/8)
3. **enough** - Errori: 66% (4/6)
```

### 4. Sessioni Brevi (Pomodoro)

**Tecnica:**
1. Imposta timer per 25 minuti
2. Studia intensamente senza distrazioni
3. Break 5 minuti
4. Ripeti

**Ottimale per:**
- Mantenere concentrazione
- Evitare affaticamento
- Massimizzare retention

## Statistiche e Progresso

### Metriche Disponibili

#### 1. Statistiche Globali (Sempre Visibili)
```
📊 42 parole praticate • 156✅ • 38❌ • 80.4%
```
- **Parole praticate**: Quante parole uniche hai studiato
- **Corrette**: Totale risposte corrette
- **Errate**: Totale risposte errate
- **Precisione**: (Corrette / Totale) × 100

#### 2. Statistiche per Parola
```
📈 Questa parola: ✅5 • ❌2 • Tentativi: 7
```
Mostra le tue performance sulla parola corrente.

#### 3. Statistiche Avanzate

**Metriche:**
- Parole Praticate (valore assoluto)
- Risposte Corrette (valore assoluto)
- Risposte Errate (valore assoluto)
- Precisione (percentuale)

**Top 5 Parole Difficili:**
Lista ordinata delle parole con più errori.

Algoritmo:
```
Parola considerata difficile se:
- Tentativi totali ≥ 3
- Errori > Risposte Corrette

Ordinamento: Per tasso di errore (Errori / Totale)
```

### Interpretare le Statistiche

#### Precisione Target
- **90-100%**: Eccellente! Pronto per materiale avanzato
- **80-89%**: Buono. Continua così
- **70-79%**: Discreto. Ripassa parole difficili
- **60-69%**: Sufficiente. Focus su ripasso
- **< 60%**: Necessario più studio

#### Strategia Basata su Statistiche

**Se Precisione Alta (>85%):**
1. Aggiungi nuovo vocabolario
2. Usa modalità casuale
3. Aumenta velocità di risposta

**Se Precisione Media (70-85%):**
1. Ripassare parole difficili
2. Usare aiuti audio
3. Studiare in sessioni più brevi

**Se Precisione Bassa (<70%):**
1. Tornare a modalità sequenziale
2. Studiare 5-10 parole alla volta
3. Ripetere più volte stessa parola

### Reset Progresso

#### Quando Resettare
- Vuoi ricominciare da zero
- Hai finito tutto il vocabolario
- Vuoi testare apprendimento effettivo

#### Come Resettare
1. Apri "📊 Statistiche Avanzate"
2. Scorri in basso
3. Clicca "🔄 Reset Progresso Completo"
4. Conferma

⚠️ **Attenzione**: Azione irreversibile! Tutti i dati saranno persi.

## Gestione File

### Formato File Richiesto

#### Struttura Excel
```
┌─────────────────┐
│   Colonna A     │  ← UNICA COLONNA
├─────────────────┤
│   english       │  ← Riga 1: Lingua
├─────────────────┤
│   hello         │  ← Riga 2+: Parole
│   goodbye       │
│   thank you     │
│   please        │
│   ...           │
└─────────────────┘
```

#### Regole Formato
1. **Solo 1 colonna**: Esattamente 1 colonna di dati
2. **Prima riga**: "english" o "italian" (lowercase)
3. **Altre righe**: Una parola/frase per riga
4. **Tipo file**: .xlsx o .xls

### Creare un Nuovo File

#### Metodo 1: Excel / LibreOffice

```
1. Apri Excel
2. Colonna A, Riga 1: Scrivi "english"
3. Colonna A, Riga 2+: Scrivi le parole
4. Salva come: File → Salva con nome → .xlsx
```

#### Metodo 2: Google Sheets

```
1. Apri Google Sheets
2. Colonna A, Riga 1: Scrivi "italian"
3. Colonna A, Riga 2+: Scrivi le parole
4. Download: File → Scarica → .xlsx
```

#### Metodo 3: Python Script

```python
import pandas as pd

# Crea DataFrame
words = ["english", "hello", "goodbye", "thank you"]
df = pd.DataFrame(words)

# Salva Excel
df.to_excel("MyWords.xlsx", index=False, header=False)
```

### Errori Comuni

#### ❌ Errore: "Il file deve avere UNA sola colonna"

**Causa:** File ha più colonne.

**Soluzione:**
1. Apri file in Excel
2. Seleziona colonna A
3. Copia tutto (Ctrl+C)
4. Nuovo file
5. Incolla in colonna A
6. Salva

#### ❌ Errore: Traduzione non corretta

**Causa:** Google Translate non disponibile.

**Soluzione:**
- Clicca "👁️ Mostra traduzione" per vedere risposta
- Controlla connessione internet
- Riprova dopo qualche secondo

### Best Practices File

1. **Nomi File Descrittivi**
   ```
   ✅ Basic_Verbs.xlsx
   ✅ Travel_Vocabulary.xlsx
   ❌ file1.xlsx
   ❌ untitled.xlsx
   ```

2. **Organizzazione per Tema**
   ```
   Animals.xlsx
   Colors.xlsx
   Food.xlsx
   Numbers.xlsx
   ```

3. **Dimensioni Ottimali**
   - Minimo: 10 parole
   - Ottimale: 20-50 parole per file
   - Massimo: 100 parole (per singola sessione)

4. **Evitare Duplicati**
   - Una parola una volta per file
   - Usa file diversi per contesti diversi

## Tips e Trucchi

### 🎯 Massimizzare l'Apprendimento

1. **Spaced Repetition**
   - Studia 20 parole oggi
   - Ripassa domani
   - Ripassa dopo 3 giorni
   - Ripassa dopo 1 settimana

2. **Context Matter**
   - Non solo parole singole
   - Includi frasi comuni
   - Usa esempi nel file Excel

3. **Audio è Fondamentale**
   - Ascolta SEMPRE la pronuncia
   - Ripeti ad alta voce
   - Registrati e confronta

4. **Consistenza > Intensità**
   - 15 minuti al giorno > 2 ore una volta
   - Meglio sessioni brevi e frequenti
   - Crea una routine

### ⚡ Trucchi Interfaccia

1. **Keyboard Shortcuts**
   - `Enter`: Verifica risposta
   - `Tab`: Naviga tra elementi

2. **Mobile-Friendly**
   - L'app funziona su smartphone
   - Pulsanti grandi per touch
   - Layout responsive

3. **Multi-Tab**
   - Apri più tab per confrontare
   - Un tab per file diverso
   - Sincronizzazione automatica

### 📊 Ottimizzare Statistiche

1. **Non Imbrogliare**
   - Non usare "Mostra" subito
   - Prova almeno 2-3 volte
   - Statistiche accurate = progresso reale

2. **Review Regolare**
   - Controlla statistiche settimanalmente
   - Identifica pattern
   - Adatta strategia

3. **Goal Setting**
   ```
   Settimana 1: Raggiungere 70% precisione
   Settimana 2: 80% precisione
   Settimana 3: 90% precisione
   Settimana 4: 95% precisione + nuovo file
   ```

## FAQ

### Generale

**Q: L'app è gratuita?**  
A: Sì, completamente gratuita e open-source.

**Q: Serve registrazione?**  
A: No, inizia subito senza account.

**Q: I miei dati sono salvati?**  
A: Sì, localmente o nel cloud (dipende da deployment).

**Q: Posso usare offline?**  
A: Solo se esegui localmente. Online serve connessione.

### Funzionalità

**Q: Quante parole posso studiare?**  
A: Illimitate! Carica quanti file vuoi.

**Q: Posso studiare altre lingue oltre inglese?**  
A: Sì, il sistema supporta qualsiasi lingua di Google Translate.

**Q: Come cambio la lingua di risposta?**  
A: Usa il menu "Scegli la lingua della risposta".

**Q: Posso studiare in entrambe le direzioni?**  
A: Sì! Crea due file: uno "english", uno "italian".

### Tecnico

**Q: Quali browser sono supportati?**  
A: Chrome, Firefox, Safari, Edge (moderni).

**Q: L'audio non funziona, perché?**  
A: Controlla:
- Connessione internet
- Volume dispositivo
- Permessi browser per audio

**Q: Le statistiche sono perse al refresh?**  
A: Dipende:
- Locale: Salvate in UserData/
- Cloud senza DB: Perse al refresh
- Cloud con DB: Persistenti

**Q: Posso esportare le statistiche?**  
A: Non ancora, feature futura.

### Problemi Comuni

**Q: "Errore nel caricamento del file"**  
A: Verifica formato file (1 colonna, prima riga lingua).

**Q: "Impossibile ottenere traduzione"**  
A: Google Translate temporaneamente non disponibile. Usa "Mostra traduzione".

**Q: Le statistiche sembrano sbagliate**  
A: Reset: Statistiche Avanzate → Reset Progresso Completo.

## Risoluzione Problemi

### Problema: App Non Si Avvia (Locale)

**Sintomi:** Errore all'avvio di `streamlit run`

**Soluzioni:**
```bash
# 1. Verifica installazione
pip list | grep streamlit

# 2. Reinstalla dipendenze
pip install -r requirements.txt

# 3. Controlla versione Python
python --version  # Deve essere 3.8+

# 4. Riavvia da zero
pip install --upgrade streamlit
streamlit run EnglishLearning.py
```

### Problema: File Non Caricabile

**Sintomi:** "Errore nel caricamento del file"

**Checklist:**
- [ ] File ha estensione .xlsx o .xls?
- [ ] File ha UNA sola colonna?
- [ ] Prima riga è "english" o "italian"?
- [ ] File non è corrotto?

**Test:**
```python
import pandas as pd
df = pd.read_excel("YourFile.xlsx", header=None)
print(df.head())  # Controlla struttura
```

### Problema: Audio Non Funziona

**Sintomi:** Pulsante "Ascolta" non produce suono

**Soluzioni:**
1. **Controlla Connessione**
   - gTTS richiede internet
   - Prova aprire google.com

2. **Verifica Permessi Browser**
   - Chrome: Impostazioni → Sito → Autorizzazioni → Audio
   - Firefox: Permessi sito → Audio

3. **Test Audio Browser**
   - Apri YouTube
   - Se funziona, problema è app-specific

4. **Riavvia Browser**
   - Chiudi tutti i tab
   - Riapri app

### Problema: Statistiche Non Salvate

**Sintomi:** Al refresh, statistiche azzerate

**Causa:** Backend Session State (temporaneo)

**Verifica Backend:**
1. Apri "ℹ️ Info Storage"
2. Controlla "storage_type"

**Soluzioni:**
- **Locale**: Backend dovrebbe essere "Local Files"
  ```bash
  # Verifica UserData/ esiste
  ls UserData/
  ```
- **Cloud**: Configura Supabase se vuoi persistenza

### Problema: App Lenta

**Sintomi:** Lentezza generale, lag

**Cause Possibili:**
1. **Connessione Lenta**
   - Traduzioni richiedono internet
   - Audio richiede download

2. **File Troppo Grande**
   - File >100 parole può essere lento
   - Dividi in file più piccoli

3. **Browser Occupato**
   - Troppe tab aperte
   - Chiudi tab inutilizzati

**Ottimizzazioni:**
```bash
# Cache del browser
# Chrome: Ctrl+Shift+Delete → Svuota cache

# Riavvia app
# Ctrl+C (stop) → streamlit run EnglishLearning.py
```

### Supporto

**Non trovi la soluzione?**

1. **GitHub Issues**
   - Apri issue su: [github.com/fedecast/LearningEnglish/issues](https://github.com/fedecast/LearningEnglish/issues)
   - Fornisci: OS, browser, messaggio errore, screenshot

2. **Email**
   - Contatta via GitHub profile

3. **Documentation**
   - Leggi README.md
   - Consulta ARCHITECTURE.md per dettagli tecnici

---

**Happy Learning! 🎓**

*Ricorda: La consistenza è la chiave. 15 minuti al giorno portano risultati straordinari!*
