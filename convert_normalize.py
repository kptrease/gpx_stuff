import glob
import os
import xml.etree.ElementTree as ET

# TODO: override this with a value input from the user
output_data_file = 'data.csv'
output_rider_file = 'riders.csv'
output_rides_file = 'rides.csv'
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

riders = get_immediate_subdirectories("data\gpx_traces")

print(riders)


for rider in riders:

    traces = []
    for file in glob.glob("data\gpx_traces\\" + rider + "\*.gpx"):
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
            line = ""

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

                            line = line + str(ride_id) + separator + str(rider_id) + separator + lat_long['lat'] + separator + lat_long['lon'] + separator + ele + separator + time + "\n"
                            # print(".", end = '')
            with open(output_data_file, "a") as myfile:
                myfile.write(line)
