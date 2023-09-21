"""Package-wide helping functions for setup."""
import importlib
import os
import shutil
import sys
from typing import IO, Optional, Union
from types import ModuleType
from pathlib import Path


def str2bool(value: str) -> bool:
    """Convert a string to its boolean representation.

    False valid values: 'false', 'f', '0', 'no', and 'n'.
    True valid values: 'true', 't', '1', 'yes', and 'y'.

    Args:
        value (str): String representing a boolean value.

    Raises:
        ValueError: Failed to parse value.

    Returns:
        bool: Boolean representation of the value.
    """
    value = value.lower()

    if value not in {"false", "f", "0", "no", "n", "true", "t", "1", "yes", "y"}:
        raise ValueError(f"{value} is not a valid boolean value")

    if isinstance(value, bool):
        out = value
    if value in {"false", "f", "0", "no", "n"}:
        out = False
    elif value in {"true", "t", "1", "yes", "y"}:
        out = True

    return out


def clearAllDirs(files_path):
    os.chdir(str(files_path / 'box_scores'))
    teams = import_module(get_config_path()).teams
    # teams=['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU',
    # 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL',
    # 'PHI', 'PHO', 'POR', 'SAC' , 'SAS', 'TOR', 'UTA', 'WAS']

    for team in teams:
        shutil.rmtree('%s' %team)
        shutil.rmtree('defense/%s' %team)
        shutil.rmtree('offense/%s' %team)
        os.mkdir('%s' %team)
        os.mkdir('defense/%s' %team)
        os.mkdir('offense/%s' %team)


def get_config_path() -> os.PathLike:
    """Read environment variables to determine configuration file location.

    Returns:
        PathLike: Configuration file location.
    """
    PROJECT_DIR: Optional[Union[str, Path]] = os.environ.get("PROJECT_DIR")
    if PROJECT_DIR is None:
        PROJECT_DIR = Path.cwd()
    else:
        PROJECT_DIR = Path(PROJECT_DIR)

    DEFAULT_CONFIG_PATH = PROJECT_DIR / "config" / "default.py"

    return os.environ.get("BOOST_GM_CONFIG", DEFAULT_CONFIG_PATH)


def import_module(module_path: str) -> ModuleType:
    """(Re)Import a Python module, as for a config file."""
    try:
        return importlib.reload(sys.modules[module_path.stem])
    except KeyError:
        pass

    assert module_path.exists(), f"File {module_path} does not exist."
    if module_path.parent not in sys.path:
        sys.path.append(str(module_path.parent.resolve()))
    return importlib.import_module(module_path.stem)


def requirements(in_file: IO) -> list:
    """Parse pip-formatted requirements file."""
    with open(in_file) as f:
        packages = f.read().splitlines()
    result = []
    for pkg in packages:
        if pkg.strip().startswith("#") or not pkg.strip():
            continue
        result.append(pkg)
    return result