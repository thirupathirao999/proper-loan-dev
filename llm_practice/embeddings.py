#from transformers import GPT2tokenizer,GPT2model,GPT2LMHeadmodel
from transformers import GPT2Tokenizer, GPT2Model, GPT2LMHeadModel 
import torch
import os

text="i am thirupathirao from zennial pro"

tokenizer=GPT2Tokenizer.from_pretrained("gpt2")
model=GPT2Model.from_pretrained("gpt2")
head_model=GPT2LMHeadModel.from_pretrained("gpt2")

input_ids=tokenizer.encode(text, return_tensors="pt")

input=torch.tensor(input_ids)
with torch.no_grad():
    embbedings=model(input)
    embedding=embbedings.last_hidden_state
    mean_embbeddingd=embedding.mean(dim=1)

print(mean_embbeddingd)

output_ids=head_model.generate(
    input_ids,
    do_sample=True,
    max_length=100,
    temperature=0.8
)

genareted_text=tokenizer.decode(output_ids[0],skip_special_tokens=True)

print(f"Genreted text: {genareted_text}")


