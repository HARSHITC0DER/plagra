BANNER = """
    ██▓███   ██▓    ▄▄▄        ▄████  ██▀███   ▄▄▄         
   ▓██░  ██▒▓██▒   ▒████▄     ██▒ ▀█▒▓██ ▒ ██▒▒████▄       
   ▓██░ ██▓▒▒██░   ▒██  ▀█▄  ▒██░▄▄▄░▓██ ░▄█ ▒▒██  ▀█▄     
   ▒██▄█▓▒ ▒▒██░   ░██▄▄▄▄██ ░▓█  ██▓▒██▀▀█▄  ░██▄▄▄▄██    
   ▒██▒ ░  ░░██████▒▓█   ▓██▒░▒▓███▀▒░██▓ ▒██▒ ▓█   ▓██▒   
   ▒▓▒░ ░  ░░ ▒░▓  ░▒▒   ▓▒█░ ░▒   ▒ ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░   
   ░▒ ░     ░ ░ ▒  ░ ▒   ▒▒ ░  ░   ░   ░▒ ░ ▒░  ▒   ▒▒ ░   
   ░░         ░ ░    ░   ▒   ░ ░   ░   ░░   ░   ░   ▒      
                ░  ░     ░  ░      ░    ░           ░  ░   
"""

print(BANNER)


import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def get_response(input_text, num_return_sequences, num_beams):
    batch = tokenizer([input_text], truncation=True, padding='max_length', max_length=60, return_tensors="pt").to(torch_device)
    translated = model.generate(**batch, max_length=60, num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
    return tgt_text

num_beams = 10
num_return_sequences = 1

# Input from the user
user_input = input("Enter a paragraph of text: ")

# Split the input paragraph into a list of sentences
from sentence_splitter import SentenceSplitter

splitter = SentenceSplitter(language='en')
sentence_list = splitter.split(text=user_input)

# Paraphrase each sentence in the list
paraphrases = []
for sentence in sentence_list:
    paraphrase = get_response(sentence, num_return_sequences, num_beams)
    paraphrases.append(paraphrase[0])

# Combine the paraphrased sentences into a paragraph
paraphrase_paragraph = ' '.join(paraphrases)

# Split the paraphrased paragraph into individual sentences
import re

sentence_pattern = r'(?<=[.!?]) +'
paraphrased_sentences = re.split(sentence_pattern, paraphrase_paragraph)

# Print the combined paragraph and the separated sentences
print("\nCombined Paragraph:")
print(paraphrase_paragraph)

print("\nSeparated Sentences:")
for idx, sentence in enumerate(paraphrased_sentences):
    print(f"Sentence {idx + 1}: {sentence}")

# Comparison of the original (user_input) and the paraphrased version (paraphrase_paragraph variable)
print("\nOriginal:")
print(user_input)

print("\nParaphrased:")
print(paraphrase_paragraph)
