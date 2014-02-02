#!/usr/bin/env python

# WHAT TERRIBLE HACKS! But it's okay, we only need to use this once.
import sys, os
sys.path.append('/users/parth/Development/t4k-rms')
from t4krms import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 't4krms.settings'

import csv
import sys
from datetime import datetime, timedelta
from fitness.models import Ride
from riders.models import Teammate

# SOME SERIOUS ASSUMPTIONS
# Fields come in following order:
# Name, Sunday Miles, Sunday Pace,
if len(sys.argv) < 4:
    print "usage: python {0} <cleaned csv file> <start date YYYY-MM-DD> <output_file>"
    print "  interactive prompt per ride, so that you can verify each one."
    sys.exit(-1)

filename = sys.argv[1]
start_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
output = sys.argv[3]

with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)

    # output file for errors that need to be manually sorted out
    output_file = open(output, 'w')
    writer = csv.writer(output_file)
    header = []
    first = True

    out_row = []

    # for each person
    for line in reader:

        # header row
        if first:
            # write headers
            writer.writerow(line);
            first = False
            continue

        NUM_FIELDS = 5 # miles, time, pace, who with, description
        name = line[0].strip()
        yes_no = line[1]
        out_row.append(name)
        out_row.append(yes_no)

        # get Teammate from name
        # TODO: I hope this works with middle names.....
        #  Jennifer Sunshine Garrison
        #  Rachel Madi Madison
        first_name = name.split(' ', 1)[0]
        last_name = name.split(' ', 1)[1]

        # Attempt to find a user based on a name

        # search by first name
        query = Teammate.objects.filter(first_name__iexact = first_name)

        # if we can't find someone with that first name, write the line out and continue
        if len(query) <= 0:
            print "UNKNOWN NAME: {0}. Skipping....".format(name)
            writer.writerow(line)
            continue

        # first name was enough, we're good to go
        if len(query) == 1:
            rider = query[0]
        else:
            # now use last name
            query = query.filter(last_name__iexact = last_name)

            #it could still not work
            if len(query) <= 0:
                print "UNKNOWN NAME: {0}. Skipping....".format(name)
                writer.writerow(line)
                continue
            # but if it does, awesome
            elif len(query) == 1:
                rider = query[0]
            # but there may be uniqueness problems still.
            else:
                print "NON-UNIQUE NAME: {0}. Skipping....".format(name)
                writer.writerow(line)
                continue

        assert(rider is not None)
        curr_date = start_date + timedelta(days=-1)
        for day in xrange(7):
            curr_date += timedelta(days=1)
            idx = NUM_FIELDS * day + 2 # get past first 2
            if line[idx].strip() == '':
                for i in xrange(5):
                    out_row.append("")
                continue
            miles = float(line[idx])
            time = line[idx+1]
            pace = float(line[idx+2])
            buddies = line[idx+3]
            description = line[idx+4]

            print "Logging Ride For {0}".format(rider.get_full_name())
            print "Date: {0}".format(curr_date)
            print "Miles: {0}".format(miles)
            print "Time: {0}".format(time)
            print "Pace: {0}".format(pace)
            print "Buddies: {0}".format(buddies)
            print "Description: {0}\n".format(description)
            response = raw_input('Is that good (y/n): ')
            if response == 'y' or response == 'yes':
                for i in xrange(5):
                    out_row.append("")
                r = Ride(user=rider, date=str(curr_date), buddies=buddies, miles=miles, pace=pace, duration=time, comments=description)
                r.save()
                print "done."
            else:
                out_row.append(miles)
                out_row.append(time)
                out_row.append(pace)
                out_row.append(buddies)
                out_row.append(description)
                print "cool, i'll leave it."


        writer.writerow(out_row)

    output_file.close();
