from typing import Iterator


def split_list_by(string_list: list[str], delimiter: str) -> Iterator[list[str]]:
    chunk: list[str] = list()
    for item in string_list:
        if item == delimiter:
            yield chunk
            chunk = list()
        else:
            chunk.append(item)
    yield chunk
