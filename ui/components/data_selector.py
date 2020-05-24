import os
from pathlib import Path, PosixPath
from typing import Tuple, Optional, List, Generator, Any, Union

import streamlit as st
import pandas as pd

DATA_DIR = Path('data')

SUPPORTED_FILE_TYPES = {".csv", ".txt", ".json", ".avro", ".xml"}


def get_available_files(src_dir: Path) -> List[str]:
    """
    Create a full list of all files in given folder and its subfolders
    :param src_dir: folder whose content will be listed
    :return: list of all files in given folder
    """
    fs = [str(Path(dp).relative_to(src_dir)/f) for dp, dn, fn in os.walk(src_dir) for f in fn]
    return fs


def _check_defaults(datasets: List[str], defaults: Union[str, List[str]]) -> List[str]:
    if isinstance(defaults, str):
        defaults = [defaults]  # make sure it's a list
    return [_check_default(datasets, d) for d in defaults]


def _check_default(datasets: List[str], default: str):
    if default not in datasets:
        try:
            def_f = Path(default)
            default = next(ds for ds in datasets if Path(ds) == def_f)
        except StopIteration:
            default = None
    return default


def filter_supported_datasets(datasets: List[str], allowed_exts: Optional[List[str]] = None) -> List[str]:
    if allowed_exts is None:
        allowed_exts = SUPPORTED_FILE_TYPES
    return [ds for ds in datasets if Path(ds).suffix in allowed_exts]


def select_file(src_folder: str, container: Optional = None, defaults: Optional[Union[str, List[str]]] = None) -> List[str]:
    """
    Selection widget for choosing the files to work on.
    :param src_folder: sub-directory within the 'data'-directory from where the files should be used
    :param container: streamlit container in which the component will be placed. Either `st` directly or `st.sidebar`.
                      By default `st` is used.
    :param defaults: Optional preset of files to use as default.
                     Can be either a string for a single file or a list of files.
    :return: tuple with name of selected file and loaded file as pandas dataframe
    """
    if container is None:
        container = st

    container.header("Select source file(s)")

    src_dir = DATA_DIR/src_folder
    available_files = get_available_files(src_dir)

    file_types = list(set([Path(f).suffix for f in available_files]))
    file_types = list(SUPPORTED_FILE_TYPES.intersection(file_types))
    sel_file_types = container.multiselect("File types:", options=file_types, default=file_types)

    datasets = filter_supported_datasets(available_files, sel_file_types)
    defaults = _check_defaults(datasets, defaults)
    defaults = [d for d in defaults if d]  # drop invalid defaults

    selected_files = container.multiselect("Source file: ", options=datasets, default=defaults)

    if len(selected_files) == 0:
        container.error("No valid file selected")
        return []
    else:
        # return [src_dir/f for f in selected_files]
        return selected_files

