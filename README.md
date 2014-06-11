gpx_stuff
=========

code for handling and processing gpx files

convert_single_rider.py:

Takes a directory full of gpx files and spits out a csv with all the trackpoints. Used to prepare a tableau public readable dataset from a dump of strava files.

All trackpoints are output with no rider information, so you can put as many as you like from different riders, and it will show up as one large dataset (useful for building a heatmap).

This was used to generate the data behind the maps for this visualiation:
http://www.tableausoftware.com/public/blog/2014/05/kate039s-quantified-bike-commute-2485


convert_normalize.py:

This is my first attempt to "normalize" the data, by building separate "tables" (output files) for riders and rides, to reduce the size of the dataset. Adds rider information to each trackpoint to allow for filtering by rider.

A new viz on tableau public based on this will be coming soon.

Input dir structure should be like so:

<input_dir>\rider1\gpx files
           \rider2\gpx files
            etc.

The output will be data.csv, rides.csv and riders.csv. You'll need to import data.csv into tableau, then import rides.csv
and riders.csv. Do an inner join on rider_ID and on ride_ID, then bring this into the viz.

I'm ramping up on python, and there's no doubt in my mind that it's possible to do all this with a lot fewer lines of code. Suggestions welcome!
