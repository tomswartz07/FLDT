import csv, sys

with open('testhostnames.csv') as csvfile:
    reader = csv.reader(csvfile)
    try:
        for row in reader:
            print("mac"+row[1]+" "+"host"+row[0])
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
