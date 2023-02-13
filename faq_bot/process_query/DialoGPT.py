from urllib import response
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class generalQuery:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        self.responces = []


    def callDialoGPT(self, query):
        input_ids = self.tokenizer.encode(query + self.tokenizer.eos_token, return_tensors = 'pt') # new_input
        history = input_ids # DialoGPT can also take history dialogs, right now it is same as input 

        output = self.model.generate(history, max_length = 100, pad_token_ids = self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        self.responces.append(response)
        return response


def get_general_responce(query):
    general_bot = generalQuery()
    responce = general_bot.callDialoGPT(query)

    return responce



