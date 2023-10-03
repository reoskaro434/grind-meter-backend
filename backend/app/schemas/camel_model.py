from pydantic import BaseModel


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


# camel snake case conversion
class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
