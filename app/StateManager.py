from app.controllers.MainController import MainController
from app.State import State
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)


class StateManager:
    def __init__(self):
        pass

    @staticmethod
    def end():
        return ConversationHandler.END

    @staticmethod
    def entry_points() -> list:
        return [
            CommandHandler("start", MainController.start)
        ]

    @staticmethod
    def fallbacks() -> list:
        return []

    @staticmethod
    def states() -> dict:
        return {
            State.STEP_1: [MessageHandler(filters.ALL, MainController.step_1)],
            State.STEP_2: [MessageHandler(filters.ALL, MainController.step_2)],
            State.STEP_3: [MessageHandler(filters.ALL, MainController.step_3)],
        }
