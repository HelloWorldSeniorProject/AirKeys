#!/bin/bash

# Update all Python requirements file for future loads

update_python_deps () {
    pip freeze > ${config}/requirements.txt

    echo "requirements.txt updated"
}

run() {
    update_python_deps
}

echo "Updating requirements file(s)"

run

exit 0;