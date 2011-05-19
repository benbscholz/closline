#closline
###a small python script for google's closure compiler

###usage
    python closline.py [-s -a -w] [-q -d -v] script.js
    
####example
    python closline -w -q script.js
####file output
    script.min.js
    
####options
#####optimization type
    -s      simple optimization
    -a      advanced optimization
    -w      whitespace only

#####output type
    -q      quiet
    -d      default
    -v      verbose
    
MIT Licensed.
