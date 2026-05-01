"""Hypothesis SearchStrategy builders — one `def strategy_<snake>()` per property.

CrossHair-compatible strategies only: stick to st.integers, st.text, st.lists,
st.tuples, st.booleans, st.from_type, st.builds, st.one_of. Avoid st.data,
st.randoms, and custom @composite that branches on intermediate state.
"""
from __future__ import annotations

from hypothesis import strategies as st


def strategy_is_iso8601_raises_on_internal_error():
    return st.binary(min_size=1, max_size=12)


def strategy_year_must_be_four_digits():
    return st.integers(min_value=1, max_value=999)


def strategy_year_only_parses():
    return st.integers(min_value=1, max_value=9999)


def strategy_z_is_always_utc():
    return st.tuples(
        st.integers(min_value=-14, max_value=14),
        st.integers(min_value=0, max_value=59),
    )


def strategy_negative_timezone_minutes_negated():
    return st.tuples(
        st.integers(min_value=1, max_value=14),
        st.integers(min_value=1, max_value=59),
    )


def strategy_microsecond_preserves_all_digits():
    return st.integers(min_value=0, max_value=999_999)


def strategy_parse_date_wraps_value_error():
    return st.tuples(
        st.integers(min_value=1, max_value=9999),
        st.integers(min_value=1, max_value=99),
        st.integers(min_value=1, max_value=99),
    )


def strategy_parse_error_is_value_error():
    return st.integers(min_value=0, max_value=10_000)
