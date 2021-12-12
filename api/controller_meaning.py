import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


def read_request_vectors(path='vec_zapr.txt'):
    with open(path, "r") as f:
        l = []
        for i in range(63):
            l.append([])
            for j in range(768):
                l[-1].append(float(f.readline().strip()))
    return np.array(l)


def read_project_vectors(path='vector_proj_full.txt'):
    with open(path, "r") as f:
        l = []
        for i in range(992):
            l.append([])
            for j in range(768):
                l[-1].append(float(f.readline().strip()))
    return np.array(l)


project_vectors = read_project_vectors()
request_vectors = read_request_vectors()

zapros_df = pd.read_excel('Перечень открытых запросов.xlsx', skiprows=1).iloc[1:, :4]
proj_df = pd.read_excel('Реестр проектов.xlsx', skiprows=1).iloc[3:995]

tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")


def get_index(inp_text, n=5, reverse_check=False):
    token = {'input_ids': [], 'attention_mask': []}
    sentence = inp_text
    # encode each sentence, append to dictionary
    new_token = tokenizer.encode_plus(sentence, max_length=128,
                                      truncation=True, padding='max_length',
                                      return_tensors='pt')
    token['input_ids'].append(new_token['input_ids'][0])
    token['attention_mask'].append(new_token['attention_mask'][0])
    # reformat list of tensors to single tensor
    token['input_ids'] = torch.stack(token['input_ids'])
    token['attention_mask'] = torch.stack(token['attention_mask'])

    output = model(**token)

    embeddings = output.last_hidden_state

    att_mask = token['attention_mask']

    mask = att_mask.unsqueeze(-1).expand(embeddings.size()).float()

    mask_embeddings = embeddings * mask

    summed = torch.sum(mask_embeddings, 1)

    summed_mask = torch.clamp(mask.sum(1), min=1e-9)

    mean_pooled = summed / summed_mask

    mean_pooled = mean_pooled.detach().numpy()
    if reverse_check:
        simularity = cosine_similarity(
            [mean_pooled[0]],
            request_vectors
        )
    else:
        simularity = cosine_similarity(
            [mean_pooled[0]],
            project_vectors
        )

    best_requests = sorted(simularity[0])[-n:][::-1]
    best_index_requests = []
    for i in range(len(best_requests)):
        best_index_requests.append(np.where(simularity == best_requests[i])[1][0])

    return best_index_requests


def get_variants_by_mean(sentence, limit):
    indexes = get_index(sentence, limit)
    return [proj_df.iloc[i ].values for i in indexes]


def get_requests_by_mean(sentence, limit):
    indexes = get_index(sentence, limit, reverse_check=True)
    return [zapros_df.iloc[i].values for i in indexes]
