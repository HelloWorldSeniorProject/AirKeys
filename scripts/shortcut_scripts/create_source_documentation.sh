#!/bin/bash

# Use Sphinx to generate html with styling using Google style in-file documentation.
# HTML will be located in documentation/code/html. Users should access index.html as it
# connects all other hmtl files.


sphinx_config="${config}/sphinx/"



generate_rst_files() {
    # Create reStructuredText files based on in-file comments.
    # These are stored in config/sphinx and should not be modified by users.

    ## force : generate new rst files. Ensures new changes are added.
    ## separate : give each module its own page.
    ## module-first : put module docs before submodule docs.
    sphinx-apidoc $src --output . --force --separate --module-first
}

create_html() {
    # use reStructuredText files to create html files. Use 
    make html

    clear

    echo "Index html file is located in documentation/code/html. Live Server is installed for quick viewing."
}

run() {
    # change to sphinx config folder (reqd.) and run generation.
    cd $sphinx_config

    generate_rst_files
    create_html

    cd -

    exit 0;
}

run