#!/bin/bash

# creates shortcuts for all users. Ran during container initialization.

# location shortcuts
export scripts="${HOME}/airkeys/scripts"
export documentation="${HOME}/airkeys/documentation"

# command shortcuts
alias all="ls -al"
alias rm="rm -i"
alias rmd="rm -ri"
alias rmf="rm -f"

# d2 documentaton-only
alias diagram="${scripts}/create_diagram.sh"
alias update_deps="${scripts}/update_dependencies.sh"
