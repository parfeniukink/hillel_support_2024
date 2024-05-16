from collections.abc import Generator
from pprint import pprint
from types import EllipsisType

nested_structure = {
    "teachers": {
        "john": {
            "age": ...,
            "full_name": ...,
        },
        "marry": {
            "age": ...,
            "address": ...,
        },
    },
    "students": {
        "john": {
            "avg": {
                "math": ...,
                "music": ...,
            },
            "contacts": ...,
        },
    },
}


def extract_nested(
    data: dict, parents: list[str] | None = None, nested: int = 0
) -> Generator[tuple, None, None]:
    if nested > 100:
        raise NotImplementedError

    for key, value in data.items():
        if isinstance(value, EllipsisType):
            if parents:
                yield (*parents, key)
            else:
                yield (key,)
        elif isinstance(value, dict):
            if parents:
                parents.append(key)
                yield tuple(parents)
                yield from extract_nested(data=value, parents=parents)
            else:
                yield (key,)

                # for item in extract_nested(data=value, parents=[key]):
                #     yield item

                yield from extract_nested(data=value, parents=[key])
        else:
            raise NotImplementedError


# results = list(extract_nested(nested_structure))

# pprint(results)

for item in extract_nested(nested_structure):
    print(item)
