import logging
import os
import re
import string # <-- MODIFICA: Aggiunto import necessario
from dotenv import load_dotenv
from telegram import Update, constants # <-- MODIFICA: Aggiunto constants per ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Configurazione del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
# MODIFICA: Silenzia i log troppo verbosi di httpx e httpcore a livello DEBUG
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Carica le variabili d'ambiente dal file .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Funzione per il comando /start (asincrona)
async def start(update: Update, context: CallbackContext) -> None:
    """Invia un messaggio quando viene eseguito il comando /start."""
    user = update.effective_user
    logger.info(f"Comando /start ricevuto da {user.username} ({user.id})")
    # MODIFICA: Assicurato l'uso corretto di MarkdownV2 e user.mention_markdown_v2()
    await update.message.reply_text(
        f"Ciao {user.mention_markdown_v2()}\\! Inviami il link di un video YouTube che vuoi trascrivere\\.",
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

# Funzione per gestire i messaggi di testo (che non sono comandi) (asincrona)
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Gestisce i messaggi di testo ricevuti, pulisce l'input e valida gli URL di YouTube."""
    user_message_original = update.message.text # Messaggio originale come ricevuto
    user = update.effective_user
    logger.info(f"Messaggio ORIGINALE ricevuto da {user.first_name}: '{user_message_original}' (len: {len(user_message_original)}) (repr: {repr(user_message_original)})")

# --- Blocco per Analisi Caratteri user_message_original ---
    logger.debug("--- Character Analysis for user_message_original from Telegram ---")
    char_details_telegram = []
    try:
        for i, char_in_string in enumerate(user_message_original):
            char_details_telegram.append(f"Idx {i}: '{repr(char_in_string)}' Ord: {ord(char_in_string)} Hex: {hex(ord(char_in_string))}")
        # Stampa i dettagli dei caratteri, 3 per riga per leggibilità se sono molti
        for i in range(0, len(char_details_telegram), 3):
            logger.debug(" | ".join(char_details_telegram[i:i+3]))
    except Exception as e: # Questa era la riga 52, ora dovrebbe essere indentata correttamente
        logger.error(f"Errore durante l'analisi dei caratteri di user_message_original: {e}")
    logger.debug(f"Length of user_message_original (post-analysis): {len(user_message_original)}")
    logger.debug(f"repr(user_message_original) (post-analysis): {repr(user_message_original)}")
    logger.debug("--- End Character Analysis ---")
    # --- Fine Blocco Analisi Caratteri ---

    # MODIFICA CHIAVE: "Pulizia" della stringa di input
    user_message_pulito = "".join(filter(lambda x: x in string.printable, user_message_original))
    
    logger.info(f"Messaggio PULITO per regex: '{user_message_pulito}' (len: {len(user_message_pulito)}) (repr: {repr(user_message_pulito)})")

    # Pattern Regex per URL di YouTube
    youtube_regex = (
        r'^(?:https?:\/\/)?(?:www\.|m\.)?'
        r'(?:'
            r'youtube\.com\/(?:watch\?v=|embed\/|live\/|v\/|shorts\/)([a-zA-Z0-9_-]{11})'
            r'|'
            r'youtu\.be\/([a-zA-Z0-9_-]{11})'
        r')'
        r'(?:\S*)?$'
    )
    
    logger.debug(f"Using regex pattern: '{youtube_regex}'")
    
    # MODIFICA: Usa user_message_pulito per la ricerca con il regex
    match = re.search(youtube_regex, user_message_pulito) 
    video_id = None

    if match:
        video_id = match.group(1) if match.group(1) else match.group(2)
        logger.info(f"URL di YouTube valido rilevato (da stringa pulita) da {user.first_name}. ID Video: {video_id}")
        await update.message.reply_text(
            f"URL di YouTube valido rilevato! (ID: {video_id}).\n"
            "Prossimo passo: estrarre informazioni e audio..."
        )
    else:
        logger.info(f"Messaggio (stringa pulita) da {user.first_name} NON è un URL YouTube valido: '{user_message_pulito}'")
        await update.message.reply_text(
            "Il messaggio non sembra essere un link di YouTube valido. "
            "Per favore, invia un link corretto (es. https://www.youtube.com/watch?v=VIDEO_ID)."
        )

# Funzione per gestire gli errori (asincrona)
async def error_handler(update: object, context: CallbackContext) -> None:
    """Logga gli Errori causati dagli Update."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # È buona norma informare l'utente, ma assicurati che 'update' sia del tipo corretto
    if isinstance(update, Update) and update.message:
        try:
            await update.message.reply_text("Si è verificato un errore interno. Il team di sviluppo è stato notificato.")
        except Exception as e:
            logger.error(f"Errore durante l'invio del messaggio di errore all'utente: {e}")

def main() -> None:
    """Avvia il bot."""
    logger.debug("Funzione main() iniziata.")

    if TOKEN is None:
        logger.critical("ERRORE: Il token del bot non è stato trovato. Assicurati che TELEGRAM_BOT_TOKEN sia impostato nel file .env e che il file .env sia nella stessa directory di main.py")
        return

    logger.debug("Token caricato correttamente.")

    try:
        logger.debug("Inizio creazione ApplicationBuilder...")
        application = ApplicationBuilder().token(TOKEN).build()
        logger.debug("ApplicationBuilder creato con successo.")

        # Registra gli handler per i comandi
        logger.debug("Aggiunta handler per /start")
        application.add_handler(CommandHandler("start", start))

        # Registra l'handler per i messaggi di testo
        logger.debug("Aggiunta handler per messaggi di testo")
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # MODIFICA: Registra l'handler per gli errori (ora ATTIVO)
        logger.debug("Aggiunta error handler")
        application.add_error_handler(error_handler)

        # Avvia il Bot in modalità polling
        logger.info("Bot pronto per avviarsi (run_polling)...")
        application.run_polling()
        # Le righe seguenti verranno eseguite solo se run_polling termina (es. con un segnale di stop)
        logger.info("run_polling terminato.")

    except Exception as e:
        logger.critical(f"Errore critico non gestito all'avvio o durante l'esecuzione del bot: {e}", exc_info=True)

    logger.debug("Funzione main() terminata (o interrotta).")

if __name__ == '__main__':
    main()
