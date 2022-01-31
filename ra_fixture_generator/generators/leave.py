# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from collections.abc import Iterator
from typing import Optional
from uuid import UUID

import more_itertools
from ramodels.mo._shared import EngagementRef
from ramodels.mo._shared import LeaveType
from ramodels.mo.details import Engagement
from ramodels.mo.details import Leave

from .base import BaseGenerator
from ..util import thawed


class LeaveGenerator(BaseGenerator):
    def __init__(self, leave_types: dict[str, UUID]) -> None:
        super().__init__()
        self.leave_type_uuids = list(leave_types.values())

    def generate(self, engagement_layers: list[list[Engagement]]) -> list[list[Leave]]:
        print("Generating leaves")

        def construct_leave(engagement: Engagement) -> Optional[Leave]:
            if random.random() > 0.4:
                return None
            return Leave(
                leave_type=LeaveType(uuid=random.choice(self.leave_type_uuids)),
                person=engagement.person,
                engagement=EngagementRef(uuid=engagement.uuid),
                validity=self.random_validity(engagement.validity),
            )

        return [
            list(filter(None, map(construct_leave, layer)))
            for layer in engagement_layers
        ]

    def generate_modifications(
        self, leave_layers: list[list[Leave]], engagement_layers: list[list[Engagement]]
    ) -> list[Leave]:
        engagement_validities = {
            e.uuid: e.validity for e in more_itertools.flatten(engagement_layers)
        }

        def construct_modification(leave: Leave) -> Iterator[Leave]:
            while random.random() < 0.1:
                with thawed(leave.copy()) as copy:
                    copy.leave_type = LeaveType(
                        uuid=random.choice(self.leave_type_uuids)
                    )
                    copy.validity = self.random_validity(
                        engagement_validities[copy.engagement.uuid]
                    )
                yield copy

        return list(
            more_itertools.flatten(
                map(construct_modification, more_itertools.flatten(leave_layers))
            )
        )
