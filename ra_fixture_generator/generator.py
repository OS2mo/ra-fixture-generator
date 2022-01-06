#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import math
from itertools import zip_longest
from operator import add
from typing import List

from more_itertools import prepend
from ra_flatfile_importer.mo.models import MOFlatFileFormat
from ra_flatfile_importer.mo.models import MOFlatFileFormatChunk
from ra_utils.apply import apply
from ramodels.mo import Employee
from ramodels.mo import OrganisationUnit
from ramodels.mo.details import Address
from ramodels.mo.details import Association
from ramodels.mo.details import Engagement
from ramodels.mo.details import Manager

from .generators.association import AssociationGenerator
from .generators.employee import EmployeeGenerator
from .generators.employee_address import EmployeeAddressGenerator
from .generators.engagement import EngagementGenerator
from .generators.manager import ManagerGenerator
from .generators.org_address import OrgAddressGenerator
from .generators.org_tree import OrgTreeGenerator
from .generators.org_unit import OrgUnitGenerator


def generate_data(name: str, size: int) -> MOFlatFileFormat:
    random.seed(name)
    employees_per_org = max(2 * int(math.log2(size)), 3)

    org_tree = OrgTreeGenerator().generate(
        size=size,
    )
    org_layers = OrgUnitGenerator().generate(
        org_tree=org_tree,
    )
    org_address_layers = OrgAddressGenerator().generate(
        org_layers=org_layers,
    )

    employees = EmployeeGenerator().generate(
        org_layers=org_layers,
        employees_per_org=employees_per_org,
    )
    employee_addresses = EmployeeAddressGenerator().generate(
        employees=employees,
    )
    engagement_layers = EngagementGenerator().generate(
        employees=employees,
        org_layers=org_layers,
        job_functions=default_classes["engagement_job_function"],
        engagement_types=default_classes["engagement_type"],
        employees_per_org=employees_per_org,
    )
    manager_layers = ManagerGenerator().generate(
        org_layers=org_layers,
        employees=employees,
        responsibilities=default_classes["responsibility"],
        manager_levels=default_classes["manager_level"],
        manager_types=default_classes["manager_type"],
        employees_per_org=employees_per_org,
    )
    association_layers = AssociationGenerator().generate(
        org_layers=org_layers,
        employees=employees,
        association_types=default_classes["association_type"],
        employees_per_org=employees_per_org,
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
        org_layer: List[OrganisationUnit],
        employee_layer: List[Employee],
        address_layer: List[Address],
        engagement_layer: List[Engagement],
        manager_layer: List[Manager],
        association_layer: List[Association],
    ) -> MOFlatFileFormatChunk:
        return MOFlatFileFormatChunk(
            org_units=org_layer,
            address=address_layer,
            employees=employee_layer,
            engagements=engagement_layer,
            manager=manager_layer,
            associations=association_layer,
        )

    # TODO: mo_flatfile needs it
    # TODO: mo_flatfile needs role
    # TODO: mo_flatfile needs leave
    # TODO: What about classes?

    chunks = map(
        apply(construct_chunk),
        zip_longest(
            org_layers,
            [employees],
            # Offset the following by one, by prepending an empty list.
            # This ensures that their dependencies (i.e. org_units/employees)
            # have been created in the chunk, before they are needed
            prepend([], address_layers),
            prepend([], engagement_layers),
            prepend([], manager_layers),
            prepend([], association_layers),
            fillvalue=[],
        ),
    )

    mo_flatfile = MOFlatFileFormat(chunks=list(chunks))
    return mo_flatfile
