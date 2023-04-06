#!/bin/bash

# Extract sections from files. Remove certain parts and replace with tabulation string.
location_shortcuts=$(awk '/^# location shortcuts/{f=1} /^# command/{f=0} f' $scripts/shortcuts.sh | sed 's/export /    -   /g')
command_shortcuts=$(awk '/^# command shortcuts/{f=1} /^# script/{f=0} f' $scripts/shortcuts.sh | sed 's/alias /    -   /g')

# Display all custom commands as well as common usage.

cat << END

L${location_shortcuts: 3}



C${command_shortcuts: 3}

Python Dev Commands :

    -   update_deps : updates requirements.txt with all installed Python modules.
    -   create_docs: generates source code documentation using Sphinx. 
            - run 'create_docs -h' for help with the command.
    
    Note: These do not work on D2 Documentation Image.
    
D2 Documentation Commands
    -   diagram: generate diagrams in pdf format using D2.
            - run 'diagram' or for help with the command.

    Note: These do not work on Python Dev Image.
END

