from __future__ import annotations
from math import *


class NormalDistribution:
    def __init__(self, mu: float, sigma: float):
        self.mu = mu
        self.sigma = sigma

    def pdf(self, z: float) -> float:
        """
        The probability density function. The classic bell curve shape of a normal distribution.
        """
        k = 1 / (self.sigma * sqrt(2 * pi))
        x = -0.5 * ((z - self.mu) / self.sigma) ** 2
        return k * exp(x)

    def cdf(self, z: float) -> float:
        """
        The cumulative density function. Integrates the PDF from -inf to z.
        Tells you the probability of a sample from a distribution returning a value less than z.
        """
        return erf((z - self.mu) / (self.sigma * sqrt(2))) / 2 + 0.5

    def log_coefficients(self):
        """
        The log of a normal distribution gives a quadratic equation ax^2 + bx + c.
        Knowing the coefficients a, b, and c makes it a lot easier to find where
        the PDFs of two normal distributions intersect. We use this as a helper to
        find the overlap coefficient of two normal distributions.
        """
        a = -1 / (2 * self.sigma**2)
        b = self.mu / self.sigma**2
        c = -(self.mu**2) / (2 * self.sigma**2)
        c -= log(self.sigma * sqrt(tau))
        return a, b, c

    def intersections(self, other: NormalDistribution) -> (float, float | None):
        """
        Calculates the intersections of the normal distribution PDFs.
        Does this by taking the natural log of each PDF and then uses the quadratic formula.
        """
        n1, n2 = self, other
        if n1.mu < n2.mu:
            n1, n2 = n2, n1

        a1, b1, c1 = n1.log_coefficients()
        a2, b2, c2 = n2.log_coefficients()
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2

        if isclose(a, 0):
            # Same variance means only one intersection
            return ((n1.mu + n2.mu) / 2, None)

        d_sqr = b**2 - (4 * a * c)
        if d_sqr < 0:
            raise ValueError(
                "No intersections detected, which shouldn't be possible. "
                "Did you accidentally set the variance of one of the distributions to zero?"
            )
        d = sqrt(d_sqr)
        i1 = (-b + d) / (2 * a)
        i2 = (-b - d) / (2 * a)
        return (i1, i2)

    def overlap_coefficient(self, other):
        """
        Calculates the overlap coefficient of two distributions.
        For two distributions A and B, this is defined by the area under min(PDF(A), PDF(B)).
        """
        n1, n2 = self, other
        if n1.mu < n2.mu:
            n1, n2 = n2, n1

        i1, i2 = n1.intersections(n2)
        if i2 is None:
            return n1.cdf(i1) * 2

        c = n1.cdf(i1)
        c += 1 - n2.cdf(i1)
        c -= 1 - n2.cdf(i2)
        c += 1 - n1.cdf(i2)
        return c

    def __eq__(self, other):
        return self.mu == other.mu and self.sigma == other.sigma


def main():
    """
    Sanity check for NormalDistribution.intersections().
    """
    from matplotlib import pyplot as plt
    import numpy as np

    n1 = NormalDistribution(2, 1)
    n2 = NormalDistribution(1, 2)

    i = n1.intersections(n2)
    if i[1] is None:
        i = [i[0]]
    xvals = np.arange(min(i) - 1, max(i) + 1, 0.01)
    l1 = [n1.pdf(z) for z in xvals]
    l2 = [n2.pdf(z) for z in xvals]
    ix = i
    iy = [n1.pdf(i) for i in ix]

    plt.plot(xvals, l1, label="l1")
    plt.plot(xvals, l2, label="l2")
    plt.scatter(ix, iy, marker="+", color="black", zorder=2)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
