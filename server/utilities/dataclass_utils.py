from typing import Any
import dataclasses

# Function to convert a dictionary to dataclasses
def dict_to_dataclass(data: dict, dataclass: Any) -> Any:
    if issubclass(dataclass, type) and issubclass(dataclass, tuple):
        return dataclass(**{k: dict_to_dataclass(v, dataclass.__annotations__.get(k, v)) for k, v in data.items()})
    return data


# Function to convert dataclasses to a dictionary
def dataclass_to_dict(data: Any) -> dict:
    if dataclasses.is_dataclass(data):
        return dataclasses.asdict(data)
    return data