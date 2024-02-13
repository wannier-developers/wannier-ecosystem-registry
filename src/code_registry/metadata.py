# -*- coding: utf-8 -*-
"""Generate the aggregated registry metadata from the registry data."""

import logging
import os
from collections import OrderedDict

import jsonschema

from . import util


logger = logging.getLogger(__name__)


def complete_metadata(code_name, metadata, git_url):
    """Fill-in any missing data for a given code metadata."""

    metadata.setdefault("title", code_name)
    return metadata


def fetch_code_data(code_data, code_name):
    """Fetch additional data for the given code data."""

    # Get Git URL, fail build if git_url is not found or wrong
    git_url = code_data.get("git_url", "")
    hosted_on = util.get_hosted_on(git_url) if git_url else None

    # Check if categories are specified, warn if not
    if "categories" not in code_data:
        logger.info("  >> WARNING: No categories specified.")

    code_data["metadata"] = complete_metadata(code_name, code_data["metadata"], git_url)
    if git_url:
        code_data["gitinfo"] = util.get_git_branches(git_url)

    # Get logo URL, if it has been specified
    if "logo" in code_data["metadata"]:
        code_data["logo"] = code_data["metadata"]["logo"]

    return code_data


def validate_codes_meta(codes_meta, codes_meta_schema):
    """Validate the codes_meta file against the corresponding JSON-schema."""

    jsonschema.validate(instance=codes_meta, schema=codes_meta_schema)

    for code, codedata in codes_meta["codes"].items():
        for category in codedata["categories"]:
            assert category in codes_meta["categories"]


def generate_codes_meta(data, schema=None):
    """Generate (and optionally validate) the comprehensive code registry metadata.

    This function produces the codes_meta file, a comprehensive metadata directory that
    combines the codes data and additionally fetched data (such as the git info).

    The codes_meta file can be used to generate the code registery website and if
    published online, by other platforms that want to operate on the code registry
    and, e.g., integrate with registered codes.
    """

    codes_meta = {
        "codes": OrderedDict(),
        "categories": data.categories,
    }
    logger.info("Fetching code data...")
    for code_name in sorted(data.codes.keys()):
        logger.info(f"  - {code_name}")
        code_data = fetch_code_data(data.codes[code_name], code_name)
        code_data["name"] = code_name
        code_data["subpage"] = os.path.join("codes", util.get_html_code_fname(code_name))
        codes_meta["codes"][code_name] = code_data

    if schema:
        validate_codes_meta(codes_meta, schema)

    return codes_meta
