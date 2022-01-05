<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Fixture Generator

OS2mo Flatfile Fixture Generator.

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
docker run --rm ra-fixture-generator --help
```
Which yields:
```
Usage: ra_fixture_generator [OPTIONS]

  Flatfile Fixture Generator.

  Used to generate flatfile fixture data (JSON) for OS2mo.

Options:
  --root-org-name TEXT  Name of the root organisation  [env var: ROOT_ORG_NAME; default: Magenta Aps]
  --size INTEGER        Size of the generated dataset  [env var: FIXTURE_SIZE; default: 10]
  --indent INTEGER      Pass 'indent' to json serializer
  --mo-file FILENAME    Output OS2mo Flatfile  [required]
  --help                Show this message and exit.
```
At this point, the flat file can be generated with:
```
docker run --rm -v $PWD:/srv/ ra-fixture-generator \
    --name "Aarhus Kommune" --lora-file /srv/lora.json --mo-file /srv/mo.json
```
At which point the file `mo.json` will be available in the current work-dir.
This file can then be uploaded using the `ra-flatfile-importer`.

For instance using:
```
docker run -i --rm ra-flatfile-importer mo upload --mo-url http://MOURL:5000 < mo.json
```

Alternatively the two can be combined:
```
docker run -i --rm ra-fixture-generator \
   --name "Aarhus Kommune" --mo-file - | \
docker run -i --rm ra-flatfile-importer mo upload --mo-url http://MOURL:5000
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
- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](LICENSES/MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
