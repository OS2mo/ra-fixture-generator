# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from ra_utils.generate_uuid import uuid_generator


class BaseGenerator:
    def __init__(self) -> None:
        self.generate_uuid = uuid_generator(base=self.__class__.__name__)

    def generate(self, *args, **kwargs):
        pass
