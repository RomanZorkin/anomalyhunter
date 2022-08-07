import difflib as dif
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


def make_short(name, **kwargs):
    depth = kwargs['depth']
    name_list = name.split()
    if len(name_list) > depth:
        name_list = name_list[:depth]
    return ' '.join(name_list)


def make_pattern(frame: pd.DataFrame, word_count: int) -> pd.DataFrame:
    return pd.DataFrame(index=range(word_count), columns=range(word_count))


def compare_base(col_word, col_num, **kwargs):
    global row_counter
    row_counter = kwargs['counter']
    words_in_row: pd.DataFrame = kwargs['row_frame']
    row_word = words_in_row.iloc[row_counter, col_num]
    t = dif.SequenceMatcher(None, col_word, row_word).ratio()
    row_counter += 1
    return t


def compare_ind(col_frame: pd.DataFrame, **kwargs):
    row_frame: pd.DataFrame = kwargs['row_frame']
    return col_frame.apply(compare_base, args=(col_frame.name,), counter=0, row_frame=row_frame)


def create_weights(
    excel_file: Path,
    asset_name: str = 'основное средство',
    ind: str = 'ind',
) -> bool:
    excel_weights = weights_dir / excel_file.name
    frame = pd.read_excel(excel_file, index_col=ind)
    frame['short'] = frame[asset_name].apply(make_short, depth=word_depth)
    word_count = len(frame)
    pattern = make_pattern(frame, word_count)

    words_in_row = pattern.copy()
    words_in_col = pattern.copy()

    words_in_row.iloc[:word_count] = frame['short']
    words_in_col = words_in_row.T
    weights: pd.DataFrame = words_in_col.apply(compare_ind, row_frame=words_in_row)
    weights.astype('float')
    weights[weights[:] > precision].to_excel(excel_weights)

    return True
