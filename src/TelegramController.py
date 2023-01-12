import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import ConversationHandler, MessageHandler
from telegram.ext import filters
from Generator import GeneratorModel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TelegramController:
    def __init__(self, generator: GeneratorModel):
        self.__get_line = 1
        self.__hello_line = "Здравствуйте! Меня зовут Георгий. Я буду вашим спортивным редактором на сегодня." \
                            " Пожалуйста, введите мне статью, а я за вас её допишу"
        self.__wait_line = "Подождите, сейчас я соображу что-нибудь умное..."
        self.__error_line = "У нас ошибочка! Обратитесь ко мне через время, когда меня подлечат"
        self.generator = generator
        self.application = ApplicationBuilder().token('SECURED TOKEN').build()
        start_handler = CommandHandler('start', self.start)

        generate_answer_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.reply)

        conversation_entry_points = [start_handler]
        main_conversation = ConversationHandler(
            entry_points=conversation_entry_points,
            states={
                self.__get_line: [generate_answer_handler]
            },
            fallbacks=[],
        )

        self.application.add_handler(main_conversation)

    def run(self):
        self.application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=self.__hello_line)
        return self.__get_line

    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        article = update.message.text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.__wait_line
        )
        try:
            result_line = self.generator.generate_line(article)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=result_line)
        except AssertionError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=self.__error_line
            )
        return ConversationHandler.END
