#!/bin/bash

# creates shortcuts for all users. Ran during container initialization.

# location shortcuts
export airkeys="${HOME}/airkeys"
export scripts="${HOME}/airkeys/scripts"
export documentation="${HOME}/airkeys/documentation"
export config="${HOME}/airkeys/config"
export src="${HOME}/airkeys/src"

# command shortcuts
alias all="ls -al"
alias rm="rm -i"
alias rmd="rm -ri"
alias rmf="rm -f"
alias lint="black ${src} --line-length 100 --target-version py311"

# script shortcuts
alias update_deps="${scripts}/shortcut_scripts/update_dependencies.sh"
alias create_docs="${scripts}/shortcut_scripts/create_source_documentation.sh"
alias commands="${scripts}/command_help.sh"
alias test="${scripts}/shortcut_scripts/run_pytest.sh"

# d2 documentaton-only
alias diagram="${scripts}/create_diagram.sh"

# usefule inline functions
inline_funcs='back'

back() {
    if [[ -z $OLDPWD ]] ; then
        cd ${airkeys}
    else
        cd -
    fi
}

for inline_func in $inline_funcs ; do export -f $inline_func ; done 

# path exports 
export PYTHONPATH=$PYTHONPATH:${src}
export PATH=$PATH:/home/NRuser/.local/bin/
