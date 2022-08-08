import difflib as dif
from time import time
import logging
from pathlib import Path

import pandas as pd

from service import config

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
weights_dir = app_config.path.utility_dir

word_depth = 6
row_counter = 0
col_counter = 0
grade = 100
level = 1


def make_short(name, **kwargs):
    depth = kwargs['depth']
    name_list = name.split()
    if len(name_list) > depth:
        name_list = name_list[:depth]
    return ' '.join(name_list)


def make_pattern(frame: pd.DataFrame, word_count: int) -> pd.DataFrame:
    """Функция создает пустую матрицу размерностью кол-во наименгований * кол-во наименеований."""
    return pd.DataFrame(index=range(word_count), columns=range(word_count))


def compare_names_col(col_word, col_num, **kwargs):
    """Функция перебора колонок фрейма и сравнения пар наименований по осям x*y."""
    global row_counter, level  # noqa: WPS420 need for compare_base function work
    row_counter = kwargs['counter']  # noqa: WPS442 use only for compare_base function work
    words_in_row: pd.DataFrame = kwargs['row_frame']
    row_word = words_in_row.iloc[row_counter, col_num]
    weight = dif.SequenceMatcher(None, col_word, row_word).ratio()

    if level == col_num // grade:
        level += 1
        logger.debug('{0}, {1}, {2}'.format(col_num, level, col_num // grade))

    row_counter += 1
    return weight


def compare_names_row(col_frame: pd.DataFrame, **kwargs):
    """Функция перебора строк и колонок фрейма."""
    row_frame: pd.DataFrame = kwargs['row_frame']
    return col_frame.apply(
        compare_names_col, args=(col_frame.name,), counter=0, row_frame=row_frame
    )


def count_weights(frame: pd.DataFrame, asset_name: str) -> pd.DataFrame:
    word_count = frame.shape[0]
    pattern = make_pattern(frame, word_count)

    words_in_row = pattern.copy()
    words_in_col = pattern.copy()

    frame['short'] = frame[asset_name].apply(make_short, depth=word_depth)
    words_in_row.iloc[:word_count] = frame['short']  # noqa: WPS362 pandas style
    words_in_col = words_in_row.T

    return words_in_col.apply(compare_names_row, row_frame=words_in_row)


def create_csv(weights: pd.DataFrame, precision: float, excel_file: Path, ind: str) -> None:
    excel_weights = weights_dir / f'weight_{excel_file.stem}.csv'
    weights.astype('float')
    weights[weights[:] > precision].to_csv(excel_weights, sep=';', index_label=ind)  # noqa: WPS221


def create_weights(excel_file: Path, precision: float, ind: str, asset_name: str) -> bool:
    """Базовая функция для подсчета весов совпадения пар наименоваий.

    Аргументы:
        excel_file: Path - объект Path соссылкой на excel файл ведомость Основных средств
        precision: float - точность совпадения от 0 до 1
        ind: str - наименования колонки индекса
        asset_name: str - наименование колонки содержащей наименования Основных средств

    Return:
        bool - возвращает True если подсчитаны веса совпадений и сохранен файл с их значениями
    """
    start = time()
    frame = pd.read_excel(excel_file, index_col='№ п/п', sheet_name='TDSheet')
    weights = count_weights(frame, asset_name)
    frame_time = time() - start

    global row_counter, level  # noqa: WPS420 need for compare_base function work
    row_counter, level = 0, 0  # noqa: WPS442 use only for compare_base function work

    create_csv(weights, precision, excel_file, ind)
    excel_time = time() - start

    logger.debug(f'frame time - {frame_time};\nexcel time - {excel_time}')
    return True
