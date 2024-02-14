# -*- coding: utf-8 -*-
"""Utility functions for the registry."""

import json
import string
from pathlib import Path
from urllib.parse import urlparse

from dulwich.client import get_transport_and_path_from_url


def get_html_code_fname(code_name):
    valid_characters = set(string.ascii_letters + string.digits + "_-")

    simple_string = "".join(c for c in code_name if c in valid_characters)

    return f"{simple_string}.html"


def get_git_branches(sourcecode_url):
    t, p = get_transport_and_path_from_url(sourcecode_url)
    branches = t.get_refs(p)
    res = {}
    for key, value in branches.items():
        res[key.decode("utf-8")] = value.decode("utf-8")
    return res


def get_git_author(sourcecode_url):
    return urlparse(sourcecode_url).path.split("/")[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())
