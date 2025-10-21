# Guida al Versionamento

Questo documento spiega come aggiornare la versione del software e mantenere il changelog.

## 📋 Processo di Rilascio

### 1. Aggiornare il File VERSION

Modifica il file `VERSION` con il nuovo numero di versione seguendo il Semantic Versioning:

```
1.0.0  →  1.0.1  (Bug fix)
1.0.0  →  1.1.0  (Nuova feature)
1.0.0  →  2.0.0  (Breaking change)
```

### 2. Aggiornare CHANGELOG.md

Aggiungi una nuova sezione in cima al file CHANGELOG.md:

```markdown
## [1.1.0] - YYYY-MM-DD

### Aggiunto
- Nuova funzionalità X
- Nuova funzionalità Y

### Modificato
- Miglioramento della funzionalità Z

### Corretto
- Bug fix per il problema W
```

### 3. Esempi di Categorie nel Changelog

- **Aggiunto**: Nuove funzionalità
  ```markdown
  - Aggiunta modalità dark mode
  - Supporto per file CSV
  ```

- **Modificato**: Cambiamenti a funzionalità esistenti
  ```markdown
  - Migliorato il design dell'interfaccia utente
  - Ottimizzate le performance del caricamento
  ```

- **Deprecato**: Funzionalità che saranno rimosse
  ```markdown
  - La modalità legacy sarà rimossa nella versione 2.0.0
  ```

- **Rimosso**: Funzionalità eliminate
  ```markdown
  - Rimosso il supporto per Python 3.7
  ```

- **Corretto**: Bug fix
  ```markdown
  - Corretto il crash al caricamento di file vuoti
  - Risolto il problema di visualizzazione su mobile
  ```

- **Sicurezza**: Correzioni di sicurezza
  ```markdown
  - Aggiornata dipendenza X per correggere vulnerabilità CVE-YYYY-XXXXX
  ```

## 🔢 Semantic Versioning

Il formato è: **MAJOR.MINOR.PATCH**

### MAJOR (X.0.0)
Incrementa quando fai cambiamenti incompatibili con versioni precedenti:
- Rimozione di funzionalità pubbliche
- Cambiamenti che richiedono modifiche al codice utente
- Refactoring completo dell'architettura

Esempio: `1.5.3 → 2.0.0`

### MINOR (0.X.0)
Incrementa quando aggiungi nuove funzionalità retrocompatibili:
- Nuove feature
- Nuove opzioni configurabili
- Miglioramenti significativi

Esempio: `1.5.3 → 1.6.0`

### PATCH (0.0.X)
Incrementa per bug fix retrocompatibili:
- Correzioni di bug
- Piccoli miglioramenti
- Aggiornamenti di sicurezza minori

Esempio: `1.5.3 → 1.5.4`

## 📝 Workflow Completo

1. **Sviluppa la feature o correggi il bug**
   ```bash
   git checkout -b feature/nuova-feature
   # ... fai le modifiche ...
   git commit -m "Aggiungi nuova feature"
   ```

2. **Aggiorna VERSION**
   ```bash
   echo "1.1.0" > VERSION
   ```

3. **Aggiorna CHANGELOG.md**
   - Aggiungi la nuova sezione con data e modifiche
   - Classifica i cambiamenti nelle categorie appropriate

4. **Commit e push**
   ```bash
   git add VERSION CHANGELOG.md
   git commit -m "Release version 1.1.0"
   git push
   ```

5. **Crea un tag (opzionale ma raccomandato)**
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

## 🎯 Best Practices

1. **Aggiorna sempre VERSION e CHANGELOG insieme**
2. **Usa date nel formato ISO (YYYY-MM-DD)**
3. **Sii descrittivo nei changelog**
4. **Mantieni un formato consistente**
5. **Documenta anche le breaking changes in modo chiaro**
6. **Testa sempre prima di rilasciare**

## 📚 Riferimenti

- [Keep a Changelog](https://keepachangelog.com/it/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/it/)
