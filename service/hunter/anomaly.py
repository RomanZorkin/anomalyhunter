import logging
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.io.excel import ExcelWriter

from service import config

logger = logging.getLogger(__name__)

dirs = config.load_from_env().path

upload_dir, export_dir, utility_dir = dirs.upload_dir, dirs.export_dir, dirs.utility_dir


def control_frame(
    upload_file: Path, upload_frame: pd.DataFrame, compare_col: str, ind: str,
) -> tuple[pd.DataFrame, int]:
    """Создание фрейма характеристики сравнения кол-во наименований * кол-во наименоаний."""

    okof_file = utility_dir / f'compare_{upload_file.stem}.csv'

    word_count = upload_frame.shape[0]

    okof = pd.DataFrame(columns=range(word_count), index=range(word_count))
    okof.iloc[:word_count] = upload_frame[compare_col]
    okof.to_csv(okof_file, sep=';', index_label=ind)
    control = pd.read_csv(okof_file, sep=';', index_col=ind)
    return control, word_count


def unit_rows(clean_index: pd.DataFrame) -> pd.DataFrame:
    levels = clean_index.index
    for num, level in enumerate(levels):
        for sublevel in levels[num:]:
            if level == sublevel:
                continue
            logger.debug(f'Compare level = {level} & sublevel = {sublevel}')
            diff_idx = clean_index.loc[level].dropna().isin(clean_index.loc[sublevel].dropna())
            if diff_idx.any():
                logger.debug(f'row {level} == row {sublevel}')
                tmp_df = pd.DataFrame([clean_index.loc[sublevel], clean_index.loc[level]]).T
                tmp_df['nan'] = np.nan
                tmp_df = tmp_df.fillna(method='ffill', axis=1).T
                clean_index.loc[sublevel] = tmp_df.loc['nan']
                clean_index.drop([level], inplace=True)
                logger.debug('drop')
                break
            else:
                logger.debug(f'row {level} != row {sublevel}')
    return clean_index


def get_dubl(filename: str, precision: float, word_count: int, ind: str) -> pd.DataFrame:
    weights_file = utility_dir / f'weight_{filename}.csv'
    dubl = utility_dir / f'dubl_{filename}.csv'

    weights = pd.read_csv(weights_file, sep=';', index_col=ind)
    # заполняем nan там где не удовлетворяет требованиям точности
    index_df = pd.DataFrame(np.where(weights > precision, weights.columns, np.nan))
    # удаляем дубликаты
    index_df.drop_duplicates(keep='first', inplace=True)
    # Исключаем все неповторяющиея названия
    index_df['nan'] = index_df.isnull().sum(axis=1)

    clean_index = index_df.loc[index_df['nan'] < (word_count - 1)]
    clean_index.pop('nan')

    clean_frame = unit_rows(clean_index)
    clean_frame.to_csv(dubl, sep=';', index_label=ind)
    clean_frame = pd.read_csv(dubl, sep=';', index_col=ind)

    # Создается маска значений весов отличных от nan
    mask = weights.notnull()
    return mask, clean_frame


def find_dif(control: pd.DataFrame, control_mask: pd.DataFrame, word_count: int) -> pd.DataFrame:
    dubl = []
    for i in range(word_count):
        logger.debug(set(control_mask.loc[i].dropna().to_list()))
        if len(set(control_mask.loc[i].dropna().to_list())) == 1:
            dubl.append(i)
    return control.query(f"index not in {dubl}")


def create_export(filename: str, mistake: list[int], clean_frame: pd.DataFrame, upload_frame: pd.DataFrame):
    export_file = export_dir / f'anomaly_{filename}.xlsx'

    mistake_arr = np.array(mistake)
    mur = pd.DataFrame()
    
    with ExcelWriter(export_file, mode='w') as writer:
        mur.to_excel(writer, sheet_name='лист')

    logger.debug(mistake_arr)
    for num, name_ind in enumerate(mistake_arr):
        #logger.debug(name_ind)
        #logger.debug(clean_frame)
        answer = clean_frame.loc[[name_ind]].T.dropna().iloc[:, 0].to_list()
        #logger.debug(answer)
        #logger.debug(upload_frame)
        mur = upload_frame.loc[answer]

        with ExcelWriter(export_file, mode='a') as writer:
            mur.to_excel(writer, sheet_name=f'лист {num}')


def get_anomaly(
    filename: str, suffix: str, sheet: str, compare_col: str, precision: float, ind: str,
) -> bool:
    upload_file = upload_dir / f'{filename}{suffix}'

    xl = pd.ExcelFile(upload_file)
    upload_frame = xl.parse(sheet)

    control, word_count = control_frame(upload_file, upload_frame, compare_col, ind)
    mask, clean_frame = get_dubl(filename, precision, word_count, ind)
    control_mask = control[mask]
    dif_compare = find_dif(control, control_mask, word_count)

    mistake = list(set(list(clean_frame.index)) & set(list(dif_compare.index)))
    mistake.sort()

    create_export(filename, mistake, clean_frame, upload_frame)
    return True
