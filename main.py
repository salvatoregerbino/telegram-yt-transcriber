import logging
import os
import re # Import per le espressioni regolari
from dotenv import load_dotenv
from telegram import Update
# Assicurati che ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext siano importati
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Abilita il logging per vedere errori e informazioni (lasciamo DEBUG per ora)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Carica le variabili d'ambiente dal file .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Funzione per il comando /start (asincrona)
async def start(update: Update, context: CallbackContext) -> None:
    """Invia un messaggio quando viene eseguito il comando /start."""
    user = update.effective_user
    logger.info(f"Comando /start ricevuto da {user.username} ({user.id})")
    await update.message.reply_markdown_v2(
        fr'Ciao {user.mention_markdown_v2()}\! Inviami il link di un video YouTube che vuoi trascrivere\.',
    )

# Funzione per gestire i messaggi di testo (che non sono comandi) (asincrona)
async def handle_message(update: Update, context: CallbackContext) -> None:
    """Gestisce i messaggi di testo ricevuti e valida gli URL di YouTube."""
    user_message = update.message.text
    user = update.effective_user # Corretto da 'update.effective_user.first_name' a 'user' per coerenza
    logger.info(f"Messaggio ricevuto da {user.first_name}: {user_message}") # Usiamo user.first_name qui per il log

 # Pattern Regex per URL di YouTube (ulteriore revisione)
    youtube_regex = (
        r'^(?:https?:\/\/)?(?:www\.|m\.)?'
        r'(?:'  # Inizio del gruppo principale di alternative
            # Alternativa 1: youtube.com con percorsi specifici
            r'youtube\.com\/(?:watch\?v=|embed\/|live\/|v\/|shorts\/)([a-zA-Z0-9_-]{11})'  # Gruppo di cattura 1 per l'ID
            r'|'  # OR
            # Alternativa 2: youtu.be
            r'youtu\.be\/([a-zA-Z0-9_-]{11})'  # Gruppo di cattura 2 per l'ID
        r')'  # Fine del gruppo principale di alternative
        r'(?:\S*)?$'  # Permette caratteri aggiuntivi (parametri) fino alla fine
    )

    match = re.search(youtube_regex, user_message)
    video_id = None # Inizializziamo video_id a None

    if match:
        # Controlliamo quale gruppo ha catturato l'ID
        # match.group(1) corrisponde all'ID dei link youtube.com
        # match.group(2) corrisponde all'ID dei link youtu.be
        video_id = match.group(1) if match.group(1) else match.group(2)

    if video_id: # Se video_id è stato trovato (non è più None)
        logger.info(f"URL di YouTube valido rilevato da {user.first_name}. ID Video: {video_id}")
        await update.message.reply_text(
            f"URL di YouTube valido rilevato! (ID: {video_id}).\n"
            "Prossimo passo: estrarre informazioni e audio..."
        )
    else: # Se match è None OPPURE se video_id è rimasto None (non dovrebbe succedere se match è vero con questo regex)
        logger.info(f"Messaggio da {user.first_name} non è un URL YouTube valido: {user_message}")
        await update.message.reply_text(
            "Il messaggio non sembra essere un link di YouTube valido. "
            "Per favore, invia un link corretto (es. https://www.youtube.com/watch?v=VIDEO_ID)."
        )

# Funzione per gestire gli errori (asincrona)
async def error_handler(update: object, context: CallbackContext) -> None:
    """Logga gli Errori causati dagli Update."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # Potresti voler informare l'utente che c'è stato un problema
    # if isinstance(update, Update) and hasattr(update, 'message'):
    #     await update.message.reply_text("Si è verificato un errore interno. Riprova più tardi.")

def main() -> None:
    """Avvia il bot."""
    logger.debug("Funzione main() iniziata.")

    if TOKEN is None:
        logger.error("Errore: Il token del bot non è stato trovato. Assicurati che sia nel file .env")
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

        # Registra l'handler per gli errori (ANCORA COMMENTATO, come da ultimo test di stabilità)
        # logger.debug("Aggiunta error handler")
        # application.add_error_handler(error_handler)

        # Avvia il Bot in modalità polling
        logger.info("Bot pronto per avviarsi (run_polling) CON CommandHandler e MessageHandler...")
        application.run_polling()
        logger.info("run_polling terminato.") # Non dovrebbe essere raggiunto facilmente

    except Exception as e:
        logger.exception(f"Errore critico non gestito nella funzione main: {e}")

    logger.debug("Funzione main() terminata.") # Non dovrebbe essere raggiunto facilmente

# Questo blocco è FONDAMENTALE per eseguire il bot!
if __name__ == '__main__':
    # print("DEBUG: Sto per chiamare main()") # Puoi rimuovere o commentare questo
    main()
