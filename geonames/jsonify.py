#!env python

import io, os, sys, getopt, json, codecs

verbose = False
start_char = '['
end_char = ']'
seperator = ','
# Set this to '4' if you want your JSON pretty
indent = 0

def parse_boolean(str):
    if str == '1' or str == 1:
        return True
    return False

def uri(id):
    return (f"https://sws.geonames.org/{id}/", f"https://sws.geonames.org/{id}/")

def convert_geoname_line(data, output):
    names = data[3].split(',')
    names.append(data[2])
    if (data[15] == ''):
        elevation = 0
    else:
        elevation = data[15]
    obj = {'id': int(data[0]),
            'uri': uri(data[0]),
            'name': data[1],
            'alternatename': list(filter(None, set(names))),
            'coordinate': data[4] + ',' + data[5],
            'coordinates': {'latitude': float(data[4]), 'longitude': float(data[5])},
            'featureclass': data[6],
            'featurecode': data[7],
            'country': data[8],
            'population': int(data[14]),
            'elevation': int(elevation),
            'timezone': data[17]}
    json.dump(obj, output, indent=indent, ensure_ascii=False)

def convert_alternative_line(data, output):
    if data[9] == '\n':
        to = ''
    else:
        to = data[9]
    doc = { 'id': data[1] + '-' + data[0],
            'alternativeid': int(data[0]),
            'geonameid': int(data[1]),
            'isolanguage': data[2],
            'alternate name': data[3],
            'isPreferredName': parse_boolean(data[4]),
            'isShortName': parse_boolean(data[5]),
            'isColloquial': parse_boolean(data[6]),
            'isHistoric': parse_boolean(data[7]),
            'from': data[8],
            'to': to}
    
    obj = {'id':int(data[1]),
           'alternatename_docs': { 'add': doc}}
    json.dump(obj, output, indent=indent, ensure_ascii=False)

def convert_file(input, output, func):
    for line in input:
        func(line.split('\t'), output)
        output.write(seperator)
    else:
        func(line.split('\t'), output)

def main(argv):
    help = 'jsonify.py -g geonamesexport.txt or jsonify.py -a alternatives.txt'
    test = False
    try:
        opts, args = getopt.getopt(argv,"hvtg:a:o:",["geonames-file=", "alternatives-file", "output",])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
 
    gFile = aFile = ''
    output = io.StringIO()
    output_file = ''
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ("-g", "--geonames-file"):
            gFile = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-a", "--alternatives-file"):
            aFile = arg
        elif opt == '-t':
            test = True
        elif opt == '-v':
            verbose = True
            print("Enabled verbose mode")
    
    if output_file == '' or output_file == '-':
#        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        output = sys.stdout
    else:
        output = open(output_file, "w", "utf-8")


    if gFile == '' and aFile == '':
        print("No file given, exiting!")
        sys.exit(1)
    elif gFile != '':
        if gFile == '-':
            input = sys.stdin
        else:
            input = open(gFile, 'rt')
        output.write(start_char)
        convert_file(input, output, convert_geoname_line)
        output.write(end_char)
    elif aFile != '':
        if aFile == '-':
            input = sys.stdin
        else:
            input = open(aFile, 'rt')
        output.write(start_char)
        convert_file(input, output, convert_alternative_line)
        output.write(end_char)
    else:
        print("Unexpected error, exiting!")
        sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
   