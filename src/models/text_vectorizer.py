import click

import numpy as np
import pandas as pd

import torch
import transformers  # type: ignore
from transformers import BertTokenizer, BertModel

TOKENIZER = BertTokenizer.from_pretrained("bert-base-uncased")
MODEL = BertModel.from_pretrained(
    "bert-base-uncased",
    output_hidden_states=True,  # Whether the model returns all hidden-states.
)
device = "cuda:0" if torch.cuda.is_available() else "cpu"


def text_to_vec(
    text: str,
    tokenizer: transformers.models.bert.tokenization_bert.BertTokenizer = TOKENIZER,
    model: transformers.models.bert.modeling_bert.BertModel = MODEL,
    device: str = device,
) -> np.ndarray:
    """
    Vectorizes text using BERT-model.
    :text: str to vetorize
    :tokenizer:
    :model: vectorizing NLP-model
    :return: np.array representing vectorized text
    """
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt")["input_ids"]
        if inputs.shape[-1] > 512:
            inputs = torch.cat((inputs[0, :129], inputs[0, -383:]))
            inputs = inputs.reshape(1, -1)
        inputs = inputs.to(device)
        model = model.to(device)
        outputs = model(inputs)
    hidden_states = outputs[2]
    token_vecs = hidden_states[-2][0]
    sentence_embedding = torch.mean(token_vecs, dim=0).numpy()
    return sentence_embedding


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.argument(
    "batch_size",
    type=click.INT,
)
def vectorize_data(input_path: str, output_path: str, batch_size: int):
    df_to_vectorize = pd.read_parquet(input_path, columns=["desc"])
    try:
        batch_start = pd.read_parquet(output_path).index[-1]
        assert isinstance(batch_start, np.int64)
        batch_start = int(batch_start)
        batch_start += 1
    except FileNotFoundError:
        batch_start = 0
    while batch_start <= df_to_vectorize.shape[0]:
        batch_end = batch_start + batch_size - 1
        print(
            f"Vectorizing descriptions from id = {batch_start} to id = {batch_end} ... ",
            end="",
        )
        vectorized_series = (
            df_to_vectorize["desc"]
            .loc[batch_start:batch_end]
            .apply(text_to_vec)  # type: ignore
        )
        print("DONE!")
        batch_start += batch_size
        vectorized_dataframe = pd.DataFrame(
            index=vectorized_series.index,
            columns=[str(_) for _ in range(len(vectorized_series.iloc[0]))],
            data=np.stack(vectorized_series.to_numpy()),  # type: ignore
        )
        print(f"Saving results to {output_path} ... ", end="")
        try:
            vectorized_dataframe.to_parquet(
                output_path, engine="fastparquet", append=True, index=True
            )
        except FileNotFoundError:
            vectorized_dataframe.to_parquet(
                output_path, engine="fastparquet", index=True
            )
        print("DONE!")


if __name__ == "__main__":
    vectorize_data()  # pylint: disable=no-value-for-parameter
