#!/bin/bash

# Streamlines and standarized all graphical exports using D2.

# Parameter vars
source_dir="${documentation}/design/source"
output_dir="${documentation}/design/output"
input_file=''
output_file=''
interactive_mode=false

usage() {
    # print as plain text in terminal up until keyword END
    cat << END
WARNING: This command is only to be used within the documentation container. Use in other containers will result in error.

Usage : Interactively view diagrams or Create a diagram in svg, png, or pdf format. 

        Flags options: -f , -o , -i , -h, -a

        -f) Specifies the source file. This flag along with the source file must be passed first for file generation
            and interactive mode or the command will return an error. 

            Source files are relative to /documentation/design/source folder, therefore only {filename}.d2
            need be passed.

            Ex. diagram -f test.d2 -> creates pdf -> /documentation/design/output/test.pdf

        -o) Specifies the output filename and extension. If this value is not passed, the generated file 
            will be a pdf version of the input file located in /documentation/design/output.

            Ex. diagram -f test.d2 -o out.png -> creates png -> /documentation/design/output/out.png
                diagram -f test.d2 -o out.pdf -> creates pdf -> /documentation/design/output/out.pdf

        -i) Opens diagram in interactive mode. Source file will be displayed and any changes to source file 
            will update graphic. Opens web browser.

            Ex. diagram -f test.d2 -i -> opens browser window to view changes to test.d2

        -h) Display help/usage. If no valid flag combinations or unrecognized flags are provided, help/usage
            will display.

        -a) Convert all files D2 files in /documentation/design/source to pdf version. Uses the name of the input
            file. No need to specify input file.
            
            *This flag should only be used during when necessary. May cause inadvertant updates.* 

END

    exit 0;
}

convert_to_media () {
    # check if output filename and extension passed
    if [ -z "${output_file}" ]; then
        echo "Creating ${input_file%.*}.pdf"
        d2 ${source_dir}/${input_file} ${output_dir}/${input_file%.*}.pdf
    else
        echo "Creating ${output_file}"
        d2 ${source_dir}/${input_file} ${output_dir}/${output_file}
    fi
    
}

interactive_mode () {
    d2 --watch ${source_dir}/${input_file}
}

convert_all() {
    output_file=""

    # check if directory empy
    if ! [ "$(ls -A ${source_dir})" ]; then
        echo "No files to convert"
        exit 0;
    fi

    for source_file in ${source_dir}/*.d2 ; do 
        input_file="${source_file##*/}"
        convert_to_media
    done

    exit 0;
}

while getopts "hif:o:a" flag; do
    case $flag in

    i ) # display graph and update on source change. Opens web browser tab using default browser.
        interactive_mode=true ;;

    f ) # provide the source file for functions. Must be supplied for conversion and interactive mode.
        if [ -e ${source_dir}/${OPTARG} ] ; then
            input_file="${OPTARG}"
        else
            echo $source_dir/${OPTARG}
            echo "Error: File does not exist."
            usage
        fi ;;
    
    o ) # provide the ouput filename and extension. See usage for more details.

        # verify filename ends in .png / .pdf / .svg
        if ! [[ "${OPTARG: -4}" =~ ^(.pdf|.png|.svg) ]]; then
            echo "Invalid extension. Extension must be .pdf, .png, or .svg."
            exit 0;
        fi

        # confirm overwrite if needed.
        if [ -e ${output_dir}/${OPTARG} ] ; then
            echo "File already exists. Overwrite? (y/n)"
            read resp
                if ! [[ "${resp}" =~ ^(y|yes|Yes|Y) ]] ; then
                    echo "Operation cancelled."
                    exit 0;
                fi
        fi
        
        output_file=${OPTARG}
        ;;

    a) # create pdfs for all files in source folder.
        convert_all ;;

    h | * ) # display usage. Triggers if unknown flag or -h flag is passed.
            usage ;;
    esac
done 

if [ $# -eq 0 ] ; then
    echo "No flags supplied" 
    usage 
else 
    if [ "$interactive_mode" = true ]; then
        interactive_mode
    else
        convert_to_media
    fi
    
    exit 0;
fi




