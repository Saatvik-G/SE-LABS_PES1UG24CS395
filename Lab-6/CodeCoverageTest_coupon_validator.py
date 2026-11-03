import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# Starter test cases
def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20


def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True


# Tests for coupon_discount line coverage
def test_cart_total_zero_or_negative():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", -50, True, "mon")


def test_welcome_coupon_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_coupon_saturday_above_500():
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0


def test_weekend_coupon_sunday_below_500():
    assert coupon_discount("WEEKEND20", 400, False, "sun") == 50


def test_weekend_coupon_weekday():
    assert coupon_discount("WEEKEND20", 600, False, "wed") == 0


def test_flat100_coupon_above_300():
    assert coupon_discount("FLAT100", 350, False, "tue") == 100


def test_flat100_coupon_300_or_below():
    assert coupon_discount("FLAT100", 250, False, "tue") == 0


def test_unknown_coupon_code():
    assert coupon_discount("SUMMER50", 500, True, "mon") == 0


# Tests for best_discount line coverage
def test_best_discount_with_cap():
    # Codes gives 100 on cart 200, but cap is 200 * 0.4 = 80
    codes = ["WELCOME10", "FLAT100"]  # WELCOME10 gives 20; FLAT100 gives 0 on 200 (<= 300)
    # Let's test a case where best exceeds cap:
    # cart_total = 400, FLAT100 gives 100, cap is 400 * 0.4 = 160 -> best <= cap
    # cart_total = 200, WEEKEND20 on sat gives 50, cap is 80 -> best <= cap
    # To exceed cap: cart_total = 100, wait, cart <= 300 gives 0 for flat100
    # On weekend, cart = 100, day='sat', WEEKEND20 gives 50. Cap = 100 * 0.4 = 40. 50 > 40! Cap triggered!
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40.0


def test_best_discount_without_exceeding_cap():
    codes = ["WELCOME10", "FLAT100"]
    # cart = 400, new_user = True: WELCOME10 gives 40, FLAT100 gives 100.
    # best = 100. Cap = 400 * 0.4 = 160. 100 < 160. Returns 100.
    assert best_discount(codes, 400, True, "fri") == 100


def test_best_discount_empty_codes():
    assert best_discount([], 500, False, "mon") == 0


# Tests for is_expired line coverage
def test_not_expired():
    # today = 10, start = 5, days_valid = 10: 10 - 5 = 5 <= 10 -> False
    assert is_expired(10, 5, 10) is False


def test_is_expired_past_days_valid():
    # today = 20, start = 5, days_valid = 10: 20 - 5 = 15 > 10 -> True
    assert is_expired(20, 5, 10) is True
