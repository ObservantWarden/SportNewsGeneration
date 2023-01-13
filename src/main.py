from Generator import GeneratorModel
from TelegramController import TelegramController

if __name__ == "__main__":
    generator_model = GeneratorModel()
    telegram_controller = TelegramController(generator_model)
    telegram_controller.run()
