#!/bin/bash

# Use Sphinx to generate html with styling using Google style in-file documentation.
# HTML will be located in documentation/code/html. Users should access index.html as it
# connects all other hmtl files.


sphinx_config="${config}/sphinx/"
major_update=false
feature_update=false
run_update_version=true

usage() {

    cd -

    # print as plain text in terminal up until keyword END
    cat << END
Usage : Use Sphinx to generate html for documentation located within source code. 

        Note: When used without any flags, fix version will be incremented.

        Ex. create_docs -> curr version = 1.0.0 -> new version = 1.0.1

        Flags options: -n, -f , -m , -h

        -n ) Specifies not to update the release version. Useful for quick fixes to comments/code.

            Ex. create_docs -n -> curr version = 1.0.0 -> new version = 1.0.0

        -f ) Specifies the that source code contains a feature update. Update version to match.

            Ex. create_docs -f -> curr version = 1.0.0 -> new version = 1.1.0

        -m ) Specifies the that source code contains a major update. Update version to match.

            Ex. create_docs -m -> curr version = 1.0.0 -> new version = 2.0.0

        -h) Display help/usage. If no valid flag combinations or unrecognized flags are provided, help/usage
            will display.

END

    exit 0;
}

update_version() {
    # Get current documentation version from conf.py file; seperate by version type.
    curr_version=$(awk "/^release/{print $NF}" ./conf.py) && curr_version=${curr_version: -6:-1}
    major_version=${curr_version: -5:1}
    feature_version=${curr_version: -3:1}
    fix_version=${curr_version: -1:1}

    # Increment version based on passed flags.
    if [ "$major_update" = true ] ; then
        major_version=$(( $major_version + 1))
    elif [ "$feature_update" = true ] ; then
        feature_version=$(( $feature_version + 1))
    else
        fix_version=$(( $fix_version + 1))
    fi

    replacement_string="release = '${major_version}.${feature_version}.${fix_version}'"

    # do an inline replacement of version within conf.py file
    sed -i "s/^release.*/${replacement_string}/" ./conf.py

}

generate_rst_files() {
    # Create reStructuredText files based on in-file comments.
    # These are stored in config/sphinx and should not be modified by users.

    ## force : generate new rst files. Ensures new changes are added.
    ## separate : give each module its own page.
    ## module-first : put module docs before submodule docs.
    if [ "$run_update_version" = true ] ; then
        update_version
    fi

    sphinx-apidoc $src --output . --separate --module-first
}

create_html() {
    # use reStructuredText files to create html files. Use 
    make clean && make html

    clear

    echo "Index html file is located in documentation/code/html. Live Server is installed for quick viewing."
}

while getopts "mfhn" flag; do
    case $flag in
    m ) # user indicates major update
        major_update=true ;;

    f ) # user indicates feature update.
        feature_update=true ;;
    
    n ) # user indicates not to update version.
        run_update_version=false ;;

    h | * ) # display help
        usage ;;
    esac
done

# change to sphinx config folder (reqd.) and run generation.
cd $sphinx_config
generate_rst_files
create_html

back

exit 0;
