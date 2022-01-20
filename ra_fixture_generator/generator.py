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

    org_tree = OrgTreeGenerator().generate(size=size)
    org_layers = OrgUnitGenerator(org_unit_levels=classes["org_unit_level"]).generate(
        org_tree=org_tree,
        org_unit_type_uuid=classes["org_unit_type"][min(classes["org_unit_type"])],
    )
    org_address_generator = OrgAddressGenerator(
        org_unit_address_types=classes["org_unit_address_type"]
    )
    org_address_layers = org_address_generator.generate(
        org_layers=org_layers,
    )
    org_address_modifications = org_address_generator.generate_modifications(
        address_layers=org_address_layers,
        org_layers=org_layers,
    )

    employee_generator = EmployeeGenerator()
    employees = employee_generator.generate(
        org_layers=org_layers,
        employees_per_org=employees_per_org,
    )

    employee_address_generator = EmployeeAddressGenerator(
        employee_address_types=classes["employee_address_type"]
    )
    employee_addresses = employee_address_generator.generate(
        employees=employees,
    )
    employee_address_modifications = employee_address_generator.generate_modifications(
        addresses=employee_addresses,
    )

    engagement_generator = EngagementGenerator(
        job_functions=classes["engagement_job_function"],
        engagement_types=classes["engagement_type"],
        primary_types=classes["primary_type"],
    )
    engagement_layers = engagement_generator.generate(
        employees=employees,
        org_layers=org_layers,
        employees_per_org=employees_per_org,
    )
    engagement_modifications = engagement_generator.generate_modifications(
        engagement_layers=engagement_layers,
        org_layers=org_layers,
    )

    manager_generator = ManagerGenerator(
        responsibilities=classes["responsibility"],
        manager_levels=classes["manager_level"],
        manager_types=classes["manager_type"],
    )
    manager_layers = manager_generator.generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
    )
    manager_modifications = manager_generator.generate_modifications(
        manager_layers=manager_layers,
        org_layers=org_layers,
    )

    association_layers = AssociationGenerator(
        association_types=classes["association_type"],
    ).generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
    )

    role_generator = RoleGenerator(role_types=classes["role_type"])
    role_layers = role_generator.generate(
        org_layers=org_layers,
        employees=employees,
        employees_per_org=employees_per_org,
    )
    role_modifications = role_generator.generate_modifications(
        role_layers=role_layers,
        org_layers=org_layers,
    )

    leave_generator = LeaveGenerator(leave_types=classes["leave_type"])
    leave_layers = leave_generator.generate(
        engagement_layers=engagement_layers,
    )
    leave_modifications = leave_generator.generate_modifications(
        leave_layers=leave_layers,
        engagement_layers=engagement_layers,
    )

    it_user_generator = ITUserGenerator(it_systems=it_systems)
    it_users = it_user_generator.generate(
        employees=employees,
    )
    it_user_modifications = it_user_generator.generate_modifications(
        it_users=it_users,
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
            prepend(
                [],
                address_layers
                + [org_address_modifications]
                + [employee_address_modifications],
            ),
            prepend([], engagement_layers + [engagement_modifications]),
            prepend([], manager_layers + [manager_modifications]),
            prepend([], association_layers),
            prepend([], role_layers + [role_modifications]),
            prepend([], [it_users] + [it_user_modifications]),
            # Offset the following by two, as it depends on the previous layers
            itertools.chain(([], []), leave_layers + [leave_modifications]),
            fillvalue=[],
        ),
    )

    mo_flatfile = MOFlatFileFormat(chunks=list(chunks))
    return mo_flatfile
