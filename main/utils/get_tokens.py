import tiktoken

def num_tokens_from_string(string: str) -> int:

    """Returns the number of tokens in a text string."""

    if isinstance(string, str):
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        num_tokens = len(encoding.encode(string))
        return num_tokens
    else: raise TypeError("expected string")
