# This file connects the frontend, backend and model 
# This file will take the query and process it with knowledge 

import os
import sys
from .server import generate_more_responces, get_responce

os.environ['CUDA_VISIBLE_DEVICES'] = '0'


#function, it collects knowledge from knowledge.txt
def get_knowledge():
    with open("/Users/kawaii/Desktop/Desktop/faq_bot/faq_bot/process_query/knowledge.txt") as file:
        knowledge = file.read()
    
    file.close()
    return knowledge

#function, checks whether the given query is a general query or goal oriented(GEU related ques)
def check_general_query(query):
    print("Checking General query not built")
    return False

#funtion, which generates general responce 
def gen_general_responce(query):
    return "General query model not made"

#function, which is called to generate GODEL responce
def gen_godel_responce(query, knowledge):
    responce  = get_responce(query, knowledge)
    return responce

#function, which connects front-end with model(only produces one answer)
def get_query(query):
    knowledge = get_knowledge()
    responce = gen_godel_responce(query, knowledge)

    return responce


#funtion, which is called to generate multiple GODEL responces
def gen_godel_more_responce(query, knowledge):
    responce = generate_more_responces(query, knowledge)
    return responce

#function, which connects front-end with model(produces multiple answers)
def get_more_query(query):
    knowledge = get_knowledge()
    responce = gen_godel_more_responce(query, knowledge)

    return responce 

