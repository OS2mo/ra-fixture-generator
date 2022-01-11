# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from uuid import UUID

from ramodels.mo import Validity
from ramodels.mo._shared import EngagementRef
from ramodels.mo._shared import LeaveType
from ramodels.mo.details import Engagement
from ramodels.mo.details import Leave

from .base import BaseGenerator


class LeaveGenerator(BaseGenerator):
    def generate(
        self, engagement_layers: list[list[Engagement]], leave_types: dict[str, UUID]
    ) -> list[list[Leave]]:
        leave_type_uuids = list(leave_types.values())

        def construct_leave(engagement: Engagement) -> Leave:
            return Leave(
                leave_type=LeaveType(uuid=random.choice(leave_type_uuids)),
                employee=engagement.employee,
                engagement=EngagementRef(uuid=engagement.uuid),
                validity=Validity(
                    from_date="1930-01-01",
                    to_date=None,
                ),
            )

        return [list(map(construct_leave, layer)) for layer in engagement_layers]
