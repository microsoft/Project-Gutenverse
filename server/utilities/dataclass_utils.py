# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Any
import dataclasses
import hashlib
import uuid

def story_title_to_hash(input)-> str: 
    sha256 = hashlib.sha256()
    sha256.update(input.encode())
    # Get the first 16 bytes of the SHA256 hash
    hash_bytes = sha256.digest()[:16]
    # Create a UUID from the hash
    return str(uuid.UUID(bytes=hash_bytes))

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