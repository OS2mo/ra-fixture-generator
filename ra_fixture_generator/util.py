#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import asyncio
import hashlib
import json
import sys
from functools import lru_cache
from functools import wraps
from typing import Awaitable
from typing import Callable
from typing import TypeVar
from uuid import UUID

import click
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic.tools import parse_obj_as


def load_file_as(model: BaseModel, json_file) -> BaseModel:
    json_data = json.load(json_file)
    return model.parse_obj(json_data)


def validate_url(ctx: click.Context, param: str, value: str) -> AnyHttpUrl:
    try:
        return parse_obj_as(AnyHttpUrl, value)
    except ValidationError as e:
        raise click.BadParameter(e)


def takes_json_file(function):
    function = click.option(
        "--json-file",
        help="JSON file of models to parse",
        type=click.File("r"),
        default=sys.stdin,
    )(function)
    return function


def model_validate_helper(model: BaseModel, json_file) -> BaseModel:
    try:
        return load_file_as(model, json_file)
    except json.decoder.JSONDecodeError:
        raise click.ClickException("Unable to parse input file as JSON")
    except ValidationError as e:
        raise click.ClickException(e)


@lru_cache(maxsize=None)
def generate_uuid(seed: str) -> UUID:
    """
    Generate an UUID based on a seed in a deterministic way
    This allows us generate the same uuid for objects across different imports,
    without having to maintain a separate list of UUIDs, or fetch the relevant uuids
    from MO
    """
    m = hashlib.md5()
    m.update(seed.encode("utf-8"))
    return UUID(m.hexdigest())


CallableReturnType = TypeVar("CallableReturnType")


def async_to_sync(
    func: Callable[..., Awaitable[CallableReturnType]]
) -> Callable[..., CallableReturnType]:
    """Decorator to run an async function to completion.

    Example:

        @async_to_sync
        async def sleepy(seconds):
            await asyncio.sleep(seconds)
            return seconds

        print(sleepy(5))  # --> 5

    Args:
        func (async function): The asynchronous function to wrap.

    Returns:
        :obj:`sync function`: The synchronous function wrapping the async one.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> CallableReturnType:
        return asyncio.run(func(*args, **kwargs))

    return wrapper
