#!/usr/bin/env python

import csv
import sys

# USAGE
# start with an originals/<x>.csv file
# remove the timestamps and total miles columns
# assert that the first row of headers is all spelled right
# sort by "have you ridden", and take out the no's
# go through names if you want, or you con do it after
# save it using excel, move it to the cleaned folder
# run python clean_spreadsheet.py clean/x.csv clean/x_cleaned.csv
# if you mess up, just run it again

# TODO: the other half where we save it
# pass a dict to model create http://stackoverflow.com/questions/1571570/can-a-dictionary-be-passed-to-django-models-on-create

# does a field need to be checked?
def needs_checking(field, val):
    field = field.lower()
    if val.strip() == '':
        return False

    # miles should be parse-able as a float
    if field.find('mile') >= 0:
        try:
            temp = float(val)
            if temp >= 20 and temp <= 999:
                return False
            else:
                return True
        except ValueError:
            return True

    # pace should be parse-able as a float
    if field.find('pace') >= 0:
        try:
            temp = float(val)
            if temp > 5 and temp < 50:
                return False
            else:
                return True
        except ValueError:
            return True

    if field.find('time') >= 0:
        return True
    return False

def test_check_function():
    # miles
    assert(needs_checking('miles', '10 miles') == True)
    assert(needs_checking('Sunday Miles', '10 miles') == True)
    assert(needs_checking('Tuesday Miles', '5') == True)
    assert(needs_checking('Sunday Miles', '5.9') == True)
    assert(needs_checking('Sunday Miles', '25') == False)
    assert(needs_checking('Wednesday Miles', '75') == False)
    assert(needs_checking('Miles', '1000') == True)

    # pace
    assert(needs_checking('what yo pace is', '7 mph') == True)
    assert(needs_checking('Pace', '7') == False)
    assert(needs_checking('Pace', 'uhhidunnobecause yeah') == True)
    assert(needs_checking('some pace', '5') == True) # bounds
    assert(needs_checking('some pace', '51') == True)

    # time
    assert(needs_checking('time', 'whateverishere') == True)
    assert(needs_checking('time', '01:00:00') == True) # even if its right

    # empty
    assert(needs_checking('time', '     ') == False)
    assert(needs_checking('pace', '     ') == False)
    assert(needs_checking('miles', '     ') == False)

test_check_function()
print "Check Function Test: passed"

if len(sys.argv) < 3:
    print "usage: python {0} <input_csv> <output_csv>".format(sys.argv[0])
    print "   this script will present every field that could be formatted wrong (miles, time, pace) and give you a chance to edit it before its thrown back."
    print "   input_csv should never be the same as output_csv"
    sys.exit(-1)

filename = sys.argv[1]
output = sys.argv[2]

if filename == output:
    print "Input and Output file cannot be the same"
    sys.exit(-1)

#U is for universal newline mode because excel saves it like that
with open(filename, 'rU') as csvfile:
    reader = csv.reader(csvfile)
    f = open(output, 'wb')
    writer = csv.writer(f)
    headers = []
    first = True
    for line in reader:
        line = [a.strip() for a in line]
        curr_name = ''
        out_line = []

        if first:
            # save the names, write it out, and be done
            headers = line
            writer.writerow(headers)
            first = False
            continue

        for i in xrange(len(line)):
            # grab the name
            if i == 0:
                curr_name = line[i]

            # spit it back out if it doesn't need to be checked
            if not needs_checking(headers[i], line[i]):
                out_line.append(line[i])
                continue

            # otherwise, present it
            print "User: {0}".format(curr_name)
            print "{0}: {1}".format(headers[i], line[i])
            new_val = raw_input("\nEnter to Skip, Type something to change: ")
            if new_val == '':
                out_line.append(line[i])
            else:
                out_line.append(new_val.strip())

        writer.writerow(out_line)

    f.close()
