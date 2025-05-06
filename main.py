import logging
import os
from dotenv import load_dotenv
from telegram import Update
# Assicurati che ApplicationBuilder sia importato qui!
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

# Funzione per il comando /start
def start(update: Update, context: CallbackContext) -> None:
    """Invia un messaggio quando viene eseguito il comando /start."""
    user = update.effective_user
    logger.info(f"Comando /start ricevuto da {user.username} ({user.id})")
    update.message.reply_markdown_v2(
        fr'Ciao {user.mention_markdown_v2()}\! Inviami il link di un video YouTube che vuoi trascrivere\.',
    )

# Funzione per gestire i messaggi di testo (che non sono comandi)
def handle_message(update: Update, context: CallbackContext) -> None:
    """Gestisce i messaggi di testo ricevuti."""
    user_message = update.message.text
    logger.info(f"Messaggio ricevuto da {update.effective_user.first_name}: {user_message}")

    # Qui aggiungeremo la logica per validare il link e avviare la trascrizione
    # Per ora, rispondiamo semplicemente confermando la ricezione
    update.message.reply_text(f'Ho ricevuto il tuo messaggio. Analizzerò il link: {user_message}')

# Funzione per gestire gli errori
def error_handler(update: object, context: CallbackContext) -> None:
    """Logga gli Errori causati dagli Update."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # Potresti voler informare l'utente che c'è stato un problema
    # if isinstance(update, Update):
    #     update.message.reply_text("Si è verificato un errore interno. Riprova più tardi.")

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

        #Registra l'handler per i messaggi di testo (usa filters.TEXT e filters.COMMAND)
        logger.debug("Aggiunta handler per messaggi di testo") 
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Registra l'handler per gli errori
        #logger.debug("Aggiunta error handler")
        #application.add_error_handler(error_handler)

        # Avvia il Bot in modalità polling
        logger.info("Bot pronto per avviarsi (run_polling)...")
        application.run_polling()
        logger.info("run_polling terminato.") # Non dovrebbe essere raggiunto facilmente

    except Exception as e:
        logger.exception(f"Errore critico non gestito nella funzione main: {e}")

    logger.debug("Funzione main() terminata.") # Non dovrebbe essere raggiunto facilmente

# Questo blocco è FONDAMENTALE per eseguire il bot!
if __name__ == '__main__':
    # print("DEBUG: Sto per chiamare main()") # Puoi rimuovere o commentare questo print se vuoi
    main()
