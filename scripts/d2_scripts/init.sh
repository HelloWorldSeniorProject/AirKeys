#!/bin/bash

# A collection of container initialization tasks. Includes 
# permission changes.

# refresh env variables.
. ${HOME}/.bashrc

task_list='prep_scripts delete_extras'
tasks=$(echo "$task_list" | wc -w)
completed=0

echo "---------------------------------"
echo "Logged in as: $(whoami)"
echo "Running startup script; Remaining Tasks: ${tasks}"

prep_scripts (){

    echo "Granting execute perms for all scripts in folder."

    for script in ${scripts}/*.sh; do echo "Modifying $script " && chmod +x $script && dos2unix $script; done;
    
    display_progress
}

delete_extras () {
    echo "Deleting Temp Svgs"

    # delete all svgs in source of design. These are generated by interactive mode
    # and not needed.
    for extra in ${documentation}/design/source/*.svg; do
        rm -f $extra
    done

    display_progress
}

display_progress() {
    completed=$((completed+1))
    echo "Tasks completed => ${completed} / ${tasks}"
}

# Run all tasks
for t in $task_list; do $t; done

echo "---------------------------------"
echo "Startup script completed."