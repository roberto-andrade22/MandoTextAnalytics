def download_model(MODEL = 't5-base'):

    from transformers import T5Tokenizer, T5ForConditionalGeneration
    import os

    tokenizer = T5Tokenizer.from_pretrained(MODEL)

    model = T5ForConditionalGeneration.from_pretrained(MODEL)

    save_path = MODEL + '_model_pytorch'
    
    try:
        os.makedirs(save_path)

    except FileExistsError:
        pass

    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)

if __name__ == '__main__':
    download_model()
