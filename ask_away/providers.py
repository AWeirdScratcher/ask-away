from typing import Dict, Iterable, List

import g4f

FREE_PROVIDERS = (
    g4f.Provider.DeepAi,
    g4f.Provider.Ails
)

def free_ask(
    messages: List[Dict[str, str]]
) -> Iterable[str]:
    """Use the free provider using gpt4free.

    Some features may be limited.

    Args:
        messages (list of dict of str: str): Messages.
    """
    for chunk in g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=FREE_PROVIDERS[0], # recommended one
        messages=messages,
        stream=True
    ):
        yield chunk

