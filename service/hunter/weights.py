import difflib as dif
from time import time
import logging
from pathlib import Path

import pandas as pd

from service import config

logger = logging.getLogger(__name__)

app_config = config.load_from_env()
weights_dir = app_config.path.weights_dir

word_depth = 6
precision = 0.5
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
    return pd.DataFrame(index=range(word_count), columns=range(word_count))


def compare_base(col_word, col_num, **kwargs):
    global row_counter, level  # noqa: WPS420 need for compare_base function work
    row_counter = kwargs['counter']  # noqa: WPS442 use only for compare_base function work
    words_in_row: pd.DataFrame = kwargs['row_frame']
    row_word = words_in_row.iloc[row_counter, col_num]
    weight = dif.SequenceMatcher(None, col_word, row_word).ratio()
    #logger.debug(col_num)

    if level == col_num // grade:
        level += 1
        logger.debug(f'{col_num}, {level}, {col_num // grade}')

    row_counter += 1
    return weight


def compare_ind(col_frame: pd.DataFrame, **kwargs):
    row_frame: pd.DataFrame = kwargs['row_frame']
    return col_frame.apply(compare_base, args=(col_frame.name,), counter=0, row_frame=row_frame)


def create_weights(
    excel_file: Path,
    asset_name: str = 'основное средство',
    ind: str = 'ind',
) -> bool:
    start = time()
    excel_weights = weights_dir / excel_file.name
    frame = pd.read_excel(excel_file, index_col=ind)
    frame['short'] = frame[asset_name].apply(make_short, depth=word_depth)
    word_count = len(frame)
    pattern = make_pattern(frame, word_count)

    words_in_row = pattern.copy()
    words_in_col = pattern.copy()

    words_in_row.iloc[:word_count] = frame['short']  # noqa: WPS362 pandas style
    words_in_col = words_in_row.T
    weights: pd.DataFrame = words_in_col.apply(compare_ind, row_frame=words_in_row)
    frame_time = time() - start
    global row_counter, level
    row_counter, level = 0, 0
    weights.astype('float')
    weights[weights[:] > precision].to_excel(excel_weights)
    excel_time = time() - start
    logger.debug(f'frame time - {frame_time};/nexcel time - {excel_time}')
    return True
