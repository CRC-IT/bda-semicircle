"""
Semicircles for approximation of drainage radius on a dip.

Contact James Scarborough for CRC BDA

https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely
pip install ...\GitHub\bda-semicircle\Shapely-1.6.4.post1-cp36-cp36m-win_amd64.whl
"""
import shapely.geometry
import math


def semicircle(origin, radius, rotation):
    """Return semicircle polygon facing the Up Dip, as degrees counter clockwise from east.

    The tactic is make a circle, make a square, rotate and move the square, use that to clip off half the circle.

    >>> circle = shapely.geometry.Point(0.0, 0.0).buffer(1.0)
    >>> circle.area
    3.1365484905459384
    >>> list(circle.exterior.coords) #doctest:+ELLIPSIS
    [(1.0, 0.0), (0.9951847266721969, -0.0980171403295605),... (1.0, 8.238535137130597e-15), (1.0, 0.0)]
    >>> len(list(circle.exterior.coords))
    66

    >>> semi = semicircle((0, 0), 1.0, 10)
    >>> semi  #doctest:+ELLIPSIS
    <shapely.geometry.polygon.Polygon object at 0x...>
    >>> len(list(semi.exterior.coords))
    36
    """
    circle = shapely.geometry.Point(origin).buffer(radius)
    square = shapely.geometry.box(*circle.bounds)
    clip = shapely.affinity.rotate(square, rotation)
    radians = math.radians(rotation)
    offsets_xy = (-math.cos(radians), -math.sin(radians))
    clip = shapely.affinity.translate(clip, *offsets_xy)
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

    origin, radius, rotation = (0, 0), 1.0, 10
    semi = semicircle(origin, radius, rotation)
    plot_line(ax, semi.exterior, color=BLUE, linewidth=10)

    circle = shapely.geometry.Point(origin).buffer(radius)
    plot_line(ax, circle.exterior)
    plot_line(ax, shapely.geometry.box(*circle.bounds).exterior)
    pyplot.show()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    _graphic_test()
