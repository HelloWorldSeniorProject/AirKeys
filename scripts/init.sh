#!/bin/bash

# A collection of container initialization tasks. Includes 
# permission changes and installing dependencies.

<<<<<<< HEAD
# refresh env variables.
. ${HOME}/.bashrc

=======
>>>>>>> develop
task_list='grant_ownership prep_scripts install_dev_dependencies'
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

prep_scripts (){

    echo "Granting execute perms for all scripts in folder."

<<<<<<< HEAD
    for script in ${scripts}/*.sh; do echo "Modifying $script " && chmod +x $script && dos2unix $script; done;
=======
    for script in ./scripts/*; do echo "Modifying $script " && chmod +x $script; done;
>>>>>>> develop
    
    display_progress
}

install_dev_dependencies () {
    echo "Installing dependencies"

    # if requirements file listing all python modules doesn't exist, create it.
<<<<<<< HEAD
    if ! [ -e "requirements.txt" ]; then 
=======
    if [ ! -e "requirements.txt" ]; then 
>>>>>>> develop
        echo "No requirements document found. Creating: requirements.txt"
        pip3 freeze > requirements.txt 
    fi
    
    # install all python modules.
    pip install -r requirements.txt

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

