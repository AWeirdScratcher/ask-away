import os
from typing import Dict, List

import appdirs

app_name = "ask-away-python"
app_author = "awdev"

data_dir = appdirs.user_data_dir(app_name, app_author)
proj_dir = os.path.join(data_dir, "projects")

os.makedirs(proj_dir, exist_ok=True)

class AppFile:
    """Represents an extension of appdirs, named AppFile.

    Acts as a context manager, and creates app files (user data).

    Args:
        fn (str): The filename.
        mode (str): The open mode.
        *args, **kwargs (Any): Args and keyword-only args.

    Attributes:
        fp (str): File path.
        mode (str): The open mode.
        args, kwargs (Any): Args and keyword-only args.
    """
    fp: str
    mode: str
    args: tuple
    kwargs: dict

    def __init__(
        self, 
        fn: str, 
        mode: str,
        *args,
        **kwargs
    ):
        self.fp = os.path.join(data_dir, fn)
        self.mode = mode
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        return open(self.fp, self.mode)

    def __exit__(self, *args):
        pass

class AppProject:
    """Represents a project.
    
    Args:
        name (str): The project name.
    """
    p: str

    def __init__(
        self, 
        name: str
    ):
        self.p = os.path.join(
            proj_dir, 
            name
        )

    def create(self) -> None:
        os.makedirs(self.p, exist_ok=True)

    def tree(self) -> Dict[str, str]:
        """Returns the project file tree.

        Returns:
            dict of str: str
        """
        tr = {}

        for f in os.listdir(self.p):
            with open(
                os.path.join(self.p, f),
                "r",
                encoding="utf-8"
            ) as f:
                tr[f] = f.read()

        return tr

def projects() -> List[str]:
    """Returns all existing projects."""
    return os.listdir(proj_dir)
