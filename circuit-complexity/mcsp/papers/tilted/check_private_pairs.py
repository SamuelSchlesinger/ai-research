"""Verify the gate and entropy margins in private-pairs.md with fractions."""

from fractions import Fraction as F


def ln_unit(x):
    """Enclose ln(x) on [1, 2] with 16 terms of the atanh series."""
    y = (x - 1) / (x + 1)
    low = 2 * sum(y**i / i for i in range(1, 32, 2))
    return low, low + 2 * y**33 / (33 * (1 - y**2))


LN2_LOW, LN2_HIGH = ln_unit(F(2))


def log_bounds(x):
    """Scale to [1, 2) before enclosing the base-two logarithm."""
    power = x.numerator.bit_length() - x.denominator.bit_length()
    unit = x / F(2)**power
    if unit < 1:
        unit *= 2
        power -= 1
    assert 1 <= unit < 2
    low, high = ln_unit(unit)
    return power + low / LN2_HIGH, power + high / LN2_LOW


def divergence(p, reference):
    on_low, on_high = log_bounds(p / reference)
    off_low, off_high = log_bounds((1 - p) / (1 - reference))
    return (p * on_low + (1 - p) * off_low,
            p * on_high + (1 - p) * off_high)


def check(a, b, p, q, pivot_limit, kappa_bound, gate_floor):
    d_low, d_high = divergence(p, F(1, 2))
    _, private_high = divergence(q, F(3, 4))
    kappa_high = d_high + max(0, private_high - 2 * d_low) * a / q
    assert kappa_high < kappa_bound < b

    entropy_high = 1 - divergence(pivot_limit, F(1, 2))[0]
    alpha_low, alpha_high = log_bounds(F(3, 2))
    ordinary = 3 + p
    private = (2 + 2 * p) / q
    delta = private - ordinary
    gamma = 1 - p
    assert 0 < delta < ordinary * alpha_low
    assert entropy_high - pivot_limit < alpha_low * a
    slope_low = log_bounds((1 - pivot_limit) / pivot_limit)[0] - 1
    assert delta * slope_low > alpha_high * gamma
    assert 2 + p - private * a + gamma * pivot_limit > gate_floor
    assert kappa_high + entropy_high < F(".0104")


if __name__ == "__main__":
    rows = [
        (".00635", ".00635", ".545836", "6/7", ".000305", ".0063495", "2.52307"),
        (".00565", ".00565", ".543317", ".8526", ".000268", ".0056497", "2.52298"),
        (".007", ".00565", ".543104", ".8523", ".000342", ".0056497", "2.51791"),
    ]
    for row in rows:
        check(*map(F, row))
    print("Verified all three gate bounds and the common confidence exponent.")
