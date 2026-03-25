# Guida Utente — AI Red Team Bot

## Sommario
- [Introduzione](#introduzione)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Esecuzione e Opzioni CLI](#esecuzione-e-opzioni-cli)
- [Output e Report](#output-e-report)
- [FAQ e Troubleshooting](#faq-e-troubleshooting)
- [Guida Sviluppatore Plugin](#guida-sviluppatore-plugin)

---

## Introduzione
AI Red Team Bot è uno strumento avanzato per penetration test automatizzati, pensato per ambienti enterprise e laboratori. Permette scansioni multi-target, analisi vulnerabilità, exploit non distruttivi e generazione di report professionali.

---

## Installazione
1. Clona la repository
2. Installa le dipendenze Python:
    ```bash
    pip install -r requirements.txt
    ```
3. (Opzionale) Crea un ambiente virtuale Python

---

## Configurazione
Puoi personalizzare porte, servizi e path comuni tramite un file YAML:

```yaml
ports:
   - 21
   - 22
   - 80
port_service_map:
   "21": "ftp"
   "22": "ssh"
common_paths:
   - /robots.txt
   - /admin
```
Passa il file con `--config config.yaml`.

---

## Esecuzione e Opzioni CLI
Esempio base:
```bash
python PhantomStrike_AI.py 192.168.1.10 -o pdf json
```
Opzioni principali:
- `--config config.yaml` — Configurazione personalizzata
- `--targets 192.168.1.1,example.com` — Multi-target
- `--output pdf json` — Formati di output
- `--plugins-dir plugins` — Directory plugin custom

---

## Output e Report
Il tool genera:
- Report PDF professionale con sommario, dettagli tecnici, raccomandazioni e grafici
- Export JSON machine-readable per SIEM/tool

---

## FAQ e Troubleshooting
**Q: Il tool non trova porte aperte, cosa posso fare?**
A: Verifica che il target sia raggiungibile e che non ci siano firewall/blocchi di rete.

**Q: Come aggiungo nuove porte o servizi?**
A: Modifica il file YAML di configurazione e riavvia il tool.

**Q: Come estendo il tool con nuovi exploit o scanner?**
A: Vedi la sezione sviluppatore qui sotto.

---

# Guida Sviluppatore Plugin

## Struttura di un Plugin
Un plugin è un file Python nella cartella `plugins/` che implementa una funzione `register(bot)`.

Esempio base:
```python
def register(bot):
      def custom_scanner(target):
            # ...logica custom...
            return {"result": "ok"}
      bot.register_scanner("custom_scan", custom_scanner)
```

## API disponibili per i plugin
- `register_exploit(nome, funzione)`
- `register_scanner(nome, funzione)`
- `run_exploit(nome, ...)`
- `run_scanner(nome, ...)`

## Debug e test plugin
- Usa i log per tracciare errori (`logger`)
- Riavvia il tool dopo aver aggiunto nuovi plugin

---

## Contatti e Supporto
Per richieste avanzate o bug, apri una issue su GitHub o contatta il maintainer.
# AI RED TEAM BOT — Enterprise Penetration Testing Assistant

**Versione 2.0**

> ⚠️ **DISCLAIMER:** Questo tool è destinato **ESCLUSIVAMENTE** ad ambienti autorizzati, laboratori interni, CTF e test di sicurezza con esplicita autorizzazione. L'uso su sistemi non autorizzati è **ILLEGALE** e punito dalla legge.

---

## 1. Descrizione

AI Red Team Bot è un framework modulare di penetration testing automatizzato, progettato per assistere security analyst e red teamer durante attività di vulnerability assessment in ambienti aziendali controllati.

Il bot esegue un flusso completo di pen testing in 6 fasi:

1. Port Scanning asincrono con banner grabbing
2. Analisi approfondita delle vulnerabilità con fingerprinting
3. Scoring AI con prioritizzazione automatica
4. Test exploit non distruttivi (safe mode)
5. Persistenza risultati su database SQLite
6. Generazione report PDF + JSON

---

## 2. Caratteristiche principali

### 2.1 Input Validation & IP Scope Detection
- Validazione rigorosa del target (IP o dominio)
- Sanitizzazione contro injection (caratteri speciali bloccati)
- Validazione formato IP tramite modulo `ipaddress`
- Regex validation per hostname/domini
- Rilevamento automatico IP privato vs pubblico:
  - IP privati (10.x, 172.16-31.x, 192.168.x, 127.x): log info
  - IP pubblici: avviso giallo evidenziato per confermare autorizzazione
  - Hostname: risoluzione DNS automatica prima del check

### 2.2 Port Scanning Avanzato
- Scansione asincrona (`asyncio`) per massima velocità
- 20 porte monitorate: 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017
- Banner grabbing automatico per identificazione versioni
- Timeout configurabile per ogni connessione (anche da CLI)

**Servizi coperti:** FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, IMAP, HTTPS, SMB, IMAPS, POP3S, MySQL, RDP, PostgreSQL, VNC, Redis, HTTP-Alt, HTTPS-Alt, MongoDB

### 2.3 Analisi Vulnerabilità Profonda
- Rilevamento automatico di vulnerabilità per ogni servizio esposto
- HTTP: fingerprinting server, rilevamento tecnologie, verifica security headers mancanti (CSP, HSTS, X-Frame-Options, ecc.)
- HTTPS/SSL: verifica certificato (scadenza, CN mismatch, protocolli deprecati TLS 1.0/1.1)
- SSH: rilevamento versioni obsolete (OpenSSH 4/5/6)
- Database: rilevamento esposizione MySQL, PostgreSQL, MongoDB, Redis
- Classificazione severità: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**, **INFO**

### 2.4 AI Scoring Engine
Il motore AI calcola un punteggio (0-15) per ogni vulnerabilità basandosi su feature extraction multi-fattore:

```
Score = (Base_Severity × Service_Risk_Factor) + Banner_Bonus + Exposed_Bonus
```

- Peso severità base (CRITICAL=10, HIGH=7.5, MEDIUM=5, LOW=2.5)
- Fattore di rischio specifico del servizio (es. SMB=1.5, Telnet=1.5)
- Bonus banner (+2.0 se rileva versioni note come vulnerabili)
- Bonus esposizione (+1.5 per database/accesso remoto su Internet)

Le vulnerabilità vengono ordinate per score decrescente, permettendo di concentrare l'attenzione sulle minacce più critiche.

### 2.5 Safe Exploit Engine
Test non distruttivi eseguiti in safe mode:
- FTP Anonymous Login: tenta login con credenziali anonymous
- HTTP Reachability: verifica status code e redirect
- Directory Enumeration: scansione di 12 path comuni sensibili (`/robots.txt`, `/.env`, `/admin`, `/wp-admin`, `/.git/HEAD`, `/phpmyadmin`, `/server-status`, `/api`, `/swagger`, `/graphql`, `/login`, `/sitemap.xml`)
- SSL/TLS Audit: verifica certificati e protocolli
- SMTP Open Relay: test EHLO + VRFY per enumerazione utenti
- Redis No-Auth: test connessione senza password (PING)
- MongoDB No-Auth: test connessione non autenticata

**Test solo informativi:** SSH (solo banner), Telnet (avviso non cifrato), SMB/RDP (segnalazione esposizione)

**Rate limiting:** pausa configurabile (default 0.3s) tra ogni richiesta HTTP per evitare di triggerare WAF/IDS sul target.

### 2.6 Report PDF Professionale
- 5 sezioni: Executive Summary, Porte Aperte e Banner, Vulnerabilità Rilevate, Risultati Exploit, Raccomandazioni
- Formato: A4, tabelle con stile professionale, colori per severità
- Nome file: `report_<target>_<timestamp>.pdf`

### 2.7 Export JSON (Machine-Readable)
- Export parallelo in formato JSON per integrazione automatizzata
- Metadata, phase timings, open ports, vulnerabilities, exploits, summary
- Ideale per SIEM, CI/CD, dashboard
- Nome file: `report_<target>_<timestamp>.json`

### 2.8 Database e Logging
- SQLite con due tabelle: `scan_sessions` e `results`
- Ogni scan crea una sessione tracciata con timestamp, metriche totali e durata
- Ogni vulnerabilità/exploit è salvato con: porta, servizio, banner, severità, AI score, risultato exploit, dettagli, timestamp
- Connessioni DB gestite con context manager (nessun leak)
- Log su file (`redteam.log`) e console con colori ANSI

### 2.9 Output Colorato
- Log nel terminale con colori ANSI per severità e fasi
- CRITICAL/ERROR: rosso, HIGH: rosso chiaro, MEDIUM/WARNING: giallo, LOW: ciano, INFO: verde, DEBUG: grigio
- Sommario finale con riepilogo evidenziato
- File di log (`redteam.log`) senza codici colore per leggibilità

### 2.10 Gestione Interruzioni (Ctrl+C)
- Signal handler per SIGINT (Ctrl+C) garantisce chiusura pulita
- La sessione DB viene chiusa correttamente anche in caso di abort
- Messaggio di conferma chiusura prima dell'exit
- Exit code 130 (standard per SIGINT)

### 2.11 Timing e Performance
- Ogni fase dello scan è cronometrata individualmente
- I tempi vengono mostrati nel log e inclusi nel report JSON
- Il sommario finale include la durata totale dello scan
- La durata viene salvata anche nella sessione DB

---

## 3. Requisiti

- Python 3.8 o superiore
- Librerie Python (vedi `requirements.txt`):
  - `reportlab >= 4.0` (generazione PDF)
  - `requests >= 2.31` (richieste HTTP)
  - `urllib3 >= 2.0` (gestione connessioni)
- Librerie standard: `argparse`, `asyncio`, `ftplib`, `json`, `logging`, `re`, `signal`, `smtplib`, `socket`, `sqlite3`, `ssl`, `sys`, `time`, `datetime`, `ipaddress`

---

## 4. Installazione

1. Clona o scarica il progetto:
   ```sh
   git clone <repository_url>
   cd PhantomStrike_AI
   ```
2. Crea un virtual environment (consigliato):
   ```sh
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```
3. Installa le dipendenze:
   ```sh
   pip install -r requirements.txt
   ```

---

## 5. Utilizzo

### 5.1 Modalità interattiva (senza argomenti)
```sh
python PhantomStrike_AI.py
```
Il bot mostrerà un banner e chiederà di inserire il target.

### 5.2 Modalità CLI con argomenti
```sh
# Scan base con report PDF
python PhantomStrike_AI.py 192.168.1.100

# Scan con output PDF + JSON
python PhantomStrike_AI.py 192.168.1.100 -o pdf json

# Solo output JSON
python PhantomStrike_AI.py example.com -o json

# Timeout personalizzati
python PhantomStrike_AI.py 10.0.0.1 --timeout 5 --http-timeout 10

# Rate limiting custom (1 secondo tra richieste)
python PhantomStrike_AI.py target.local --rate-limit 1.0

# Modalità silenziosa
python PhantomStrike_AI.py 192.168.1.1 -q

# Modalità debug/verbose
python PhantomStrike_AI.py 192.168.1.1 -v
```

### 5.3 Argomenti CLI completi
| Argomento         | Descrizione                         | Default        |
|-------------------|-------------------------------------|---------------|
| target            | IP o dominio da scansionare         | (interattivo) |
| -o, --output      | Formati output: pdf, json           | pdf           |
| --timeout         | Timeout connessione porte (sec)     | 3             |
| --http-timeout    | Timeout richieste HTTP (sec)        | 5             |
| --rate-limit      | Pausa tra richieste HTTP (sec)      | 0.3           |
| -q, --quiet       | Solo errori e risultati finali      | off           |
| -v, --verbose     | Output debug dettagliato            | off           |
| -h, --help        | Mostra help e esce                  | —             |

### 5.4 Esempio di output (con colori)
```
╔══════════════════════════════════════════════════════════╗
║       AI Red Team Bot — Enterprise Pen Test Assistant   ║
║       ⚠️  SOLO per ambienti autorizzati / lab           ║
╚══════════════════════════════════════════════════════════╝

Inserisci target (IP o dominio): 192.168.1.100

[INFO] Avvio scan su 192.168.1.100
[INFO] Target 192.168.1.100 è un IP privato (rete locale/lab).
[INFO] Fase 1: Port Scanning + Banner Grabbing...
[INFO] Porte aperte: [22, 80, 443] (3.12s)
[INFO] Fase 2: Analisi Vulnerabilità...
[INFO] Vulnerabilità rilevate: 5 (1.45s)
[INFO] Fase 3: AI Scoring e Prioritizzazione...
[INFO]   [HIGH] Score 7.5: Server HTTP esposto
[INFO]   [MEDIUM] Score 5.0: SSH esposto - rischio bruteforce
[INFO] Fase 4: Safe Exploit Testing...
[INFO] Exploit completati: 2 successi / 5 test (4.23s)
[INFO] Fase 5: Salvataggio risultati...
[INFO] Fase 6: Generazione Report...
[INFO]   PDF: report_192_168_1_100_20260323_103011.pdf
[INFO]   JSON: report_192_168_1_100_20260323_103011.json
[INFO]
[INFO] ============================================================
[INFO]  SCAN COMPLETATO
[INFO] ============================================================
[INFO]   Target:         192.168.1.100
[INFO]   Sessione:       #1
[INFO]   Porte aperte:   3
[INFO]   Vulnerabilità:  5
[INFO]   Exploit OK:     2
[INFO]   Durata totale:  9.15s
[INFO]   File generati:  report_192.168.1.100_20260323.pdf, ...json
[INFO] ============================================================
```

### 5.5 File generati
- `report_<target>_<timestamp>.pdf`   → Report PDF professionale
- `report_<target>_<timestamp>.json`  → Export JSON machine-readable
- `redteam.db`                        → Database SQLite con storico
- `redteam.log`                       → Log di tutte le operazioni

---

## 6. Struttura del progetto

```
PhantomStrike_AI/
├── PhantomStrike_AI.py      → Script principale (single-file architecture)
├── requirements.txt       → Dipendenze Python
├── Descrizione.txt        → Descrizione sintetica del progetto
├── README.txt             → Questa documentazione
├── README_IT.md           → Documentazione (Markdown)
│
│  [Generati a runtime:]
├── redteam.db             → Database SQLite (sessioni e risultati)
├── redteam.log            → Log delle operazioni
├── report_*.pdf           → Report PDF generati
└── report_*.json          → Export JSON generati
```

---

## 7. Architettura dei moduli

```
┌─────────────────┐
│   CLI PARSER    │  → argparse: target, output, timeout, rate-limit
│  + VALIDATION   │    + validazione input + IP scope detection
└────────┬────────┘
         │
┌────────▼────────┐
│ SIGNAL HANDLER  │  → Ctrl+C graceful shutdown, chiusura sessione DB
└────────┬────────┘
         │
┌────────▼────────┐
│ PORT SCANNER    │  → Scansione asincrona + banner grabbing (con timing)
│ (asyncio)       │
└────────┬────────┘
         │
┌────────▼────────┐
│ VULNERABILITY   │  → Analisi profonda: HTTP headers, SSL certs,
│    ANALYZER     │    version detection, fingerprinting
└────────┬────────┘    (con rate limiting tra richieste HTTP)
         │
┌────────▼────────┐
│   AI SCORING    │  → Feature extraction multi-fattore,
│    ENGINE       │    scoring 0-15, ordinamento per priorità
└────────┬────────┘
         │
┌────────▼────────┐
│  SAFE EXPLOIT   │  → FTP anon, HTTP dirs, SSL audit, SMTP VRFY,
│    ENGINE       │    Redis/MongoDB no-auth (con rate limiting)
└────────┬────────┘
         │
┌────────▼────────┐
│   DATABASE      │  → SQLite con context manager: sessioni + risultati
│   (SQLite)      │
└────────┬────────┘
         │
┌────────▼────────┐
│  REPORT GEN     │  → PDF (5 sezioni, tabelle, raccomandazioni)
│  PDF + JSON     │    JSON (machine-readable per SIEM/automazione)
└────────┘
```

---

## 8. Configurazione

### 8.1 Costanti nel codice
Le costanti principali sono definite in cima al file `PhantomStrike_AI.py`:
- `TARGET_PORTS`      → Lista porte da scansionare (modificabile)
- `PORT_SERVICE_MAP`  → Mapping porta → nome servizio
- `DB_NAME`           → Nome file database SQLite (default: redteam.db)
- `SCAN_TIMEOUT`      → Timeout connessione in secondi (default: 3)
- `HTTP_TIMEOUT`      → Timeout richieste HTTP in secondi (default: 5)
- `HTTP_RATE_LIMIT`   → Pausa tra richieste HTTP (default: 0.3s)

Per aggiungere porte personalizzate, modificare `TARGET_PORTS` e `PORT_SERVICE_MAP` nel file sorgente.

### 8.2 Override da CLI
Tutti i timeout e il rate limit sono sovrascrivibili da riga di comando:
- `--timeout 5`          → sovrascrive SCAN_TIMEOUT
- `--http-timeout 10`    → sovrascrive HTTP_TIMEOUT
- `--rate-limit 1.0`     → sovrascrive HTTP_RATE_LIMIT

---

## 9. Sicurezza e Limitazioni

### Misure di sicurezza implementate
- Validazione input rigorosa (blocco caratteri shell injection)
- Rilevamento e avviso per target su IP pubblico
- Query SQL parametrizzate (nessuna concatenazione diretta)
- Connessioni DB con context manager (nessun leak)
- Eccezioni specifiche (no bare except)
- Exploit solo in safe mode (non distruttivi)
- Rate limiting per evitare detection da WAF/IDS
- Gestione Ctrl+C con chiusura pulita sessione DB
- Logging completo per audit trail

### Limitazioni attuali
- Single-threaded per gli exploit (scan è asincrono)
- Nessun supporto per autenticazione target (proxy, credenziali)
- AI scoring basato su regole statiche (non machine learning)
- Nessun modulo per fuzzing o injection testing attivo

---

## 10. Roadmap — Sviluppi futuri

### Breve termine
- [ ] Modalità multi-target (scansione batch da file)
- [ ] Configurazione da file YAML/TOML
- [ ] Export CSV per fogli di calcolo

### Medio termine
- [ ] Machine Learning per scoring predittivo
- [ ] Modulo Nmap integration per deep scanning
- [ ] Modulo directory bruteforce (wordlist-based)
- [ ] API REST per integrazione con SIEM
- [ ] Dashboard web (Flask/FastAPI) per monitoraggio

### Lungo termine
- [ ] AI predittiva basata su storico attacchi
- [ ] Integrazione con MITRE ATT&CK framework
- [ ] Plugin system per moduli custom
- [ ] Supporto scanning reti (CIDR ranges)
- [ ] Integrazione con Metasploit/Burp Suite API
- [ ] Report multi-formato (HTML, DOCX, Markdown)

---

## 11. Changelog

### v2.0 (23/03/2026)
**Nuove funzionalità:**
- Interfaccia CLI completa con argparse (target, -o, --timeout, ecc.)
- Export JSON machine-readable per integrazione SIEM
- Rate limiting configurabile tra richieste HTTP
- Timing per ogni fase dello scan (con output e salvataggio)
- Test SMTP open relay safe (EHLO + VRFY)
- Output colorato nel terminale (ANSI colors)
- Rilevamento automatico IP privato/pubblico con avviso
- Gestione Ctrl+C con chiusura pulita sessione DB
- Sommario finale con riepilogo completo dello scan

**Miglioramenti:**
- Connessioni DB con context manager (no memory leak)
- Rimosso import inutilizzato
- Tabella scan_sessions con campo duration_seconds

### v1.0 (21/03/2026)
**Nuove funzionalità:**
- Validazione input con sanitizzazione target
- Gestione errori con eccezioni specifiche
- Banner grabbing su tutte le porte
- Analisi profonda: HTTP fingerprinting, SSL check, version detection
- 20 porte monitorate (da 4 originali)
- AI Scoring Engine multi-fattore (score 0-15)
- Safe Exploit Engine: FTP anon, HTTP dirs, SSL audit, Redis, MongoDB
- Report PDF professionale con 5 sezioni e tabelle
- Database SQLite con sessioni e risultati dettagliati
- Logging su file e console

### v0.1 (Versione originale MVP)
- Port scan basico su 4 porte (21, 22, 80, 443)
- Analisi vulnerabilità superficiale
- Report PDF minimale
- Database SQLite base

---

## 12. Licenza e responsabilità

Questo software è fornito "as is" senza garanzie di alcun tipo. L'autore non è responsabile per usi impropri o non autorizzati.

L'utilizzo di questo tool su sistemi senza esplicita autorizzazione scritta del proprietario costituisce reato informatico ed è punibile ai sensi di legge (Art. 615-ter Codice Penale italiano e normative internazionali equivalenti).

**Usare ESCLUSIVAMENTE per:**
- Penetration test autorizzati con contratto/autorizzazione
- Laboratori interni di sicurezza informatica
- Competizioni CTF (Capture The Flag)
- Ricerca e formazione in cybersecurity

---

## 13. Contatti e contributi

Per segnalazioni, suggerimenti o contributi al progetto, aprire una issue o pull request sul repository.

Buon hacking (etico)! 🛡️

---

## 14. Uso avanzato, API e sistema plugin

### 14.1 Configurazione YAML (esempio)
Puoi sovrascrivere porte, servizi e path comuni tramite file YAML:

```yaml
ports:
   - 21
   - 22
   - 80
port_service_map:
   "21": "ftp"
   "22": "ssh"
common_paths:
   - /robots.txt
   - /admin
```
Esegui con:
```sh
python PhantomStrike_AI.py --config config.yaml
```

### 14.2 Supporto multi-lingua
Seleziona la lingua a runtime (default: italiano):
```sh
python PhantomStrike_AI.py --lang en
```
Per aggiungere una lingua, crea un file `messages_xx.py` (vedi `messages_en.py`, `messages_it.py`).

### 14.3 Sistema plugin (locale e remoto)
Un plugin è un file Python in `plugins/` che implementa una funzione `register(bot)`. Esempio:
```python
def register(bot):
      def custom_scanner(target):
            # ...logica custom...
            return {"result": "ok"}
      bot.register_scanner("custom_scan", custom_scanner)
```
API disponibili per i plugin:
- `register_exploit(nome, funzione)`
- `register_scanner(nome, funzione)`
- `run_exploit(nome, ...)`
- `run_scanner(nome, ...)`

**Plugin remoti/live:** Posiziona i file plugin su repo remoto o URL, poi usa `--plugins-url <url>` per caricarli a runtime (hot-reload supportato).

### 14.4 REST API (opzionale)
Se abilitata, il bot espone un server FastAPI per controllo remoto e integrazione:
```sh
python PhantomStrike_AI.py --api
```
Consulta l'endpoint `/docs` per OpenAPI schema e uso.

### 14.5 Integrazione CI/CD
Il progetto include workflow GitHub Actions per test automatici e quality check. Vedi badge CI in cima al README.

### 14.6 Logging, caching, rate limiting
- **Logging:** Tutte le azioni sono loggate su `redteam.log` e console (livello configurabile, output colorato).
- **Caching:** Scan porte e info HTTP sono cache-izzati per performance e per evitare richieste duplicate.
- **Rate limiting:** Pausa configurabile tra richieste HTTP per evitare trigger WAF/IDS.

### 14.7 Internazionalizzazione (i18n)
Tutti i messaggi sono localizzati. Per aggiungere una lingua:
1. Copia `messages_en.py` in `messages_xx.py`.
2. Traduci tutte le stringhe.
3. Usa `--lang xx` a runtime.

---
