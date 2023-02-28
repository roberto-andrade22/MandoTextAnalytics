def load_model(MODEL = 't5-base'):
    from transformers import T5Tokenizer, T5ForConditionalGeneration
    import numpy as np
    import os
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = '5120'
    import torch

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    save_path = MODEL + '_model_pytorch'

    tokenizer = T5Tokenizer.from_pretrained(save_path)

    model = T5ForConditionalGeneration.from_pretrained(save_path).to(device)

    return(model, tokenizer)

import torch
import torch.nn
import gc

fine_tuned = 'Alred/t5-base-finetuned-summarization-cnn-ver2'

model, tokenizer = load_model()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def make_episode_summary(episode_plot, model = model, tokenizer = tokenizer, device = device):
    chunk_size = 512
    chunks = [episode_plot[i:i+chunk_size] for i in range(0, len(episode_plot), chunk_size)]
    summaries = []
  
    for chunk in chunks:
        input_ids = tokenizer.encode(chunk, return_tensors="pt").to(device)
        summary_ids = model.generate(input_ids, 
                                    min_length=20, 
                                    max_length= 58, 
                                    length_penalty= 1.0, 
                                    num_beams=3,
                                    early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    summary = ' '.join(summaries)
    torch.cuda.empty_cache()
    gc.collect()
    return(summary)
