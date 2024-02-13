from pathlib import Path

import pytest
import jsonschema

from code_registry import yaml

ROOT = Path(__file__).parent.parent.resolve()


@pytest.fixture
def codes_yaml():
    return yaml.load(ROOT.joinpath("codes.yaml"))


@pytest.fixture
def categories_yaml():
    return yaml.load(ROOT.joinpath("categories.yaml"))


@pytest.fixture
def valid_categories(categories_yaml):
    return set(categories_yaml)


def test_validate_codes_schema(codes_schema):
    jsonschema.Draft7Validator.check_schema(codes_schema)


def test_validate_codes_meta_schema(codes_meta_schema):
    jsonschema.Draft7Validator.check_schema(codes_meta_schema)


def test_validate_categories_schema(categories_schema):
    jsonschema.Draft7Validator.check_schema(categories_schema)


def test_validate_metadata_schema(metadata_schema):
    jsonschema.Draft7Validator.check_schema(metadata_schema)


def test_validate_codes_yaml_schema(
    validate, codes_schema, codes_yaml, valid_categories
):
    validate(instance=codes_yaml, schema=codes_schema)


def test_validate_codes_yaml_categories(codes_yaml, valid_categories):
    for code in codes_yaml.values():
        for category in code.get("categories", []):
            assert category in valid_categories


def test_validate_categories_yaml(validate, categories_schema, categories_yaml):
    validate(instance=categories_yaml, schema=categories_schema)
