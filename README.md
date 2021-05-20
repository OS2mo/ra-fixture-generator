<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Fixture Generator

OS2mo/LoRa Flatfile Fixture Generator.

## Usage
```
docker build . -t ra-fixture-generator
```
Which yields:
```
...
Successfully built ...
Successfully tagged ra-fixture-generator:latest
```
After which you can run:
```
docker run --rm ra-fixture-generator
```
Which yields:
```
...
```

## Versioning
This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing data models
- MINOR: Backwards compatible updates to existing data models OR new models added
- PATCH: Backwards compatible bug fixes

<!--
## Getting Started

TODO: README section missing!

### Prerequisites


TODO: README section missing!

### Installing

TODO: README section missing!

## Running the tests

TODO: README section missing!

## Deployment

TODO: README section missing!

## Built With

TODO: README section missing!

## Authors

Magenta ApS <https://magenta.dk>

TODO: README section missing!
-->
## License
- This project: [MPL-2.0](MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
