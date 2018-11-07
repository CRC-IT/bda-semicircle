"""
Create semicircles on demand with a file-based API.

Contact is James Scarborough for California Resources Corp - Big Data Analytics

https://geoffboeing.com/2014/09/using-geopandas-windows/
https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely

pip install ...\GitHub\bda-semicircle\Shapely-1.6.4.post1-cp36-cp36m-win_amd64.whl
    GDAL-2.3.2-cp36-cp36m-win_amd64.whl
    pyproj-1.9.5.1-cp36-cp36m-win_amd64
    Fiona-1.7.13-cp36-cp36m-win_amd64.whl
    geopandas-0.4.0-py2.py3-none-any.whl
    descartes-1.1.0-py2.py3-none-any.whl
"""

import pandas as pd
import geopandas as gpd
from semicircle import semicircle


def do_file(csvfile, suffix='_semicircles.shp', cols=('x', 'y', 'radius', 'rotation'), to_file=True):
    """Import csv file of xy's and parameters then produce a semicircle shapefile.

    >>> print(open('example.csv').read())
    x,y,radius,rotation
    0,0,1.0,10
    <BLANKLINE>
    >>> gdf = do_file('example.csv')
    >>> gdf.iloc[0]
    x                                                           0
    y                                                           0
    radius                                                      1
    rotation                                                   10
    geometry    POLYGON ((1 0, 0.9951847266721969 -0.098017140...
    Name: 0, dtype: object
    >>> gpd.read_file('example.csv_semicircles.shp').iloc[0]
    x                                                           0
    y                                                           0
    radius                                                      1
    rotation                                                   10
    geometry    POLYGON ((1 0, 0.9951847266721969 -0.098017140...
    Name: 0, dtype: object
    >>> import os; from glob import glob
    >>> for f in glob('example.csv_semicircles.*'): os.remove(f)

    >>> print(open('example-real.csv').read())
    x,y,UWI,Well Name,Zone ,radius,rotation
    6254513.29,2353569.785,040000,,Zone,,
    6253790.414,2353831.202,040000,SEC,Zone A1,12,45
    6254341.15,2353978.79,040000,SEC,,0,45
    <BLANKLINE>
    >>> real = do_file('example-real.csv', to_file=False)
    >>> [poly is None or poly.area for poly in real['geometry']]
    [True, 225.83149130302806, True]
    """
    gdf = gpd.GeoDataFrame(pd.read_csv(csvfile, thousands=','))  # User's Excel formatted with thousands separator
    semicircles = [semicircle(*[row[col] for col in cols]) for i, row in gdf.iterrows()]
    gdf['geometry'] = semicircles
    if to_file: gdf.to_file(csvfile+suffix)
    return gdf


def _graphic_test():
    """Map out the semicircles we made."""
    import matplotlib.pyplot as plt
    gdf = do_file('example.csv', to_file=False)
    gdf.plot()
    plt.show()


import os.path as op
from glob import glob
from datetime import datetime
import time


def watch(folder='//olgwfap1/Transfer/semicircles/', filetype='*.csv',
          suffix='_semicircles.shp', error='_error.txt', sleep=10, _debug=False):
    r"""Watch a folder for new files to process.

    Runs from the command line like:
    C:\Users\scarborj\Documents\GitHub\bda-semicircle>\Users\scarborj\Documents\venv\bda-semicircle\
    Scripts\python.exe deploy.py \\olgwfap1\Transfer\semicircles

    >>> folder = '//olgwfap1/Transfer/semicircles/'
    >>> watch(folder=folder, _debug=True)  #doctest:+ELLIPSIS
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles/
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles\example-of-error.csv
    2018-...-... ...:...:... error
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles\example.csv
    2018-...-... ...:...:... done
    >>> import os
    >>> for f in glob(op.join(folder, 'example.csv_semicircles.*')): os.remove(f)
    >>> os.remove(op.join(folder, 'example-of-error.csv_error.txt'))
    """
    _log(folder)
    while True:
        for csvfile in glob(op.join(folder, filetype)):
            if not op.exists(csvfile+suffix) and not op.exists(csvfile+error):
                _log(csvfile)
                try:
                    do_file(csvfile, suffix=suffix)
                    _log('done')
                except Exception as e:
                    open(csvfile+error, 'w').write(str(e))
                    _log('error')
        if _debug: break
        time.sleep(sleep)


def _log(message):
    print(str(datetime.now())[:19], message)


if __name__ == '__main__':
    import sys
    import doctest
    if len(sys.argv) > 1:
        """If this is called from command line with args, go into server mode."""
        watch(*sys.argv[1:])
    else:
        """Otherwise run doctests and plot the file-based test."""
        doctest.testmod()
        _graphic_test()
