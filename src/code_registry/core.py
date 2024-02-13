# -*- coding: utf-8 -*-
"""Core data classes for the registry."""
from dataclasses import dataclass

import jsonschema


@dataclass
class CodeRegistrySchemas:
    """The code registry JSON-schema objects."""

    codes: dict
    categories: dict
    codes_meta: dict
    metadata: dict


@dataclass
class CodeRegistryData:
    """The code registry data objects (codes and categories)."""

    codes: dict
    categories: dict

    def validate(self, schemas: CodeRegistrySchemas):
        """Validate the registry data against the provided registry schemas."""
        jsonschema.validate(instance=self.codes, schema=schemas.codes)
        jsonschema.validate(instance=self.categories, schema=schemas.categories)
