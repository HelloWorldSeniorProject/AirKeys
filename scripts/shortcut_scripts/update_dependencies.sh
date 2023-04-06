#!/bin/bash

# Update all Python requirements file for future loads

update_python_deps () {
    pip freeze > ${config}/requirements.txt

    echo "requirements.txt updated"
}



echo "Updating requirements file(s)"
update_python_deps


exit 0;