import src

RAW_DATA_PATH = "data/raw/GoodReads_100k_books.csv"
CLEANED_DATA_PATH = "data/interim/GoodReads_books_clean.csv"

if __name__ == "__main__":
    src.cleanse_data(  # pylint: disable=no-value-for-parameter
        [RAW_DATA_PATH, CLEANED_DATA_PATH]
    )
    # параметры функции помещены в список, это необходимо для адекватной работы click.
    # Однако это вызывает проблемы с pylint,
    # поскольку функции не хватает параметра output_path.
    # Поэтому эта проверка для данной строки кода отлючена вручную.
