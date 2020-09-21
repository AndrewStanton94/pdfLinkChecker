#!/usr/bin/python

import csv
import json
import codecs
from os import walk


# Export results
# text = json.dumps(pdf.summary, indent=4)
# with codecs.open(fileName, "w", "utf-8") as f:
    # f.write(text)


# with open('pdfsToCheck.txt', 'r') as file:
    # files = [line.replace('\n', '') for line in file.readlines()]

csvFile = open('results.csv', 'w')
writer = csv.writer(csvFile)
writer.writerow(['name', 'url', '200', '404', 'others'])


# Get files in output directory
files = []
for (_, _, filenames) in walk("output"):
    files.extend(filenames)
    break


for filename in files:
    with open('output/' + filename, 'r') as file:
        data = json.loads(file.read())
        name = data['source']['filename']
        location = data['source']['location']

        refCheck = data['refCheck']
        if '200' in refCheck:
            valid = '\n'.join(refCheck['200'])
        else:
            valid = ''

        if '404' in refCheck:
            missing = '\n'.join(refCheck['404'])
        else:
            missing = ''

        output = [name, location, valid, missing]
        otherKeys = [k for k in refCheck.keys() if k not in ['200', '404']]
        for key in otherKeys:
            output.append(key + ': \n\n' + '\n'.join(refCheck[key]))
        print(output)
        writer.writerow(output)

csvFile.close()
