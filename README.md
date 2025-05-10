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
      
  * **Troubleshooting Avanzato Validazione URL (2025-05-10):**
        * Sviluppo iniziale del pattern regex per la validazione.
        * Emersione di un comportamento anomalo: l'URL di test `https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58` (inteso come non-YouTube valido) veniva erroneamente identificato come link YouTube.
        * **Indagine Approfondita sulla "Stringa Anomala":**
            * Utilizzo di `test_regex.py` per isolare il problema: si è scoperto che la stringa di test, nonostante apparisse corta con `print()` e `repr()`, aveva `len() == 52`.
            * L'analisi dei caratteri (`ord()`) ha rivelato che la stringa conteneva in realtà un URL YouTube completo e valido: `https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58`. Questo accadeva anche inserendo la stringa manualmente nell'editor `nano`.
            * La costruzione programmatica della stringa "pulita" (es. `https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58`, 42 caratteri) in `test_regex.py` ha confermato il corretto funzionamento del regex (nessun match).
            * Il problema della stringa anomala (52 caratteri, `repr()` fuorviante) è stato replicato anche per i messaggi `update.message.text` ricevuti da Telegram nel bot `main.py`.
            * L'analisi dei caratteri (`ord()`) in `main.py` ha confermato che il bot riceve da Telegram la stringa completa di 52 caratteri. Anche le `entities` del messaggio Telegram indicavano una lunghezza di 52.
            * Un tentativo di "pulizia" della stringa con `string.printable` non ha sortito l'effetto desiderato, poiché tutti i 52 caratteri della stringa anomala sono risultati "stampabili".
        * **Conclusione Attuale:** Il regex e il codice Python del bot funzionano correttamente con i dati che ricevono. La stringa di 52 caratteri `https://www.youtube.com/watch?v=dQw4w9WgXcqqqqq12:58` *è* strutturalmente un link YouTube valido. Il problema principale è capire perché l'input utente, inteso come la versione più corta, arrivi al bot come questa stringa più lunga e completa.
        * **Prossimi Passi (per la stringa anomala):** Indagare il metodo di input dell'utente nel client Telegram (digitazione vs copia-incolla, origine del testo copiato), testare con URL semplici e diversi, e se possibile con client Telegram differenti.
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
