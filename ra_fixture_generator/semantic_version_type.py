#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import re
from functools import lru_cache

from pydantic import BaseModel

# Regex from https://semver.org/
_semver_regex = (
    # Version part
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    # Prerelease part
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    # Build metadata
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)


@lru_cache
def get_regex():
    return re.compile(_semver_regex)


class SemanticVersion(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=_semver_regex,
            examples=["0.1.0", "1.0.0-alpha", "1.0.0-alpha+001"],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")
        m = get_regex().fullmatch(v)
        if not m:
            raise ValueError("invalid semver format")
        return cls(v)

    def __repr__(self):
        return f"SemanticVersion({super().__repr__()})"


class SemanticVersionModel(BaseModel):
    __root__: SemanticVersion
