# iso8601 — ETNA Tasks

Total tasks: 32

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `is_iso8601_returns_false_on_exception_fde429d_1` | proptest | `IsIso8601RaisesOnInternalError` | `witness_is_iso8601_raises_on_internal_error_case_bytes` |
| 002 | `is_iso8601_returns_false_on_exception_fde429d_1` | quickcheck | `IsIso8601RaisesOnInternalError` | `witness_is_iso8601_raises_on_internal_error_case_bytes` |
| 003 | `is_iso8601_returns_false_on_exception_fde429d_1` | crabcheck | `IsIso8601RaisesOnInternalError` | `witness_is_iso8601_raises_on_internal_error_case_bytes` |
| 004 | `is_iso8601_returns_false_on_exception_fde429d_1` | hegel | `IsIso8601RaisesOnInternalError` | `witness_is_iso8601_raises_on_internal_error_case_bytes` |
| 005 | `microsecond_float_rounding_81ff287_1` | proptest | `MicrosecondPreservesAllDigits` | `witness_microsecond_preserves_all_digits_case_502099` |
| 006 | `microsecond_float_rounding_81ff287_1` | quickcheck | `MicrosecondPreservesAllDigits` | `witness_microsecond_preserves_all_digits_case_502099` |
| 007 | `microsecond_float_rounding_81ff287_1` | crabcheck | `MicrosecondPreservesAllDigits` | `witness_microsecond_preserves_all_digits_case_502099` |
| 008 | `microsecond_float_rounding_81ff287_1` | hegel | `MicrosecondPreservesAllDigits` | `witness_microsecond_preserves_all_digits_case_502099` |
| 009 | `negative_tz_minutes_dropped_d724fec_1` | proptest | `NegativeTimezoneMinutesNegated` | `witness_negative_timezone_minutes_negated_case_minus_one_thirty` |
| 010 | `negative_tz_minutes_dropped_d724fec_1` | quickcheck | `NegativeTimezoneMinutesNegated` | `witness_negative_timezone_minutes_negated_case_minus_one_thirty` |
| 011 | `negative_tz_minutes_dropped_d724fec_1` | crabcheck | `NegativeTimezoneMinutesNegated` | `witness_negative_timezone_minutes_negated_case_minus_one_thirty` |
| 012 | `negative_tz_minutes_dropped_d724fec_1` | hegel | `NegativeTimezoneMinutesNegated` | `witness_negative_timezone_minutes_negated_case_minus_one_thirty` |
| 013 | `parse_date_unwrapped_value_error_4e89389_1` | proptest | `ParseDateWrapsValueError` | `witness_parse_date_wraps_value_error_case_month_thirteen` |
| 014 | `parse_date_unwrapped_value_error_4e89389_1` | quickcheck | `ParseDateWrapsValueError` | `witness_parse_date_wraps_value_error_case_month_thirteen` |
| 015 | `parse_date_unwrapped_value_error_4e89389_1` | crabcheck | `ParseDateWrapsValueError` | `witness_parse_date_wraps_value_error_case_month_thirteen` |
| 016 | `parse_date_unwrapped_value_error_4e89389_1` | hegel | `ParseDateWrapsValueError` | `witness_parse_date_wraps_value_error_case_month_thirteen` |
| 017 | `parse_error_not_value_error_4498905_1` | proptest | `ParseErrorIsValueError` | `witness_parse_error_is_value_error_case_garbage` |
| 018 | `parse_error_not_value_error_4498905_1` | quickcheck | `ParseErrorIsValueError` | `witness_parse_error_is_value_error_case_garbage` |
| 019 | `parse_error_not_value_error_4498905_1` | crabcheck | `ParseErrorIsValueError` | `witness_parse_error_is_value_error_case_garbage` |
| 020 | `parse_error_not_value_error_4498905_1` | hegel | `ParseErrorIsValueError` | `witness_parse_error_is_value_error_case_garbage` |
| 021 | `regex_requires_full_date_6d33d31_1` | proptest | `YearOnlyParses` | `witness_year_only_parses_case_2007` |
| 022 | `regex_requires_full_date_6d33d31_1` | quickcheck | `YearOnlyParses` | `witness_year_only_parses_case_2007` |
| 023 | `regex_requires_full_date_6d33d31_1` | crabcheck | `YearOnlyParses` | `witness_year_only_parses_case_2007` |
| 024 | `regex_requires_full_date_6d33d31_1` | hegel | `YearOnlyParses` | `witness_year_only_parses_case_2007` |
| 025 | `year_unconstrained_dc7f577_1` | proptest | `YearMustBeFourDigits` | `witness_year_must_be_four_digits_case_three_digit` |
| 026 | `year_unconstrained_dc7f577_1` | quickcheck | `YearMustBeFourDigits` | `witness_year_must_be_four_digits_case_three_digit` |
| 027 | `year_unconstrained_dc7f577_1` | crabcheck | `YearMustBeFourDigits` | `witness_year_must_be_four_digits_case_three_digit` |
| 028 | `year_unconstrained_dc7f577_1` | hegel | `YearMustBeFourDigits` | `witness_year_must_be_four_digits_case_three_digit` |
| 029 | `z_uses_default_tz_704a58e_1` | proptest | `ZIsAlwaysUtc` | `witness_z_is_always_utc_case_plus_five_thirty` |
| 030 | `z_uses_default_tz_704a58e_1` | quickcheck | `ZIsAlwaysUtc` | `witness_z_is_always_utc_case_plus_five_thirty` |
| 031 | `z_uses_default_tz_704a58e_1` | crabcheck | `ZIsAlwaysUtc` | `witness_z_is_always_utc_case_plus_five_thirty` |
| 032 | `z_uses_default_tz_704a58e_1` | hegel | `ZIsAlwaysUtc` | `witness_z_is_always_utc_case_plus_five_thirty` |

## Witness Catalog

- `witness_is_iso8601_raises_on_internal_error_case_bytes` — is_iso8601(b'2007-01-25') must raise
- `witness_microsecond_preserves_all_digits_case_502099` — fraction .502099 must produce microsecond=502099
- `witness_negative_timezone_minutes_negated_case_minus_one_thirty` — -01:30 must yield exactly -90 minutes
- `witness_parse_date_wraps_value_error_case_month_thirteen` — month=13 must raise ParseError, not bare ValueError
- `witness_parse_error_is_value_error_case_garbage` — ParseError must be caught by `except ValueError`
- `witness_year_only_parses_case_2007` — parse_date('2007') must yield datetime(2007, 1, 1, ...)
- `witness_year_must_be_four_digits_case_three_digit` — parse_date('999') must raise ParseError
- `witness_z_is_always_utc_case_plus_five_thirty` — parse_date('...Z', default_timezone=FixedOffset(5,30,...)) utcoffset must be 0
