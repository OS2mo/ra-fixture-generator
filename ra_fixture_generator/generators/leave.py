# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from typing import Optional
from uuid import UUID

from ramodels.mo._shared import EngagementRef
from ramodels.mo._shared import LeaveType
from ramodels.mo.details import Engagement
from ramodels.mo.details import Leave

from .base import BaseGenerator


class LeaveGenerator(BaseGenerator):
    def __init__(self, leave_types: dict[str, UUID]) -> None:
        super().__init__()
        self.leave_type_uuids = list(leave_types.values())

    def generate(self, engagement_layers: list[list[Engagement]]) -> list[list[Leave]]:
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
