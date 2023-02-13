import torch
import numpy as np
import dotmap


from transformers import (
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

# function, which is used to connect GPU
def set_seed(args):
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if args.n_gpu > 0:
        torch.cuda.manual_seed_all(args.seed)

model = None
tokenizer = None
args = dotmap.DotMap()
args.model_name_or_path = '/Users/kawaii/Desktop/Desktop/faq_bot/faq_bot/GODEL-Large'
args.prompt = ''
args.padding_text = ''
args.length = 128
args.num_samples = 1
args.temperature = 1
args.num_beams = 5
args.repetition_penalty = 1
args.top_k = 0
args.top_p = 0.5
args.no_cuda = False
args.seed = 2022
args.stop_token = '<|endoftext|>'
args.n_gpu = 0 # changed from 1 to 0
args.device = 'cpu'

#mps_device = torch.device("mps")
#coda is not compatible with M1 GPU (MPS)

set_seed(args)

#function, which activate model and tokenizer 
def main():
    global model, tokenizer, args
    global model_more 

    config = AutoConfig.from_pretrained(args.model_name_or_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        args.model_name_or_path,
        from_tf=bool(".ckpt" in args.model_name_or_path),
        config=config,
    )

    model_more = AutoModelForSeq2SeqLM.from_pretrained(
        args.model_name_or_path,
        from_tf=bool(".ckpt" in args.model_name_or_path),
        config=config,
    )

    model = model.to(args.device)
    model_more = model_more.to(args.device)

    # model = model.to(mps_device)
    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, use_fast=not args.use_slow_tokenizer)

# function, which generates only one responce 
def generate(context, knowledge):
    global model, args, tokenizer

    input_ids = tokenizer(context + ' <|knowledge|> ' + knowledge + ' =>', return_tensors="pt").input_ids.to(args.device)
    gen_kwargs = {
        # 'num_beams': args.num_beams,
        'max_length': args.length,
        'min_length': 32,
        'top_k': 10,
        'no_repeat_ngram_size': 4

    }

    output_sequences = model.generate(input_ids, **gen_kwargs)
    output_sequences = tokenizer.batch_decode(output_sequences, skip_special_tokens=True) # skip_special_tokens = True

    return output_sequences



# function to generate more responces 
def generate_more(context, knowledge):
    global model_more, args, tokenizer

    input_ids = tokenizer(context + ' <|knowledge|> ' + knowledge + ' =>', return_tensors="pt").input_ids.to(args.device)
    gen_kwargs = {
        'num_beams': args.num_beams,
        'max_length': args.length,
        'min_length': 32,
        'top_k': 10,
        'no_repeat_ngram_size': 4

    }

    output_sequences = model_more.generate(input_ids, **gen_kwargs)
    output_sequences = tokenizer.batch_decode(output_sequences, skip_special_tokens=True) # skip_special_tokens = True

    return output_sequences

# function, which is called to generate more responces 
def generate_more_responces(query, knowledge):
    main()
    output = generate_more(query, knowledge)
    return output

# function, which is called to generate only one responce
def get_responce(query, knowledge):
    main()
    output = generate(query, knowledge)
    return output



