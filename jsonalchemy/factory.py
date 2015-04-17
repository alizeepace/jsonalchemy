# -*- coding: utf-8 -*-
#
# This file is part of JSONAlchemy.
# Copyright (C) 2015 CERN.
#
# JSONAlchemy is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# JSONAlchemy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JSONAlchemy; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Factory helpers."""

from __future__ import absolute_import

import json

from jsonschema import Draft4Validator

from .wrappers import JSONBase, create_type_from_schema

from .utils import load_schema_from_url


def model_factory(schema_url, bases=()):
    schema = load_schema_from_url(schema_url)

    return create_type_from_schema(schema, bases=bases)()


def compose(*schema_urls):

    import collections

    def update(orig_dict, new_dict):
        for key, val in new_dict.iteritems():
            if isinstance(val, collections.Mapping):
                tmp = update(orig_dict.get(key, {}), val)
                orig_dict[key] = tmp
            elif isinstance(val, list):
                # FIXME we can't merge lists nicely
                raise RuntimeError()
            else:
                orig_dict[key] = new_dict[key]
        return orig_dict

    result = {}
    for schema_url in schema_urls:
            schema = load_schema_from_url(schema_url)
            update(result, schema)

    validator = Draft4Validator(result)
    return result
