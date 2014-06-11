import codecs
import glob
import os
import xml.etree.ElementTree as ET
from optparse import OptionParser

#TODO: OptionParser is deprecated, so need to switch over to ArgParse
parser = OptionParser()
parser.add_option('-i', '--input', dest='data_dir', type='string', action='store',
                  help='path to the directory your gpx files live in. Dirs for each rider, each with gpx files, should live in this dir')
parser.add_option('-o', '--output', dest='output_dir', type='string', action='store',
                  help='directory you\'d like your output files to be saved in.')
parser.add_option('-d', '--delimiter', dest='delimiter', type='string', action='store', default=',',
                  help='what delimiter would you like to use? Default is comma, but use another if your user uses commas'
                       'in their trace names')

parser.set_defaults(verbose=True)
(options, args) = parser.parse_args()

if options.data_dir:
    data_dir = options.data_dir
if options.output_dir:
    output_dir = options.output_dir
if options.delimiter:
    delimiter = options.delimiter

# set this value to obscure the endpoints (protect the privacy of the people provding the traces
# strips out this many points from the beginning and end of each ride
# TODO: would like to make this a user parameter, but having trouble thinking throug the semantics of a boolean param. Could just make it an int
points_to_obscure = 50

output_data_file = output_dir + '\\data.csv'
output_rider_file = output_dir + '\\riders.csv'
output_rides_file = output_dir + '\\rides.csv'
rider_id = 0
ride_id = 0
separator = "|"

# open or create the rider file, and add header information on the first line
with open(output_rider_file, "w+") as myfile_rider:
    myfile_rider.write('rider_id|rider\n')

# open or create the rides file, and add header information on the first line
with open(output_rides_file, "w+") as myfile_rides:
    myfile_rides.write('ride_id|ride\n')

# open or create the data file, and add header information on the first line
with open(output_data_file, "w+") as myfile:
    myfile.write('ride_ID' + separator + 'rider_ID' + separator + 'latitude ' + separator + 'longitude' + separator + 'elevation' + separator + 'time\n')

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

riders = get_immediate_subdirectories(data_dir)

print(riders)


for rider in riders:

    traces = []
    for file in glob.glob(data_dir + "\\" + rider + "\*.gpx"):
        traces.append(file)

    # write a new rider and rider ID to the riders file
    rider_id += 1
    with open(output_rider_file, "a") as myfile_rider:
        myfile_rider.write(str(rider_id) + separator + rider + '\n')

    for trace in traces:
        tree = ET.parse(trace)
        # each file/xml root represents one ride
        ride = tree.getroot()

        # there is a metadata child and a trk child. Everything we do is on the trk child. Could make this more explicit.
        for data in ride:
            lines = []

            for trkseg in data:
                if('name' in trkseg.tag):
                    ride = trkseg.text
                    ride_id += 1

                    # write a new ride and ride ID to the rides file
                    with open(output_rides_file, "a") as myfile_rides:
                        myfile_rides.write(str(ride_id) + separator + str(ride) + '\n')

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

                            line = str(ride_id) + separator + str(rider_id) + separator + lat_long['lat'] + separator + lat_long['lon'] + separator + ele + separator + time + "\n"
                            lines.append(line)

                with codecs.open(output_data_file, "a", encoding='utf8') as myfile:
                    for i in range(points_to_obscure, (len(lines) - points_to_obscure)):
                        myfile.write(lines[i])


