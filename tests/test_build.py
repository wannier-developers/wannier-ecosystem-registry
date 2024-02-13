# -*- coding: utf-8 -*-

import pytest
import base64
from dataclasses import dataclass

import requests

import code_registry


@pytest.fixture
def code_git_url():
    return "https://github.com/aiidalab/aiidalab-hello-world.git"


@pytest.fixture
def code_metadata_url():
    """A URL for the test code metadata."""
    return "https://raw.githubusercontent.com/aiidalab/aiidalab-hello-world/master/metadata.json"


@pytest.fixture
def code_logo_url():
    """A URL for the test code logo."""
    return "https://raw.githubusercontent.com/aiidalab/aiidalab-hello-world/master/img/logo.png"


@pytest.fixture
def code_logo_img():
    """A one-pixel large 'logo' for the test code."""
    return base64.b64decode(
        b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAAAA1BMVEX/TQBcNTh/AAAAAXRSTlPM0jRW/QAAAApJREFUeJxjYgAAAAYAAzY3fKgAAAAASUVORK5CYII="
    )


@pytest.fixture
def code_logo(requests_mock, code_logo_url, code_logo_img):
    @dataclass
    class CodeLogo:
        url = code_logo_url
        img = code_logo_img

    requests_mock.get(code_logo_url, content=code_logo_img)
    return CodeLogo


@pytest.fixture
def code_metadata(requests_mock, code_logo):
    """Create metadata content for a test code."""
    return {
        "description": "A test code that does not really exist.",
        "version": "1.0.0",
        "logo": code_logo.url,
    }


@pytest.fixture
def codes_yaml(requests_mock, code_git_url, code_metadata):
    """Create codes.yaml content with one test code entry."""
    codes_yaml = {
        "test": {
            "git_url": code_git_url,
            "metadata": code_metadata,
            "categories": ["utilities"],
        }
    }
    requests_mock.get(code_git_url)
    yield codes_yaml


@pytest.fixture
def categories_yaml():
    """Create categories.yaml content."""
    return {
        "utilities": {
            "title": "Utilities",
            "description": "Utility codes for everyday tasks.",
        }
    }


@pytest.fixture
def code_registry_data(codes_yaml, categories_yaml):
    """Create code registry data content."""
    return code_registry.CodeRegistryData(codes=codes_yaml, categories=categories_yaml)


@pytest.fixture
def code_registry_schemas(codes_schema, categories_schema):
    """Create code registry schema content."""
    return code_registry.CodeRegistrySchemas(
        codes=codes_schema, categories=categories_schema
    )


@pytest.mark.usefixtures("mock_schema_endpoints")
def test_generate_codes_meta(code_registry_data, codes_meta_schema):
    codes_meta = code_registry.generate_codes_meta(
        data=code_registry_data, schema=codes_meta_schema
    )
    # Very basic validation here, the codes_meta.json file is already validated via the schema:
    assert "codes" in codes_meta
    assert "categories" in codes_meta

    # Check that the test code metadata is present.
    assert "test" in codes_meta["codes"]
    assert (
        codes_meta["codes"]["test"]["git_url"]
        == code_registry_data.codes["test"]["git_url"]
    )
    assert all(
        cat in codes_meta["categories"]
        for cat in codes_meta["codes"]["test"]["categories"]
    )


@pytest.mark.usefixtures("mock_schema_endpoints")
def test_get_logo_url(code_registry_data, code_logo_url, codes_meta_schema):
    """Test whether the logo url is correctly resolved."""
    codes_meta = code_registry.generate_codes_meta(
        data=code_registry_data, schema=codes_meta_schema
    )
    assert codes_meta["codes"]["test"]["logo"] == code_logo_url
    r = requests.get(code_logo_url)
    assert r.status_code == 200
