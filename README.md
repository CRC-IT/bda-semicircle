# bda-semicircle
Generate semicircle polygons for approximation of drainage radius on a dip.

`semicircle.py` has the algorithm to generate a circle then clip with a rotated and offset square.

`deploy.py` will watch a network share directory, process input from CSV files, and output Shapefiles.  

The format of a `*.csv` placed in `\\olgwfap1\Transfer\semicircles` is `x, y, radius, rotation`, and must have that header.  
Rotation is degrees counter clockwise from East.

Contact is James Scarborough for California Resources Corp - Big Data Analytics
