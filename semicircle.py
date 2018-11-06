"""
Semicircles for approximation of drainage radius on a dip.

Contact is James Scarborough for California Resources Corp - Big Data Analytics

https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
pip install ...\GitHub\bda-semicircle\Shapely-1.6.4.post1-cp36-cp36m-win_amd64.whl
"""
import shapely.geometry
import math
import numpy as np


def semicircle(x, y, radius, rotation):
    """Return semicircle polygon facing the Up Dip, as degrees counter clockwise from east.

    The tactic is make a circle, make a square, rotate and move the square, use that to clip off half the circle.

    >>> circle = shapely.geometry.Point(0.0, 0.0).buffer(1.0)
    >>> circle.area
    3.1365484905459384
    >>> list(circle.exterior.coords) #doctest:+ELLIPSIS
    [(1.0, 0.0), (0.9951847266721969, -0.0980171403295605),... (1.0, 8.238535137130597e-15), (1.0, 0.0)]
    >>> len(list(circle.exterior.coords))
    66

    >>> semi = semicircle(0, 0, 1.0, 10)
    >>> semi  #doctest:+ELLIPSIS
    <shapely.geometry.polygon.Polygon object at 0x...>
    >>> len(list(semi.exterior.coords))
    36
    >>> semi.area / circle.area
    0.49999999999999994

    >>> real = semicircle(6253790.414, 2353831.202, 12, 45)
    >>> real.area
    225.83149130302806
    >>> math.pi * 12**2 / 2  # half of pi*r^2
    226.1946710584651
    """
    if any(np.isnan([x, y, radius, rotation])) or not radius:
        "User file may have blanks (NaN) or zero radius. 'None' is best for Shapefile export"
        return None
    circle = shapely.geometry.Point(x, y).buffer(radius)
    square = shapely.geometry.box(*circle.bounds)
    clip = shapely.affinity.rotate(square, rotation)
    radians = math.radians(rotation)
    clip = shapely.affinity.translate(clip, xoff=-math.cos(radians) * radius,
                                            yoff=-math.sin(radians) * radius)
    semi = circle.difference(clip)  # Circle - Square = Semicircle
    return semi


def _graphic_test():
    """Plot out the circle, square, and resulting semicircle."""
    from matplotlib import pyplot
    BLUE, GRAY = '#6699cc', '#999999'
    fig = pyplot.figure(1, figsize=(10, 5), dpi=180)
    ax = fig.add_subplot(121)

    def plot_line(ax, ob, color=GRAY, linewidth=3):
        x, y = ob.xy
        ax.plot(x, y, color=color, linewidth=linewidth, solid_capstyle='round', zorder=1)

    x, y, radius, rotation = 0, 0, 1.0, 10
    semi = semicircle(x, y, radius, rotation)
    plot_line(ax, semi.exterior, color=BLUE, linewidth=10)

    circle = shapely.geometry.Point(x, y).buffer(radius)
    plot_line(ax, circle.exterior)
    plot_line(ax, shapely.geometry.box(*circle.bounds).exterior)
    pyplot.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    _graphic_test()
