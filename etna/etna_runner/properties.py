"""Property functions for the iso8601 ETNA workload.

Each property is pure, total, deterministic. Returns PropertyResult.

The PascalCase manifest name maps to property_<snake> here via
scripts/check_python_workload.py:pascal_to_snake.
"""
from __future__ import annotations

import datetime
from typing import Tuple

import iso8601

from ._result import PASS, PropertyResult, fail


# ---------------------------------------------------------------------------
# IsIso8601RaisesOnInternalError (variant: is_iso8601_returns_false_on_exception_fde429d_1)
# ---------------------------------------------------------------------------
def property_is_iso8601_raises_on_internal_error(args: bytes) -> PropertyResult:
    """is_iso8601 must surface internal errors as ParseError, not silently
    return False.

    Bug (fde429d): the original ``except Exception: return False`` path
    swallowed any error from ``re.match`` (e.g. when the caller passes a
    bytes-like object) and reported the input as "not ISO 8601" instead of
    flagging the misuse. The fix raises ``ParseError`` instead.
    """
    payload = args
    try:
        result = iso8601.is_iso8601(payload)  # type: ignore[arg-type]
    except iso8601.ParseError:
        return PASS
    return fail(
        f"is_iso8601({payload!r}) returned {result!r}; "
        f"expected ParseError because re.match cannot accept bytes"
    )


# ---------------------------------------------------------------------------
# YearMustBeFourDigits (variant: year_unconstrained_dc7f577_1)
# ---------------------------------------------------------------------------
def property_year_must_be_four_digits(args: int) -> PropertyResult:
    """A bare 1-3 digit year string must raise ParseError.

    Bug (dc7f577): when the year regex was unconstrained (``[0-9]+``),
    inputs like "999" parsed as year=999 and returned a valid datetime
    instead of raising. ISO 8601 requires a 4-digit year.
    """
    n = args
    if not (1 <= n <= 999):
        return PASS
    candidate = str(n)
    try:
        parsed = iso8601.parse_date(candidate)
    except iso8601.ParseError:
        return PASS
    return fail(
        f"parse_date({candidate!r}) returned {parsed!r}; "
        f"expected ParseError because the year is not 4 digits"
    )


# ---------------------------------------------------------------------------
# YearOnlyParses (variant: regex_requires_full_date_6d33d31_1)
# ---------------------------------------------------------------------------
def property_year_only_parses(args: int) -> PropertyResult:
    """A bare 4-digit year string ("YYYY") must parse as January 1 of that year.

    Bug (6d33d31): the regex used to require month and day. ``parse_date("2007")``
    raised ParseError instead of returning datetime(2007, 1, 1).
    """
    year = args
    if not (1 <= year <= 9999):
        return PASS
    candidate = f"{year:04d}"
    try:
        parsed = iso8601.parse_date(candidate)
    except iso8601.ParseError as e:
        return fail(
            f"parse_date({candidate!r}) raised ParseError({e}); "
            f"expected datetime({year}, 1, 1, ...) (YYYY-only must parse)"
        )
    if parsed.year != year or parsed.month != 1 or parsed.day != 1:
        return fail(
            f"parse_date({candidate!r}) returned {parsed!r}; "
            f"expected year={year}, month=1, day=1"
        )
    return PASS


# ---------------------------------------------------------------------------
# ZIsAlwaysUtc (variant: z_uses_default_tz_704a58e_1)
# ---------------------------------------------------------------------------
def property_z_is_always_utc(args: Tuple[int, int]) -> PropertyResult:
    """A trailing ``Z`` always denotes UTC, regardless of ``default_timezone``.

    Bug (704a58e): the original implementation routed ``Z`` through
    ``default_timezone``, so ``parse_date("...Z", default_timezone=tz)``
    returned a datetime in ``tz`` instead of UTC.
    """
    offset_hours, offset_minutes = args
    if not (-14 <= offset_hours <= 14):
        return PASS
    if not (0 <= offset_minutes <= 59):
        return PASS
    if offset_hours == 0 and offset_minutes == 0:
        return PASS  # offset == UTC, can't distinguish
    tz = iso8601.FixedOffset(offset_hours, offset_minutes, "custom")
    parsed = iso8601.parse_date("2007-01-25T12:00:00Z", default_timezone=tz)
    actual = parsed.utcoffset()
    expected = datetime.timedelta(0)
    if actual != expected:
        return fail(
            f"parse_date('2007-01-25T12:00:00Z', default_timezone=FixedOffset({offset_hours}, {offset_minutes}, ...)) "
            f"utcoffset={actual!r}; expected {expected!r} (Z must be UTC)"
        )
    return PASS


# ---------------------------------------------------------------------------
# NegativeTimezoneMinutesNegated (variant: negative_tz_minutes_dropped_d724fec_1)
# ---------------------------------------------------------------------------
def property_negative_timezone_minutes_negated(args: Tuple[int, int]) -> PropertyResult:
    """For a negative timezone offset, the minute portion must also be negated.

    Bug (d724fec): the original code only negated the hour, so an offset
    of ``-01:30`` was interpreted as -60 + 30 = -30 minutes instead of -90.
    """
    hours, minutes = args
    if not (1 <= hours <= 14):
        return PASS
    if not (1 <= minutes <= 59):
        return PASS
    candidate = f"2007-01-25T12:00:00-{hours:02d}:{minutes:02d}"
    parsed = iso8601.parse_date(candidate)
    actual = parsed.utcoffset()
    expected = -datetime.timedelta(hours=hours, minutes=minutes)
    if actual != expected:
        return fail(
            f"parse_date({candidate!r}).utcoffset()={actual!r}; expected {expected!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# MicrosecondPreservesAllDigits (variant: microsecond_float_rounding_81ff287_1)
# ---------------------------------------------------------------------------
def property_microsecond_preserves_all_digits(args: int) -> PropertyResult:
    """The microsecond field of the parsed datetime must equal the literal
    6-digit fraction in the input.

    Bug (81ff287): the original code computed
    ``int(float("0.<frac>") * 1e6)``, which off-by-ones for many fractions
    due to binary float rounding (e.g. "0.502099" -> 502098). The fix uses
    ``Decimal`` arithmetic, which preserves all six digits.
    """
    n = args
    if not (0 <= n <= 999_999):
        return PASS
    frac = f"{n:06d}"
    candidate = f"2007-01-25T12:00:00.{frac}Z"
    parsed = iso8601.parse_date(candidate)
    if parsed.microsecond != n:
        return fail(
            f"parse_date({candidate!r}).microsecond={parsed.microsecond}; "
            f"expected {n} (6-digit fraction)"
        )
    return PASS


# ---------------------------------------------------------------------------
# ParseDateWrapsValueError (variant: parse_date_unwrapped_value_error_4e89389_1)
# ---------------------------------------------------------------------------
def property_parse_date_wraps_value_error(args: Tuple[int, int, int]) -> PropertyResult:
    """parse_date must raise ParseError (not bare ValueError or TypeError) for
    syntactically valid but logically invalid inputs (e.g. month=13).

    Bug (4e89389): the original code let any datetime-construction
    exception (e.g. ``ValueError("month must be in 1..12")``) propagate
    unchanged. The fix re-raises as ParseError.

    NOTE: ParseError is a ValueError subclass on the modern tree, so the
    check is by concrete type, not isinstance(..., ValueError).
    """
    year, month, day = args
    if not (1 <= year <= 9999):
        return PASS
    if not (1 <= month <= 99):
        return PASS
    if not (1 <= day <= 99):
        return PASS
    # Skip inputs that the stdlib datetime constructor accepts — a regex match
    # followed by a successful datetime build is "valid input", not a witness.
    try:
        datetime.datetime(year, month, day)
        return PASS
    except (ValueError, OverflowError):
        pass
    candidate = f"{year:04d}-{month:02d}-{day:02d}"
    try:
        parsed = iso8601.parse_date(candidate)
    except iso8601.ParseError:
        return PASS
    except Exception as e:
        return fail(
            f"parse_date({candidate!r}) raised {type(e).__name__}({e}); "
            f"expected ParseError"
        )
    return fail(
        f"parse_date({candidate!r}) returned {parsed!r}; "
        f"expected ParseError because month/day is out of range"
    )


# ---------------------------------------------------------------------------
# ParseErrorIsValueError (variant: parse_error_not_value_error_4498905_1)
# ---------------------------------------------------------------------------
def property_parse_error_is_value_error(args: int) -> PropertyResult:
    """ParseError must be a subclass of ValueError, so that callers using
    ``except ValueError`` handle it (matching stdlib parsers like strptime
    and json.loads).

    Bug (4498905): the original ParseError extended Exception, so a
    catch-ValueError caller silently let the parse failure propagate.
    """
    n = args
    candidate = "this-is-not-a-date" + ("!" * (n % 4))
    try:
        iso8601.parse_date(candidate)
    except ValueError:
        return PASS
    except Exception as e:
        return fail(
            f"parse_date({candidate!r}) raised {type(e).__name__}({e}); "
            f"expected a ValueError subclass (ParseError must extend ValueError)"
        )
    return fail(
        f"parse_date({candidate!r}) returned without raising; "
        f"the input is not a valid ISO 8601 date"
    )
