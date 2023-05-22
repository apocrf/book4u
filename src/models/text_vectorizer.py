import click

import numpy as np
import pandas as pd

import torch
import transformers  # type: ignore
from transformers import BertTokenizer, BertModel
import yaml  # type: ignore


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
    :param text: str to vectorize
    :param tokenizer: text tokenizer
    :param model: model to vectorize text
    :param device: device to transfer model to
    :return: np.ndarray representing vectorized text
    """
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors="pt", verbose=False)["input_ids"]
        if inputs.shape[-1] > 512:
            inputs = torch.cat((inputs[0, :129], inputs[0, -383:]))
            inputs = inputs.reshape(1, -1)
        inputs = inputs.to(device)
        model = model.to(device)
        outputs = model(inputs)
    hidden_states = outputs[2]
    token_vecs = hidden_states[-2][0]
    sentence_embedding = torch.mean(token_vecs, dim=0).numpy()
    if device != "cpu":
        torch.cuda.empty_cache()
    return sentence_embedding


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.argument("params_path", type=click.Path(exists=True))
def vectorize_data(input_path: str, output_path: str, params_path: str):
    """
    Create and save pd.Dataframe containing vectorized book descriptions
    in .parquet format. Transformation to vectors realized by batches.
    :param input_path: Path to read interim .parquet from
    :param output_path: Path to save vectorized data in .parquet
    :param batch_size: size of the batch
    """
    print(f"Device: {device}")
    with open(params_path, "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)
    batch_size: int = params["vectorize"]["batch_size"]
    df_to_vectorize = pd.read_parquet(input_path, columns=["desc"])
    try:
        batch_start: int = pd.read_parquet(output_path).index[-1]
        assert isinstance(batch_start, np.int64)
        batch_start += 1
    except FileNotFoundError:
        batch_start = 0
    while batch_start <= df_to_vectorize.shape[0]:  # type: ignore
        batch_end: int = batch_start + batch_size - 1
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
