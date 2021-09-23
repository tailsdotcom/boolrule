#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from boolrule import BoolRule, MissingVariableException


@pytest.mark.parametrize('s,expected', [
    ('5 > 3', True),
    ('5 < 3', False),
    ('5 > 5', False),
    ('3 >= 5', False),
    ('5 >= 3', True),
    ('5 >= 5', True),
    ('5 <= 3', False),
    ('3 <= 5', True),
    ('3 <= 5', True),
    ('5 ≥ 3', True),
    ('5 ≥ 5', True),
    ('3 ≤ 3', True),
    ('3 ≤ 5', True),
    ('7 == true', False),
    ('true == true', True),
    ('None is None', True),
    ('1 != 2', True),
    ('1 != 1', False),
    ('2 != true', True),
    ('1 ≠ 2', True),
    ('1 ≠ 1', False),
    ('2 ≠ true', True),
])
def test_simple_comparisons(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected


@pytest.mark.parametrize('s,expected', [
    ('5 > 3 and 3 > 1', True),
    ('5 > 3 and 3 > 5', False),
    ('5 > 3 or 3 > 5', True)
])
def test_logical_combinations(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected


@pytest.mark.parametrize('s,expected', [
    ('5 > 3 and (3 > 5 or 3 > 1)', True),
    ('5 > 3 and (3 > 5 and 3 < 1)', False),
])
def test_nested_logical_combinations(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected

@pytest.mark.parametrize('s,expected', [
    ('(1=1 or 2=2) and (3 = 3)', True),
    ('(1=1 or 2=2) and (3 = 4)', False),
])
def test_nested_logical_combinations_and_error(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected

@pytest.mark.parametrize('s,context,expected', [
    ('foo = "bar" AND baz > 10', {'foo': 'bar', 'baz': 20}, True),
    ('foo = "bar" AND baz > 10', {'foo': 'bar', 'baz': 9}, False),
    (
        'foo = "bar" AND ("a" = "b" OR baz > 10)',
        {'foo': 'bar', 'baz': 11}, True
    ),
    ('foo.bar = "bar"', {'foo': {'bar': 'bar'}}, True),
    ('foo.bar isnot none', {'foo': {'bar': 4}}, True),
    ('foo.bar is none', {'foo': {'bar': 4}}, False),
    ('foo.bar is none', {'foo': {'bar': None}}, True),
])
def test_subsitution_values(s, context, expected):
    boolrule = BoolRule(s)
    assert boolrule.test(context) == expected


@pytest.mark.parametrize('s,context,expected', [
    ('1=1 and 2 in (1, true)', {}, False),
    ('x in (5, 6, 7)', {'x': 5}, True),
    ('x in (5, 6, 7)', {'x': 8}, False),
    ('x in (5, 6, 7, y)', {'x': 99, 'y': 99}, True),
    ('x ∈ (5, 6, 7)', {'x': 5}, True),
    ('x ∈ (5, 6, 7)', {'x': 8}, False),
    ('x ∈ (5, 6, 7, y)', {'x': 99, 'y': 99}, True),
    ('x ∉ (5, 6, 7)', {'x': 5}, False),
    ('x ∉ (5, 6, 7)', {'x': 8}, True),
    ('x ∉ (5, 6, 7, y)', {'x': 99, 'y': 99}, False),
])
def test_list_membership(s, context, expected):
    boolrule = BoolRule(s)
    assert boolrule.test(context) == expected


@pytest.mark.parametrize('s,expected', [
    ('(1, 2, 3) ⊆ (1, 2, 3)', True),
    ('(1, 2, 3) ⊇ (1, 2, 3)', True),
    ('(1, 2, 3) ⊆ (1, 2, 3, 4)', True),
    ('(1, 2, 3, 4) ⊇ (1, 2, 3)', True),
    ('(1, 2, 3) ⊆ (1, 2)', False),
    ('(1, 2) ⊇ (1, 2, 3)', False),
])
def test_subset(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected


@pytest.mark.parametrize('s,expected', [
    ('(1, 2, 3) ∩ (1, 2, 3)', True),
    ('(4) ∩ (3, 4, 5)', True),
    ('(1, 2, 3) ∩ (4, 5, 6)', False),
])
def test_intersects(s, expected):
    boolrule = BoolRule(s)
    assert boolrule.test() == expected


@pytest.mark.parametrize('s,context', [
    ('foo < bar', None),
    ('foo < bar', {}),
    ('foo < bar', {'foo': 5}),
])
def test_missing_vars_raises_exception(s, context):
    with pytest.raises(MissingVariableException):
        boolrule = BoolRule(s)
        boolrule.test(context)


@pytest.mark.parametrize('s', [
    # unbalanced brackets
    ('5 > 4)',),
    # ambiguous list
    ('1=1 and 2 in (1, 3 = 3)',),
])
def test_malformed_queries_raises_exception(s):
    with pytest.raises(Exception):
        BoolRule(s)
