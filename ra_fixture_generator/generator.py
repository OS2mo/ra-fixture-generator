#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import itertools
import math
from itertools import zip_longest
from operator import add
from uuid import UUID

from more_itertools import prepend
from ra_flatfile_importer.models import MOFlatFileFormat
from ra_flatfile_importer.models import MOFlatFileFormatChunk
from ra_utils.apply import apply
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address
from ramodels.mo.details import Association
from ramodels.mo.details import Engagement
from ramodels.mo.details import ITUser
from ramodels.mo.details import Leave
from ramodels.mo.details import Manager
from ramodels.mo.details import Role

from .generators.association import AssociationGenerator
from .generators.employee import EmployeeGenerator
from .generators.employee_address import EmployeeAddressGenerator
from .generators.engagement import EngagementGenerator
from .generators.it_user import ITUserGenerator
from .generators.leave import LeaveGenerator
from .generators.manager import ManagerGenerator
from .generators.org_address import OrgAddressGenerator
from .generators.org_tree import OrgTreeGenerator
from .generators.org_unit import OrgUnitGenerator
from .generators.role import RoleGenerator


def generate_data(
    size: int,
    classes: dict[str, dict[str, UUID]],
    it_systems: dict[str, UUID],
) -> MOFlatFileFormat:
    employees_per_org = max(2 * int(math.log2(size)), 3)

    org_tree = OrgTreeGenerator().generate(
        size=size,
    )
    org_layers = OrgUnitGenerator().generate(
        org_tree=org_tree,
        org_unit_type_uuid=classes["org_unit_type"][min(classes["org_unit_type"])],
        org_unit_levels=classes["org_unit_level"],
    )
    org_address_layers = OrgAddressGenerator().generate(
        org_layers=org_layers,
        org_unit_address_types=classes["org_unit_address_type"],
    )

    employees = EmployeeGenerator().generate(
        org_layers=org_layers,
        employees_per_org=employees_per_org,
    )
    employee_addresses = EmployeeAddressGenerator().generate(
        employees=employees,
        employee_address_types=classes["employee_address_type"],
    )
    engagement_layers = EngagementGenerator().generate(
        employees=employees,
        org_layers=org_layers,
        employees_per_org=employees_per_org,
        job_functions=classes["engagement_job_function"],
        engagement_types=classes["engagement_type"],
        primary_types=classes["primary_type"],
    )
    manager_layers = ManagerGenerator().generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
        responsibilities=classes["responsibility"],
        manager_levels=classes["manager_level"],
        manager_types=classes["manager_type"],
    )
    association_layers = AssociationGenerator().generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
        association_types=classes["association_type"],
    )
    role_layers = RoleGenerator().generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
        role_types=classes["role_type"],
    )
    leave_layers = LeaveGenerator().generate(
        engagement_layers=engagement_layers,
        leave_types=classes["leave_type"],
    )
    it_users = ITUserGenerator().generate(
        employees=employees,
        it_systems=it_systems,
    )

    # All employee addresses can be merged into the first layer of org-addresses,
    # as employees is a flat layer structure.
    address_layers = list(
        map(
            apply(add),
            zip_longest(org_address_layers, [employee_addresses], fillvalue=[]),
        )
    )

    def construct_chunk(
        org_layer: list[OrganisationUnit],
        employee_layer: list[Employee],
        address_layer: list[Address],
        engagement_layer: list[Engagement],
        manager_layer: list[Manager],
        association_layer: list[Association],
        role_layer: list[Role],
        it_user_layer: list[ITUser],
        leave_layer: list[Leave],
    ) -> MOFlatFileFormatChunk:
        return MOFlatFileFormatChunk(
            org_units=org_layer,
            employees=employee_layer,
            address=address_layer,
            engagements=engagement_layer,
            manager=manager_layer,
            associations=association_layer,
            roles=role_layer,
            leaves=leave_layer,
            it_users=it_user_layer,
        )

    chunks = map(
        apply(construct_chunk),
        zip_longest(
            org_layers,
            [employees],
            # Offset the following by one, by prepending an empty list. This ensures
            # that chunks for their dependencies (i.e. org_units/employees) have been
            # created before they are referenced.
            prepend([], address_layers),
            prepend([], engagement_layers),
            prepend([], manager_layers),
            prepend([], association_layers),
            prepend([], role_layers),
            prepend([], [it_users]),
            # Offset the following by two, as it depends on the previous layers
            itertools.chain(([], []), leave_layers),
            fillvalue=[],
        ),
    )

    mo_flatfile = MOFlatFileFormat(chunks=list(chunks))
    return mo_flatfile
