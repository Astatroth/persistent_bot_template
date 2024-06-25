import logging
import os
import traceback
from app.StateManager import StateManager
from core import core
from telegram import Update
from telegram.ext import (
    Application,
    CallbackContext,
    ConversationHandler,
    PicklePersistence
)


Config = core.Config()
Logger = core.Logger(Config)
I18n = core.I18n(Config)
StateManager = StateManager()

Logger.get_logger("httpx").setLevel(logging.WARNING)


def main() -> None:
    persistence = PicklePersistence(filepath=os.path.dirname(__file__) + '/storage/persistence/' + Config.BOT_NAME)
    application = Application.builder().token(Config.BOT_TOKEN).persistence(persistence).build()

    async def error_handler(self, update: object, context: CallbackContext) -> int:
        tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
        tb_string = "".join(tb_list)
        self.log.error(msg=f"Exception while handling an update: {tb_string}")

        if isinstance(update, Update):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=self.lang.t("errors.whoops")
            )

        return ConversationHandler.END

    conversation_handler = ConversationHandler(
        entry_points=StateManager.entry_points(),
        states=StateManager.states(),
        fallbacks=StateManager.fallbacks(),
        name=Config.BOT_NAME,
        persistent=True
    )

    application.add_handler(conversation_handler)
    application.add_error_handler(error_handler)

    if Config.APP_ENV == "local":
        application.run_polling()
    else:
        application.run_webhook(
            listen=Config.APP_IP,
            port=Config.APP_PORT,
            url_path=Config.BOT_URL,
            webhook_url=Config.BOT_WEBHOOK_URL
        )


if __name__ == "__main__":
    main()
