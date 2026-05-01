# iso8601 — Injected Bugs

Pure-Python ISO 8601 date/time parser (pyiso8601). Bug fixes mined from upstream history; modern HEAD is the base, each patch reverse-applies a fix to install the original bug.

Total mutations: 8

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `is_iso8601_returns_false_on_exception_fde429d_1` | `is_iso8601_silent_on_error` | `iso8601/iso8601.py:161` | `patch` | `fde429d40d82057d2507c657b9a7bbd30e369aa8` |
| 2 | `microsecond_float_rounding_81ff287_1` | `microsecond_float_rounding` | `iso8601/iso8601.py:144` | `patch` | `81ff287384424cda10f087a25e2e104d2c02532a` |
| 3 | `negative_tz_minutes_dropped_d724fec_1` | `negative_tz_minutes_dropped` | `iso8601/iso8601.py:98` | `patch` | `d724fec9ab004cf4e7fa8159764c12990a1050db` |
| 4 | `parse_date_unwrapped_value_error_4e89389_1` | `parse_date_unwrapped_value_error` | `iso8601/iso8601.py:149` | `patch` | `4e893893e92f8383deffe8093877f13127fed4f3` |
| 5 | `parse_error_not_value_error_4498905_1` | `parse_error_not_value_error` | `iso8601/iso8601.py:64` | `patch` | `4498905f0d6e1e3895ae24ea9b896a4a3a11b3a1` |
| 6 | `regex_requires_full_date_6d33d31_1` | `regex_requires_full_date` | `iso8601/iso8601.py:57` | `patch` | `6d33d31529dcc0217caf2febc3f2806cd1ed87e4` |
| 7 | `year_unconstrained_dc7f577_1` | `year_unconstrained` | `iso8601/iso8601.py:22` | `patch` | `dc7f577cff153b9890337645a4e5ca7ba35bd785` |
| 8 | `z_uses_default_tz_704a58e_1` | `z_uses_default_tz` | `iso8601/iso8601.py:86` | `patch` | `704a58e77b61d3496b36a1d14836f75796d194eb` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `is_iso8601_returns_false_on_exception_fde429d_1` | `IsIso8601RaisesOnInternalError` | `witness_is_iso8601_raises_on_internal_error_case_bytes` |
| `microsecond_float_rounding_81ff287_1` | `MicrosecondPreservesAllDigits` | `witness_microsecond_preserves_all_digits_case_502099` |
| `negative_tz_minutes_dropped_d724fec_1` | `NegativeTimezoneMinutesNegated` | `witness_negative_timezone_minutes_negated_case_minus_one_thirty` |
| `parse_date_unwrapped_value_error_4e89389_1` | `ParseDateWrapsValueError` | `witness_parse_date_wraps_value_error_case_month_thirteen` |
| `parse_error_not_value_error_4498905_1` | `ParseErrorIsValueError` | `witness_parse_error_is_value_error_case_garbage` |
| `regex_requires_full_date_6d33d31_1` | `YearOnlyParses` | `witness_year_only_parses_case_2007` |
| `year_unconstrained_dc7f577_1` | `YearMustBeFourDigits` | `witness_year_must_be_four_digits_case_three_digit` |
| `z_uses_default_tz_704a58e_1` | `ZIsAlwaysUtc` | `witness_z_is_always_utc_case_plus_five_thirty` |

## Framework Coverage

| Property | proptest | quickcheck | crabcheck | hegel |
|----------|---------:|-----------:|----------:|------:|
| `IsIso8601RaisesOnInternalError` | ✓ | ✓ | ✓ | ✓ |
| `MicrosecondPreservesAllDigits` | ✓ | ✓ | ✓ | ✓ |
| `NegativeTimezoneMinutesNegated` | ✓ | ✓ | ✓ | ✓ |
| `ParseDateWrapsValueError` | ✓ | ✓ | ✓ | ✓ |
| `ParseErrorIsValueError` | ✓ | ✓ | ✓ | ✓ |
| `YearOnlyParses` | ✓ | ✓ | ✓ | ✓ |
| `YearMustBeFourDigits` | ✓ | ✓ | ✓ | ✓ |
| `ZIsAlwaysUtc` | ✓ | ✓ | ✓ | ✓ |

## Bug Details

### 1. is_iso8601_silent_on_error

- **Variant**: `is_iso8601_returns_false_on_exception_fde429d_1`
- **Location**: `iso8601/iso8601.py:161` (inside `is_iso8601`)
- **Property**: `IsIso8601RaisesOnInternalError`
- **Witness(es)**:
  - `witness_is_iso8601_raises_on_internal_error_case_bytes` — is_iso8601(b'2007-01-25') must raise
- **Source**: internal — raise ParseError if we get an exception on is_iso8601()
  > is_iso8601() used to swallow any exception raised inside re.match (e.g. when called with a bytes-like object) and silently return False, hiding caller misuse. The fix re-raises as ParseError.
- **Fix commit**: `fde429d40d82057d2507c657b9a7bbd30e369aa8` — raise ParseError if we get an exception on is_iso8601()
- **Invariant violated**: is_iso8601(x) raises ParseError when the underlying regex match raises (e.g. bytes input); it must not silently return False.
- **How the mutation triggers**: Reverse-applying the patch swaps the ``except Exception as e: raise ParseError(e)`` body for ``except Exception: return False``. Calling ``is_iso8601(b'2007-01-25')`` then returns False instead of raising.

### 2. microsecond_float_rounding

- **Variant**: `microsecond_float_rounding_81ff287_1`
- **Location**: `iso8601/iso8601.py:144` (inside `parse_date`)
- **Property**: `MicrosecondPreservesAllDigits`
- **Witness(es)**:
  - `witness_microsecond_preserves_all_digits_case_502099` — fraction .502099 must produce microsecond=502099
- **Source**: internal — Fix microsecond rounding issues
  > The original microsecond computation used ``int(float('0.<frac>') * 1e6)``, whose binary float representation off-by-ones for many fractions (e.g. ``0.502099`` becomes 502098). The fix uses ``Decimal`` arithmetic to preserve all six digits.
- **Fix commit**: `81ff287384424cda10f087a25e2e104d2c02532a` — Fix microsecond rounding issues
- **Invariant violated**: For any 6-digit fraction F, parse_date(f'2007-01-25T12:00:00.{F}Z').microsecond == int(F).
- **How the mutation triggers**: Reverse-applying the patch swaps the Decimal multiplication for ``int(float(...) * 1e6)``. ``parse_date('2007-01-25T12:00:00.502099Z').microsecond`` then equals 502098.

### 3. negative_tz_minutes_dropped

- **Variant**: `negative_tz_minutes_dropped_d724fec_1`
- **Location**: `iso8601/iso8601.py:98` (inside `parse_timezone`)
- **Property**: `NegativeTimezoneMinutesNegated`
- **Witness(es)**:
  - `witness_negative_timezone_minutes_negated_case_minus_one_thirty` — -01:30 must yield exactly -90 minutes
- **Source**: internal — Handle negative timezone offsets correctly
  > For negative timezone offsets the parser used to negate the hour but leave the minute positive, so an offset of ``-01:30`` resolved to ``-60 + 30 = -30`` minutes instead of ``-90``. The fix negates both.
- **Fix commit**: `d724fec9ab004cf4e7fa8159764c12990a1050db` — Handle negative timezone offsets correctly
- **Invariant violated**: parse_date('...-HH:MM').utcoffset() == -timedelta(hours=HH, minutes=MM) for HH>=1 and MM>=1.
- **How the mutation triggers**: Reverse-applying the patch deletes the ``minutes = -minutes`` line in parse_timezone. ``parse_date('2007-01-25T12:00:00-01:30').utcoffset()`` then equals ``-timedelta(hours=1, minutes=-30)`` (i.e. -30 minutes).

### 4. parse_date_unwrapped_value_error

- **Variant**: `parse_date_unwrapped_value_error_4e89389_1`
- **Location**: `iso8601/iso8601.py:149` (inside `parse_date`)
- **Property**: `ParseDateWrapsValueError`
- **Witness(es)**:
  - `witness_parse_date_wraps_value_error_case_month_thirteen` — month=13 must raise ParseError, not bare ValueError
- **Source**: internal — Correctly raise ParseError for more invalid inputs
  > When the regex matched but datetime construction itself raised (e.g. month=13 -> ValueError('month must be in 1..12')), the bare ValueError used to leak out of parse_date. The fix wraps it as ParseError so callers can use a single exception type.
- **Fix commit**: `4e893893e92f8383deffe8093877f13127fed4f3` — Correctly raise ParseError for more invalid inputs
- **Invariant violated**: parse_date(s) raises only ParseError (or returns) for any string s — never bare ValueError or TypeError from the underlying datetime constructor.
- **How the mutation triggers**: Reverse-applying the patch flips the bottom ``except Exception as e: raise ParseError(e)`` body to ``raise e`` (re-raises the original). ``parse_date('2007-13-25')`` then raises ValueError, not ParseError.

### 5. parse_error_not_value_error

- **Variant**: `parse_error_not_value_error_4498905_1`
- **Location**: `iso8601/iso8601.py:64` (inside `ParseError`)
- **Property**: `ParseErrorIsValueError`
- **Witness(es)**:
  - `witness_parse_error_is_value_error_case_garbage` — ParseError must be caught by `except ValueError`
- **Source**: internal — Derive `ParseError` from `ValueError`
  > ParseError used to extend ``Exception`` directly, so callers using the stdlib-style ``except ValueError`` for ``strptime``/``json.loads`` did not catch ISO 8601 parse failures. The fix re-bases ParseError on ValueError to bring it in line with stdlib parsers.
- **Fix commit**: `4498905f0d6e1e3895ae24ea9b896a4a3a11b3a1` — Derive `ParseError` from `ValueError`
- **Invariant violated**: iso8601.ParseError is a subclass of ValueError, so ``except ValueError`` catches every parse_date failure.
- **How the mutation triggers**: Reverse-applying the patch changes ``class ParseError(ValueError)`` to ``class ParseError(Exception)``. A caller doing ``try: parse_date('garbage') except ValueError`` then sees the ParseError propagate uncaught.

### 6. regex_requires_full_date

- **Variant**: `regex_requires_full_date_6d33d31_1`
- **Location**: `iso8601/iso8601.py:57` (inside `ISO8601_REGEX`)
- **Property**: `YearOnlyParses`
- **Witness(es)**:
  - `witness_year_only_parses_case_2007` — parse_date('2007') must yield datetime(2007, 1, 1, ...)
- **Source**: internal — Fix parsing of YYYY-MM and add YYYY
  > The regex used to require both month and day. Plain ``YYYY`` (and ``YYYY-MM``) failed to parse with ParseError. The fix made the month/day group optional via ``){0,1}  # YYYY only`` so a bare year string parses as January 1 of that year.
- **Fix commit**: `6d33d31529dcc0217caf2febc3f2806cd1ed87e4` — Fix parsing of YYYY-MM and add YYYY
- **Invariant violated**: parse_date('YYYY') returns datetime(YYYY, 1, 1, tzinfo=UTC) for any 4-digit year; it must not raise ParseError.
- **How the mutation triggers**: Reverse-applying the patch removes the ``{0,1}`` quantifier from the outer ``# YYYY only`` group, making the month/day branch mandatory. ``parse_date('2007')`` then raises ParseError.

### 7. year_unconstrained

- **Variant**: `year_unconstrained_dc7f577_1`
- **Location**: `iso8601/iso8601.py:22` (inside `ISO8601_REGEX`)
- **Property**: `YearMustBeFourDigits`
- **Witness(es)**:
  - `witness_year_must_be_four_digits_case_three_digit` — parse_date('999') must raise ParseError
- **Source**: internal — Raise error when parsing year with wrong number for years
  > The ISO8601_REGEX year group used to be unconstrained (``[0-9]+``), so a 1-3 digit string parsed as a one-, two- or three-digit year and produced a valid datetime instead of raising ParseError. ISO 8601 requires four digits for the year.
- **Fix commit**: `dc7f577cff153b9890337645a4e5ca7ba35bd785` — Raise error when parsing year with wrong number for years
- **Invariant violated**: parse_date(s) raises ParseError for any string s whose year portion is not exactly four digits.
- **How the mutation triggers**: Reverse-applying the patch relaxes ``(?P<year>[0-9]{4})`` to ``(?P<year>[0-9]+)``. ``parse_date('999')`` then returns ``datetime(999, 1, 1)`` instead of raising.

### 8. z_uses_default_tz

- **Variant**: `z_uses_default_tz_704a58e_1`
- **Location**: `iso8601/iso8601.py:86` (inside `parse_timezone`)
- **Property**: `ZIsAlwaysUtc`
- **Witness(es)**:
  - `witness_z_is_always_utc_case_plus_five_thirty` — parse_date('...Z', default_timezone=FixedOffset(5,30,...)) utcoffset must be 0
- **Source**: internal — Z always specifies UTC now
  > When the date string ended in ``Z`` the parser used to return ``default_timezone`` instead of UTC, so a non-UTC ``default_timezone`` argument silently overrode the explicit ``Z`` marker. The fix returns UTC unconditionally for ``Z``.
- **Fix commit**: `704a58e77b61d3496b36a1d14836f75796d194eb` — Z always specifies UTC now
- **Invariant violated**: parse_date(s, default_timezone=tz).utcoffset() == timedelta(0) whenever s ends in 'Z', for any tz.
- **How the mutation triggers**: Reverse-applying the patch flips ``return UTC`` back to ``return default_timezone`` inside the ``if tz == 'Z':`` branch of parse_timezone. Then a Z-suffixed date with a non-UTC default_timezone is parsed in that timezone.
