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


def do_file(csvfile, suffix='_semicircles.shp', to_file=True):
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
    """
    gdf = gpd.GeoDataFrame(pd.read_csv(csvfile))
    semicircles = [semicircle(r['x'], r['y'], r['radius'], r['rotation']) for i, r in gdf.iterrows()]
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
    """Watch a folder for new files to process.

    Runs from the command line like:
    C:\Users\scarborj\Documents\GitHub\bda-semicircle>\Users\scarborj\Documents\venv\bda-semicircle\
    Scripts\python.exe deploy.py \\olgwfap1\Transfer\semicircles

    >>> folder = '//olgwfap1/Transfer/semicircles/'
    >>> watch(folder=folder, _debug=True)  #doctest:+ELLIPSIS
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles/
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles\example-of-error.csv
    2018-...-... ...:...:... //olgwfap1/Transfer/semicircles\example.csv
    >>> import os
    >>> for f in glob(op.join(folder, 'example.csv_semicircles.*')): os.remove(f)
    >>> os.remove(op.join(folder, 'example-of-error.csv_error.txt'))
    """
    print(str(datetime.now())[:19], folder)
    while True:
        for csvfile in glob(op.join(folder, filetype)):
            if not op.exists(csvfile+suffix) and not op.exists(csvfile+error):
                try:
                    print(str(datetime.now())[:19], csvfile)
                    do_file(csvfile, suffix=suffix)
                except Exception as e:
                    open(csvfile+error, 'w').write(str(e))
        if _debug: break
        time.sleep(sleep)


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
