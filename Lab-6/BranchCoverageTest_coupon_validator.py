import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ============================================================================
# 1. Tests for coupon_discount()
# ============================================================================

def test_cart_total_zero_raises_error():
    """Branch: cart_total <= 0 evaluates True (cart_total == 0)."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_cart_total_negative_raises_error():
    """Branch: cart_total <= 0 evaluates True (cart_total < 0)."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", -100, True, "mon")


def test_welcome10_new_user_true():
    """Branch: code == 'WELCOME10' True, is_new_user True -> returns 10%."""
    assert coupon_discount("WELCOME10", 250, True, "mon") == 25.0


def test_welcome10_new_user_false():
    """Branch: code == 'WELCOME10' True, is_new_user False -> returns 0."""
    assert coupon_discount("WELCOME10", 250, False, "mon") == 0


def test_weekend20_saturday_cart_above_500():
    """Branch: code == 'WEEKEND20' True, day in ('sat','sun') True (sat), cart_total >= 500 True."""
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0


def test_weekend20_sunday_cart_exactly_500():
    """Branch boundary: cart_total == 500 evaluates True."""
    assert coupon_discount("WEEKEND20", 500, False, "sun") == 100.0


def test_weekend20_sunday_cart_below_500():
    """Branch: code == 'WEEKEND20' True, day in ('sat','sun') True (sun), cart_total >= 500 False -> returns 50."""
    assert coupon_discount("WEEKEND20", 400, False, "sun") == 50


def test_weekend20_weekday_not_weekend():
    """Branch: code == 'WEEKEND20' True, day in ('sat','sun') False (wed) -> returns 0."""
    assert coupon_discount("WEEKEND20", 600, False, "wed") == 0


def test_flat100_cart_above_300():
    """Branch: code == 'FLAT100' True, cart_total > 300 True (301) -> returns 100."""
    assert coupon_discount("FLAT100", 301, False, "fri") == 100


def test_flat100_cart_exactly_300():
    """Branch boundary: code == 'FLAT100' True, cart_total > 300 False (300) -> returns 0."""
    assert coupon_discount("FLAT100", 300, False, "fri") == 0


def test_flat100_cart_below_300():
    """Branch: code == 'FLAT100' True, cart_total > 300 False (200) -> returns 0."""
    assert coupon_discount("FLAT100", 200, False, "fri") == 0


def test_unrecognized_coupon_code():
    """Branch: code matches none of the valid codes -> falls through to return 0."""
    assert coupon_discount("INVALID_CODE", 500, True, "sat") == 0


# ============================================================================
# 2. Tests for best_discount()
# ============================================================================

def test_best_discount_empty_codes_list():
    """Branch: for loop with empty list (0 iterations) -> returns 0."""
    assert best_discount([], 500, False, "mon") == 0


def test_best_discount_single_coupon_below_cap():
    """Branch: for loop 1 iteration, best <= cap."""
    assert best_discount(["WELCOME10"], 200, True, "mon") == 20.0


def test_best_discount_multiple_coupons_picks_highest_and_checks_value_less_than_best():
    """Branch: evaluates value > best as BOTH True and False during iteration.
    First code (WEEKEND20 on 600 sat) -> value = 120, best becomes 120 (True branch).
    Second code (WELCOME10 on 600 existing user) -> value = 0, which is NOT > 120 (False branch 25->23).
    Cap = 600 * 0.4 = 240. 120 <= 240 (best > cap is False).
    """
    assert best_discount(["WEEKEND20", "WELCOME10"], 600, False, "sat") == 120.0


def test_best_discount_exceeds_cap():
    """Branch: best > cap evaluates True.
    cart_total = 100, WEEKEND20 on sat gives 50.
    Cap = 100 * 0.4 = 40.
    50 > 40 is True -> returns cap (40.0).
    """
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40.0


def test_best_discount_exactly_equal_to_cap():
    """Branch boundary: best == cap evaluates False for best > cap.
    cart_total = 250, cap = 250 * 0.4 = 100.
    FLAT100 on 350 cart: let cart_total = 250, wait FLAT100 needs > 300.
    If cart_total = 500, cap = 200. WEEKEND20 on 500 gives 500 * 0.20 = 100.
    If cart_total = 125, WEEKEND20 gives 50, cap = 125 * 0.4 = 50. best == cap -> returns 50.
    """
    assert best_discount(["WEEKEND20"], 125, False, "sat") == 50.0


# ============================================================================
# 3. Tests for is_expired()
# ============================================================================

def test_is_expired_days_valid_zero():
    """Branch: days_valid <= 0 evaluates True (days_valid == 0) -> returns True."""
    assert is_expired(10, 5, 0) is True


def test_is_expired_days_valid_negative():
    """Branch: days_valid <= 0 evaluates True (days_valid < 0) -> returns True."""
    assert is_expired(10, 5, -3) is True


def test_is_expired_past_validity_period():
    """Branch: days_valid <= 0 False, today - start > days_valid True (15 > 10) -> returns True."""
    assert is_expired(20, 5, 10) is True


def test_is_expired_exactly_on_expiry_day():
    """Branch boundary: today - start == days_valid (10 == 10) evaluates False -> returns False."""
    assert is_expired(15, 5, 10) is False


def test_is_expired_well_within_validity_period():
    """Branch: today - start < days_valid (3 < 10) evaluates False -> returns False."""
    assert is_expired(8, 5, 10) is False
