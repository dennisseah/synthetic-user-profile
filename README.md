# synthetic-user-profile
using generativeAI to generate user profile

## Prerequisites

- python 3.12 or version above
- install poetry (https://python-poetry.org/docs/)
- install vscode (https://code.visualstudio.com/)

## Setup

1. Clone the repository
2. `cd synthetic-user-profile` (root directory of this git repository)
3. `python -m venv .venv`
4. `poetry install` (install the dependencies)
5. code . (open the project in vscode)
6. install the recommended extensions (cmd + shift + p -> `Extensions: Show Recommended Extensions`)
7. `pre-commit install` (install the pre-commit hooks)
```

## Unit Test Coverage

```sh
python -m pytest -p no:warnings --cov-report term-missing --cov=synthetic_user_profile  tests
```

## Dependency Injection

In order to handle the dependency injection, we have a `hosting.py` file in the `synthetic_user_profile` module.
`lagom` is a simple dependency injection library that we use in this project.


## Experiments

We have some code in the `experiments` directory. You can run the experiments by running the following command:

```sh
python -m experiments.profile
```

and then
```sh
python -m experiments.infer
```

