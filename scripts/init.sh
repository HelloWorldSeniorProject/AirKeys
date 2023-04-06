#!/bin/bash

# A collection of container initialization tasks. Includes 
# permission changes and installing dependencies.

# refresh env variables.
. ${HOME}/.bashrc

task_list='grant_ownership prep_scripts'
tasks=$(echo "$task_list" | wc -w)
completed=0

echo "---------------------------------"
echo "Logged in as: $(whoami)"
echo "Running startup script; Remaining Tasks: ${tasks}"

grant_ownership() {
    echo "Changing directory ownership from root to NRuser"
    
    sudo chown -R NRuser /home/NRuser

    display_progress
}

prep_scripts() {

    echo "Granting execute perms for all scripts in folder."

    # sys scripts
    for script in ${scripts}/*.sh; do chmod +x $script && sudo dos2unix $script; done;

    # command scripts
    for script in ${scripts}/shortcut_scripts/*.sh; do chmod +x $script && sudo dos2unix $script; done;

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

