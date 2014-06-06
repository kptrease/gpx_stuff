import codecs
import glob
import os
import xml.etree.ElementTree as ET
import sys
from optparse import OptionParser

#TODO: OptionParser is deprecated, so need to switch over to ArgParse
parser = OptionParser()
parser.add_option('-i', '--input', dest='data_dir', type='string', action='store',
                  help='path to the directory your gpx files live in')
parser.add_option('-o', '--output', dest='output_file', type='string', action='store', default='traces.csv',
                  help='what you\'d like your output file to be called. Default is traces.csv. Include full destination '
                       'file path to put it where you want.')
parser.add_option('-d', '--delimiter', dest='delimiter', type='string', action='store', default=',',
                  help='what delimiter would you like to use? Default is comma, but use another if your user uses commas'
                       'in their trace names')

parser.set_defaults(verbose=True)
(options, args) = parser.parse_args()

if options.data_dir:
    data_dir = options.data_dir
if options.output_file:
    output_file = options.output_file
if options.delimiter:
    delimiter = options.delimiter

# set this value to obscure the endpoints (protect the privacy of the people provding the traces
# strips out this many points from the beginning and end of each ride
# TODO: would like to make this a user parameter, but having trouble thinking throug the semantics of a boolean param. Could just make it an int
points_to_obscure = 50

# open or create the output file, and add header information on the first line
with codecs.open(output_file, "w+", encoding='utf8') as myfile:
    myfile.write('ride' + delimiter + 'latitude' + delimiter + 'longitude' + delimiter + 'elevation' + delimiter + 'time\n')

traces = []

data_dir = data_dir + "\*.gpx"
for file in glob.glob(data_dir):
    traces.append(file)

for trace in traces:
    tree = ET.parse(trace)
    # each file/xml root represents one ride
    ride = tree.getroot()

    # there is a metadata child and a trk child. Everything we do is on the trk child. Could make this more explicit.
    for data in ride:

        for trk in data:
            if('name' in trk.tag):
                name = trk.text

            if('trkseg' in trk.tag):
                lines = []
                for trkpt in trk:
                    if('trkpt' in trkpt.tag):
                        # the attrib here is a dictionary with lat and long in it.
                        lat_long = trkpt.attrib

                        for data in trkpt:
                            if 'ele' in data.tag:
                                ele = data.text
                            if 'time' in data.tag:
                                time = data.text
                        line = name + delimiter + lat_long['lat'] + delimiter + lat_long['lon'] + delimiter + ele + delimiter + time + "\n"
                        lines.append(line)

                with codecs.open(output_file, "a", encoding='utf8') as myfile:
                    for i in range(points_to_obscure, (len(lines) - points_to_obscure)):
                        myfile.write(lines[i])
