# -*- coding: utf-8 -*-
"""Manage a registry of codes."""

from .core import CodeRegistryData
from .core import CodeRegistrySchemas
from .metadata import generate_codes_meta
from .version import __version__
from .web import build_from_config
from .web import build_html
from .web import write_schemas


__all__ = [
    "CodeRegistryData",
    "CodeRegistrySchemas",
    "__version__",
    "build_from_config",
    "build_html",
    "generate_codes_meta",
    "write_schemas",
]
