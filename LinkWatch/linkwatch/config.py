from typing import List

import toml
from pydantic import BaseModel, field_validator


class Site(BaseModel):
    name: str
    url: str

    class Config:
        anystr_strip_whitespace = True

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, value):
        if not value:
            raise ValueError("site name can not be empty")
        return value

    @field_validator("url")
    @classmethod
    def url_has_scheme(cls, value):
        if not value.startswith(("http://", "https://")):
            raise ValueError("url must start with http:// or https://")
        return value


class Settings(BaseModel):
    title: str = "linkwatch"
    output: str = "status.html"
    sites: List[Site] = []

    class Config:
        extra = "forbid"


def load_settings(path="sites.toml"):
    data = toml.load(path)
    return Settings(**data)
