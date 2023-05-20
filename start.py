import src

RAW_DATA_PATH = "data/raw/GoodReads_100k_books.csv"
CLEANED_DATA_PATH = "data/interim/GoodReads_books_clean.parquet"
TRANSFORMED_DATA_PATH = "data/interim/extended_descriptions.parquet"
TRANSFORMED_MAX_DATA_PATH = "data/interim/extended_max_descriptions.parquet"
VECTORIZED_SHORT_DATA_PATH = "data/processed/short_description_vectorized.parquet"
VECTORIZED_DATA_PATH = "data/processed/description_vectorized.parquet"
VECTORIZED_MAX_DATA_PATH = "data/processed/max_description.parquet"

if __name__ == "__main__":
    src.cleanse_data(  # pylint: disable=no-value-for-parameter
        [RAW_DATA_PATH, CLEANED_DATA_PATH], standalone_mode=False
    )
    # параметры функции помещены в список, это необходимо для адекватной работы click.
    # Однако это вызывает проблемы с pylint,
    # поскольку функции не хватает параметра output_path.
    # Поэтому эта проверка для данной строки кода отключена вручную.
    src.create_extended_df(  # pylint: disable=no-value-for-parameter
        [CLEANED_DATA_PATH, TRANSFORMED_DATA_PATH], standalone_mode=False
    )
    src.vectorize_data(  # pylint: disable=no-value-for-parameter
        [CLEANED_DATA_PATH, VECTORIZED_SHORT_DATA_PATH, "300"], standalone_mode=False
    )
    src.vectorize_data(  # pylint: disable=no-value-for-parameter
        [TRANSFORMED_DATA_PATH, VECTORIZED_DATA_PATH, "300"], standalone_mode=False
    )
    src.vectorize_data(  # pylint: disable=no-value-for-parameter
        [TRANSFORMED_MAX_DATA_PATH, VECTORIZED_MAX_DATA_PATH, "300"],
        standalone_mode=False,
    )
