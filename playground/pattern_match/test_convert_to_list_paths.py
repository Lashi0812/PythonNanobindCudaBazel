import pathlib

def convert_to_list_paths(
    paths: pathlib.Path | str | list[str],
) -> list[pathlib.Path] | None:
    match paths:
        case str():
            return [pathlib.Path(paths)]
        case pathlib.Path():
            return [paths]
        case list() as list_str if all(isinstance(a, str) for a in list_str):
            return list(map(pathlib.Path, list_str))
        case _:
            return None

convert_to_list_paths(pathlib.Path("a"))
convert_to_list_paths("a")
convert_to_list_paths(list("hello"))
list_path:list[pathlib.Path] = list(map(lambda x :pathlib.Path(x),list("hello")))
# convert_to_list_paths(list_path)
