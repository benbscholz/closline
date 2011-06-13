#!/usr/bin/python

#Copyright (C) 2011 by Ben Brooks Scholz

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from httplib import HTTPConnection
from urllib import urlencode
from sys import argv
from sys import exit
from optparse import OptionParser

# parse command line options
parser = OptionParser()

# optimization level options
parser.add_option("-s", action="store_const", const="simple", dest="optimize")
parser.add_option("-a", action="store_const", const="advanced", dest="optimize")
parser.add_option("-w", action="store_const", const="whitespace", dest="optimize")

# warning level options
parser.add_option("-q", action="store_const", const="quiet", dest="warning")
parser.add_option("-d", action="store_const", const="default", dest="warning")
parser.add_option("-v", action="store_const", const="verbose", dest="warning")

# pretty print option
parser.add_option("-p", action="store_true", dest="pprint")

(options, args) = parser.parse_args()

# check for filename argument
if len(args) == 0:
    print "Missing argument."
    exit()

# set the optimization type according to the parsed options
if options.optimize == "advanced":
    optimize_level = "ADVANCED_OPTIMIZATIONS"
    print "Compiling Javascript with advanced optimizations...\n"
elif options.optimize == "whitespace":
    optimize_level = "WHITESPACE_OPTIMIZATIONS"
    print "Compiling Javascript without whitespace...\n"
else:
    optimize_level = "SIMPLE_OPTIMIZATIONS"
    print "Compiling Javascript with simple optimizations...\n"

# set the warning type according to the parsed options
if options.warning == "verbose":
    warning_level = "VERBOSE"
elif options.warning == "quiet":
    warning_level = "QUIET"
else:
    warning_level = "DEFAULT"
    
# handle output file names
file_path = argv.pop()
input_js = open(file_path).read()    
comp_name = file_path[:len(file_path)-3] + ".min.js"
out_file = open(comp_name, 'w')

if options.pprint:
    # define the POST parameters with pretty print
    params = urlencode([
        ('js_code', input_js),
        ('compilation_level', optimize_level),
        ('output_format', 'text'),
        ('formatting', 'pretty_print'),
        ('output_info', 'compiled_code'),
    ])
else:
    # define the POST parameters without pretty print
    params = urlencode([
        ('js_code', input_js),
        ('compilation_level', optimize_level),
        ('output_format', 'text'),
        ('output_info', 'compiled_code'),
    ])

# define a second post request for compilation data
stat_params = urlencode([
    ('js_code', input_js),
    ('compilation_level', optimize_level),
    ('output_format', 'text'),
    ('output_info', 'statistics'),
])

# prepare the connection
headers = { "Content-type": "application/x-www-form-urlencoded" }
connect = HTTPConnection('closure-compiler.appspot.com')

# make the HTTP request for compiled code
connect.request('POST', '/compile', params, headers)
output = connect.getresponse().read()

# make the HTTP request for compilation statistics
connect.request('POST', '/compile', stat_params, headers)
stats = connect.getresponse().read()
print stats

# close the connection
connect.close()

if len(output) == 1:
    print "Code compiled to nothing! There may be an error."
else:
    print "Complete."


out_file.write(output)
out_file.close()
