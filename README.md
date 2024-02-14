# Wannier-Functions Software Ecosystem Registry code entry

This repository contains the **source code** of the official Wannier-Functions Software Ecosystem Registry code entry.

<p align="center">
 <a href="https://wannier-developers.github.io/wannier-ecosystem-registry" rel="Go to the registry">
  <img src="src/static/gotobutton.svg">
 </a>
</p>

## Adding an code to the registry

All codes that are part of this registry must adhere to the following requirements:

- The code is interfaced with the Wannier90 code.

Codes are added to the registry by adding an entry to the `codes.yaml` file within this repository.

1. Create a pull request to this repository that adds a new entry to the `codes.yaml` file, e.g., by [editing the file directly in the browser](https://github.com/wannier-developers/wannier-ecosystem-registry/edit/main/codes.yaml). Example:

    ```yaml
    QuantumESPRESSO:
    categories:
        - ab-initio_engines
    metadata:
        description: |
            Quantum ESPRESSO is an integrated suite of open-source computer codes for quantum simulations of materials using state-of-the art electronic-structure techniques, based on density-functional theory, density-functional perturbation theory, and many-body perturbation theory, within the plane-wave pseudo-potential and projector-augmented-wave approaches
        homepage_url: https://www.quantum-espresso.org
        sourcecode_url: https://gitlab.com/QEF/q-e
        documentation_url: https://www.quantum-espresso.org/documentation/
        title: Quantum ESPRESSO
        logo: https://www.quantum-espresso.org/wp-content/uploads/2022/03/quantum_ogo_ok.png
    ```

    **Note**: To check which fields are optional, refer to the `valid keys` subsection; but it is highly encouraged to fill in all the fields to process your PR quickly. The `categories` field must contain at least one item.


2. Your code will show up in the [Wannier-Functions Software Ecosystem Registry](https://wannier-developers.github.io/wannier-ecosystem-registry) once your pull request is approved and merged.

**Tip**: The registry supports the `$ref` syntax to reference externally hosted documents.
That means you can reference metadata that is hosted at a different location, which makes it easier to dynamically update it.
For example, if you place a `metadata.yaml` file within your code repository, then you can reference that file like this:

```yaml
my-code:
  metadata:
    $ref: https://github.com/my-org/my-code/raw/main/metadata.yaml
  categories:
    - ab-initio_engines
```
You can even reference only parts of the metadata, example:
```yaml
my-code:
  metadata:
    title: my-code
    description:
      $ref: https://github.com/my-org/my-code/raw/main/metadata.yaml#description
  categories:
    - ab-initio_engines
```

*Feel free to propose a new codes category to be added to [`category.yaml`](https://github.com/wannier-developers/wannier-ecosystem-registry/blob/main/categories.yaml)) before adding your code.*


### Valid keys for code entries in `codes.yaml`

| Key | Requirement | Description |
|:---:|:---:|:---|
| `metadata` | **Mandatory** | General description of the code (see below). |
| `categories` | **Mandatory** | An array of categories, where each category must be one of the categories specified in [`categories.yaml`](https://github.com/big-map/big-map-registry/blob/main/categories.yaml). |

### Valid keys for code metadata

| Key | Requirement | Description |
|:---:|:---:|:---|
| `title` | **Mandatory** | The title will be displayed in the list of codes. |
| `description` | **Mandatory** | The description will be displayed on the detail page of your code. |
| `homepage_url` | **Mandatory** | Link to the home page of the code. |
| `documentation_url` | Optional | The link to the online wannier-interface (or general) documentation of the code (e.g. on [Read The Docs](https://readthedocs.org/)). |
| `sourcecode_url` | Optional |   Link to the source code. Can be github, gitlab or any other publicly available repository. |
| `logo` | Optional | Url to a logo file (png or jpg). |

## Information for maintainers

To prepare a development environment, please run the following steps:
```console
$ pip install -r src/requirements.txt -r tests/requirements.txt
$ pre-commit install
```

This will install all requirements needed to run the git pre-commit hooks (linters), build the website locally, and execute the test framework.

To execute tests, run:
```console
$ PYTHONPATH=src pytest
```

Executed tests include unit, integration, and validation tests.
The validation tests check the validity of all schema files, the data files e.g. `codes.yaml` and `categories.yaml`, and – if present – the configuration file (`config.yaml`).

To generate the website, simply execute the following script:

```console
$ python src/build.py
```

The continuous-integration workflow is implemented with GitHub actions, which runs the pre-commit hooks, unit, integration, and validation tests.
In addition, all commits on the `main` branch are automatically deployed to GitHub pages.

## Acknowledgements

This project has received funding from the European Union’s [Horizon 2020 research and innovation programme](https://ec.europa.eu/programmes/horizon2020/en) under grant agreement [No 957189](https://cordis.europa.eu/project/id/957189). The project is part of BATTERY 2030+, the large-scale European research initiative for inventing the sustainable batteries of the future.
