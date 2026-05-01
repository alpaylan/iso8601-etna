"""Witness functions — one `def witness_<snake>_case_<tag>() -> PropertyResult`
per witness in the manifest. Plain function, zero arguments, no decorators,
no randomness. Calls a property with frozen inputs.

Each witness must:
  * Pass on the base tree (PropertyResult.is_pass).
  * Fail when the corresponding patch is reverse-applied
    (PropertyResult.is_fail).
"""
from __future__ import annotations

from ._result import PropertyResult
from .properties import (
    property_is_iso8601_raises_on_internal_error,
    property_microsecond_preserves_all_digits,
    property_negative_timezone_minutes_negated,
    property_parse_date_wraps_value_error,
    property_parse_error_is_value_error,
    property_year_must_be_four_digits,
    property_year_only_parses,
    property_z_is_always_utc,
)


# IsIso8601RaisesOnInternalError -------------------------------------------
def witness_is_iso8601_raises_on_internal_error_case_bytes() -> PropertyResult:
    return property_is_iso8601_raises_on_internal_error(b"2007-01-25")


# YearMustBeFourDigits -----------------------------------------------------
def witness_year_must_be_four_digits_case_three_digit() -> PropertyResult:
    return property_year_must_be_four_digits(999)


# YearOnlyParses -----------------------------------------------------------
def witness_year_only_parses_case_2007() -> PropertyResult:
    return property_year_only_parses(2007)


# ZIsAlwaysUtc -------------------------------------------------------------
def witness_z_is_always_utc_case_plus_five_thirty() -> PropertyResult:
    return property_z_is_always_utc((5, 30))


# NegativeTimezoneMinutesNegated -------------------------------------------
def witness_negative_timezone_minutes_negated_case_minus_one_thirty() -> PropertyResult:
    return property_negative_timezone_minutes_negated((1, 30))


# MicrosecondPreservesAllDigits --------------------------------------------
def witness_microsecond_preserves_all_digits_case_502099() -> PropertyResult:
    return property_microsecond_preserves_all_digits(502099)


# ParseDateWrapsValueError -------------------------------------------------
def witness_parse_date_wraps_value_error_case_month_thirteen() -> PropertyResult:
    return property_parse_date_wraps_value_error((2007, 13, 25))


# ParseErrorIsValueError ---------------------------------------------------
def witness_parse_error_is_value_error_case_garbage() -> PropertyResult:
    return property_parse_error_is_value_error(0)
