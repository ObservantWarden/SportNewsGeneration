import logging

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


class GeneratorModel:
    def __init__(self):
        self.device = torch.device('cpu:0')
        # Токены
        self.bos_token = '[SN]'
        self.eos_token = '[EN]'

        # Ниже команды для загрузки и инициализации модели и токенизатора.
        model_path = 'Bhgbz/football_hockey_ruGPT3large'

        self.tokenizer = GPT2Tokenizer.from_pretrained(
            model_path,
            bos_token=self.bos_token,
            eos_token=self.eos_token,
            pad_token='[PAD]'
        )
        self.model = GPT2LMHeadModel.from_pretrained(model_path).to(self.device)

    def generate_line(self, text):
        logging.info("TEXT GENERATION STARTED\n")
        # Дополнение текста и его токенизация
        text = self.bos_token + ' ' + text
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to(self.device)

        # Генерация продолжения
        self.model.eval()
        with torch.no_grad():
            out = self.model.generate(input_ids,
                                      do_sample=True,
                                      temperature=1,
                                      pad_token_id=50256,
                                      top_k=40,
                                      top_p=0.7,
                                      max_length=512,
                                      )

        # Вывод ответа
        generated_text = list(map(self.tokenizer.decode, out))[0]
        logging.info("TEXT GENERATED: ", generated_text + "\n")

        if generated_text.find(self.eos_token) != -1:
            return generated_text[6:generated_text.find(self.eos_token)]
        else:
            raise AssertionError("Ошибка генератора текста!")
