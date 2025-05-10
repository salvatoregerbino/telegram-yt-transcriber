# Telegram Bot per la Trascrizione di Video YouTube

## Titolo del Progetto

**Telegram Bot per la Trascrizione di Video YouTube**

## Riepilogo delle Attività Svolte

* **Setup Iniziale e Debug (Completato il 2025-05-06):**
    * Creazione repository GitHub e clonazione locale.
    * Modellazione iniziale del `README.md`.
    * Configurazione ambiente virtuale Python (`venv`) locale.
    * Installazione dipendenze (`python-telegram-bot==22.0`, `pytube`, `python-dotenv`, `certifi`).
    * Creazione file `.env` per token.
    * Sviluppo e debug script `main.py` per:
        * Corretta gestione `if __name__ == '__main__':`.
        * Utilizzo `ApplicationBuilder` e corretta gestione `async/await` per gli handler.
        * Importazioni corrette per la v22.0 di `python-telegram-bot`.
        * Risoluzione errore SSL (lavorando su rete locale).
        * Risoluzione problema di arresto anomalo del bot.
    * Bot di base funzionante: risponde a `/start` e a messaggi di testo, con gestione errori attiva.
    * Codice funzionante committato e unito al branch `main`.

## Task Attuali

* **Implementazione Validazione URL di YouTube (Branch: `feature/validate-youtube-url`):**
    * **Obiettivo:** Modificare la funzione `handle_message` per identificare se un messaggio di testo ricevuto è un URL di YouTube valido.
    * **Metodo:** Utilizzo di espressioni regolari (regex) con il modulo `re` di Python.
    * **Librerie Coinvolte:**
        * `re` (modulo built-in di Python) - [Documentazione Ufficiale `re`](https://docs.python.org/3/library/re.html)

## Prossimi Passi

1.  **Validazione dell'Input Utente:**
    * Modificare `handle_message` per verificare se il testo inviato è un URL di YouTube valido.
2.  **Recupero delle Informazioni dal Video (con `pytube`):**
    * Se l'URL è valido, usare `pytube` per estrarre il titolo del video e, successivamente, l'audio.
3.  **Trascrizione Audio:**
    * Scegliere e integrare un servizio/libreria per la trascrizione audio (es. Whisper, API gratuite/a basso costo).
4.  **Suddivisione in Capitoli e Minutaggio.**
5.  **Formattazione Output.**

---
