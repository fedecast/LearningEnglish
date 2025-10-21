# Changelog

Tutte le modifiche importanti a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [1.0.0] - 2025-10-21

### Aggiunto
- **Sistema di Progresso Ibrido**: Implementato sistema di tracciamento con supporto per database cloud (Supabase), file locali e session state
- **Statistiche in Tempo Reale**: Visualizzazione delle statistiche di apprendimento con contatori per risposte corrette ed errate
- **Gestione Multi-File**: Supporto per caricamento e selezione di più file Excel dalla cartella Files
- **Traduzione Automatica**: Integrazione con Google Translator per traduzioni automatiche
- **Text-to-Speech**: Funzionalità di pronuncia delle parole con gTTS
- **Modalità di Apprendimento**: 
  - Ordine casuale o sequenziale delle parole
  - Verifica automatica delle risposte
  - Sistema di feedback visivo per risposte corrette/errate
- **Statistiche Avanzate**:
  - Contatori globali di precisione
  - Statistiche per singola parola
  - Identificazione delle parole più difficili
  - Funzione di reset del progresso
- **Interfaccia Mobile-Friendly**: Design ottimizzato per dispositivi mobili con CSS responsive
- **Sistema di Deployment Flessibile**: Tre modalità di deployment (Base, Standard, Premium)

### Caratteristiche Tecniche
- Architettura ibrida per persistenza dati (Cloud/Locale/Session)
- Gestione automatica dei fallback tra i sistemi di storage
- File di progresso separati per ogni file Excel
- Directory UserData esclusa da Git per privacy
- Supporto per deployment su Streamlit Cloud

### Documentazione
- README.md per introduzione al progetto
- DEPLOYMENT.md per istruzioni di deployment
- PROGRESS_SYSTEM.md per dettagli sul sistema di progresso

---

## Come interpretare questo changelog

- **Aggiunto**: Nuove funzionalità
- **Modificato**: Cambiamenti a funzionalità esistenti
- **Deprecato**: Funzionalità che saranno rimosse in versioni future
- **Rimosso**: Funzionalità rimosse
- **Corretto**: Bug fix
- **Sicurezza**: Correzioni relative alla sicurezza

## Formato delle versioni

Il progetto utilizza [Semantic Versioning](https://semver.org/lang/it/):
- **MAJOR**: Cambiamenti incompatibili con versioni precedenti
- **MINOR**: Nuove funzionalità retrocompatibili
- **PATCH**: Bug fix retrocompatibili
