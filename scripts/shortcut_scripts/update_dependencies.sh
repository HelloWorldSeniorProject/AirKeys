#!/bin/bash

# Update all Python requirements file for future loads

update_python_deps () {
    pip freeze > ${config}/requirements.txt

    picam_str='
# Install only on Pi; fails otherwise.
# picamera==1.13
'
    
    printf "$picam_str" >> ${config}/requirements.txt

    echo "requirements.txt updated"
}



echo "Updating requirements file(s)"
update_python_deps


exit 0;