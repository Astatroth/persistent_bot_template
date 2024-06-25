from app.State import State
from telegram import Update
from telegram.ext import CallbackContext


class MainController:
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Hola!")

        return State.STEP_1

    @staticmethod
    async def step_1(update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Step 1")

        return State.STEP_2

    @staticmethod
    async def step_2(update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Step 2")

        return State.STEP_3

    @staticmethod
    async def step_3(update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Step 3")

        return State.STEP_1
