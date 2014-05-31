import codecs
import glob
import os
import xml.etree.ElementTree as ET

# TODO: override this with a value input from the user
output_file = 'traces.csv'
# change this if you want the output file to use a different separator (if your user used commas in their data, for example
# separator = "|"
separator = ","

# open or create the output file, and add header information on the first line
with codecs.open(output_file, "w+", encoding='utf8') as myfile:
    myfile.write('ride' + separator + 'latitude ' + separator + 'longitude' + separator + 'elevation' + separator + 'time\n')

traces = []
# TODO: get this path from input. Right now, hard-coded to my local machine's dir structure
for file in glob.glob("C:\Python33\working\data\gpx_traces\*.gpx"):
    traces.append(file)

for trace in traces:
    tree = ET.parse(trace)
    # each file/xml root represents one ride
    ride = tree.getroot()

    # there is a metadata child and a trk child. Everything we do is on the trk child. Could make this more explicit.
    for data in ride:
        line = ""

        for trkseg in data:
            if('name' in trkseg.tag):
                name = trkseg.text

            if('trkseg' in trkseg.tag):
                for trkpt in trkseg:
                    if('trkpt' in trkpt.tag):
                        # the attrib here is a dictionary with lat and long in it.
                        lat_long = trkpt.attrib

                        for data in trkpt:
                            if 'ele' in data.tag:
                                ele = data.text
                            if 'time' in data.tag:
                                time = data.text

                        line = line + name + separator + lat_long['lat'] + separator + lat_long['lon'] + separator + ele + separator + time + "\n"
        with codecs.open(output_file, "a", encoding='utf8') as myfile:
            myfile.write(line)
