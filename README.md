<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Fixture Generator


## Usage
The primary usage of the tool is to generate a fixture set for OS2mo in a format usable by
[ra-flatfile-importer](https://git.magenta.dk/rammearkitektur/ra-flatfile-importer).
```
Usage: python -m ra_fixture_generator [OPTIONS]

  Flatfile Fixture Generator.

  Used to generate flatfile fixture data (JSON) for OS2mo.

Options:
  -s, --size INTEGER          Size of the generated dataset. The number of generated employees roughly scales in 50n *log₂n.
                              [env var: FIXTURE_SIZE; default: 10]
  --mo-url TEXT               OS2mo URL.  [env var: MO_URL; required]
  --client-id TEXT            Client ID used to authenticate against OS2mo.  [env var: CLIENT_ID; default: dipex; required]
  --client-secret TEXT        Client secret used to authenticate against OS2mo.  [env var: CLIENT_SECRET; required]
  --auth-server TEXT          Keycloak authentication server.  [env var: AUTH_SERVER; required]
  --auth-realm TEXT           Keycloak realm for OS2mo authentication.  [env var: AUTH_REALM; default: mo]
  -o, --output-file FILENAME  Output OS2mo flatfile to FILENAME.  [default: mo.json]
  -i, --indent INTEGER        Pass 'indent' to json serializer.
  --help                      Show this message and exit.
```
On a development machine with the OS2mo stack running, the following command will generate a small fixture dataset:
```
python -m ra_fixture_generator \
  --mo-url=http://localhost:5000 \
  --client-secret=603f1c82-d012-4d04-9382-dbe659c533fb \
  --auth-server=http://localhost:8081/auth \
  --size=10 \
  --output-file mo.json
```
At which point the file `mo.json` will be available in the current work-dir.  This file can then be uploaded using
[ra-flatfile-importer](https://git.magenta.dk/rammearkitektur/ra-flatfile-importer). Alternatively the two processes can
be combined using [os2mo-fixture-loader](https://git.magenta.dk/rammearkitektur/os2mo-fixture-loader).


## Prerequisite
This tool requires that a minimal OS2mo stack is configured and reachable. This is due to the fact that facets and
classes in OS2mo are referenced by their UUIDs, thus the generator needs knowledge of the specific UUIDs on the OS2mo
instance targeted by the fixture.

In addition, at least one class needs to be configured for the following facets:
  - `org_unit_type`
  - `employee_address_type`
  - `engagement_job_function`
  - `engagement_type`
  - `responsibility`
  - `manager_level`
  - `manager_type`
  - `association_type`

and `org_unit_level` needs to have at least 8 classes defined, which will be used in lexicographic order for
organisation units on each level in the organisational tree.

A recommended [os2mo-init](https://git.magenta.dk/rammearkitektur/os2mo-init) configuration, which adds a default set of
classes, is available in [init.config.yml](init.config.yml). **NOTE** that this configuration must be run in _addition_
to the default configuration, which means a completely empty stack must run os2mo-init _twice_.


## Versioning
This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing data models
- MINOR: Backwards compatible updates to existing data models OR new models added
- PATCH: Backwards compatible bug fixes


## Authors
Magenta ApS <https://magenta.dk>


## License
- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](LICENSES/MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
