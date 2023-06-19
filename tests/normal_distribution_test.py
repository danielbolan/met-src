from math import *
from met_src.normal_distribution import NormalDistribution


def test_pdf():
    n = NormalDistribution(0, 1)
    assert isclose(n.pdf(0), tau**-0.5)
    assert isclose(n.pdf(inf), 0)
    assert isclose(n.pdf(-inf), 0)

    n = NormalDistribution(1, 1)
    assert isclose(n.pdf(1), tau**-0.5)
    assert isclose(n.pdf(inf), 0)
    assert isclose(n.pdf(-inf), 0)

    n = NormalDistribution(0, 2)
    assert isclose(n.pdf(0), (8 * pi) ** -0.5)
    assert isclose(n.pdf(inf), 0)
    assert isclose(n.pdf(-inf), 0)


def test_cdf():
    def run_cdf_test(n):
        assert isclose(n.cdf(n.mu), 0.5)
        assert isclose(n.cdf(inf), 1)
        assert isclose(n.cdf(-inf), 0)
        val = n.mu + n.sigma
        assert isclose(n.cdf(val) * 2 - 1, 0.6827, abs_tol=1e-4)
        val = n.mu + n.sigma * 2
        assert isclose(n.cdf(val) * 2 - 1, 0.9545, abs_tol=1e-4)
        val = n.mu + n.sigma * 3
        assert isclose(n.cdf(val) * 2 - 1, 0.9973, abs_tol=1e-4)
        val = n.mu - n.sigma
        assert isclose(n.cdf(val) * 2, 1 - 0.6827, abs_tol=1e-4)

    dists = [
        NormalDistribution(0, 1),
        NormalDistribution(0, 10),
        NormalDistribution(5, 2),
        NormalDistribution(100, 100),
    ]

    for dist in dists:
        run_cdf_test(dist)


def test_intersections():
    n1 = NormalDistribution(-1, 1)
    n2 = NormalDistribution(1, 1)
    i1, i2 = n1.intersections(n2)
    assert isclose(i1, 0)
    assert i2 is None
    assert n1.intersections(n2) == n2.intersections(n1)

    n1 = NormalDistribution(0, 5)
    n2 = NormalDistribution(6, 5)
    i1, i2 = n1.intersections(n2)
    assert isclose(i1, 3)
    assert i2 is None
    assert n1.intersections(n2) == n2.intersections(n1)

    n1 = NormalDistribution(0, 2)
    n2 = NormalDistribution(1, 1)
    i1, i2 = n1.intersections(n2)
    assert isclose(i1, -0.1808, abs_tol=1e-4)
    assert isclose(i2, 2.8475, abs_tol=1e-4)
    assert n1.intersections(n2) == n2.intersections(n1)


def test_overlap_coefficient():
    n1 = NormalDistribution(0, 1)
    n2 = NormalDistribution(0, 1)
    c = n1.overlap_coefficient(n2)
    assert isclose(c, 1)
    assert isclose(n2.overlap_coefficient(n1), c)

    n1 = NormalDistribution(100, 100)
    n2 = NormalDistribution(100, 100)
    c = n1.overlap_coefficient(n2)
    assert isclose(c, 1)
    assert isclose(n2.overlap_coefficient(n1), c)

    n1 = NormalDistribution(1e100, 1)
    n2 = NormalDistribution(-1e100, 1)
    c = n1.overlap_coefficient(n2)
    assert isclose(c, 0)
    assert isclose(n2.overlap_coefficient(n1), c)

    n1 = NormalDistribution(0, 2)
    n2 = NormalDistribution(1, 2)
    c = n1.overlap_coefficient(n2)
    assert isclose(c, 0.8026, abs_tol=1e-4)
    assert isclose(n2.overlap_coefficient(n1), c)
