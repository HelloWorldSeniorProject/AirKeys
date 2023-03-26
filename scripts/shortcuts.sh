#!/bin/bash

# creates shortcuts for all users. Ran during container initialization.

# location shortcuts
scripts="~/airkeys/scripts"
documentation="~/airkeys/documentaion"

# command shortcuts
alias all="ls -al"
alias rm="rm -i"
alias rmf="rm -ri"


# d2 documentaton-only
alias diagram="${scripts}/create_diagram.sh"