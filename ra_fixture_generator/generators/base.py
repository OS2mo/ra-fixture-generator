# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from ra_utils.generate_uuid import uuid_generator


class BaseGenerator:
    def __init__(self, seed: str = None) -> None:
        if seed is None:
            seed = self.__class__.__name__

        self.seed = seed
        self.generate_uuid = uuid_generator(seed)

    def generate(self, *args, **kwargs):
        pass
