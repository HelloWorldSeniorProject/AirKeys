#!/bin/bash

# Run Pytest from testing folder. Gives users the ability to specify to only run certain files or functions within files.
filename=""
funcname=""
run_all=false
test_dir=${src}/test/
temp_dir=${test_dir}/temp/

usage() {

    # print as plain text in terminal up until keyword END
    cat << END
Usage : Run test functions in tests folder using Pytest. 

        Flags options: -f, -m , -a , -h

        -f ) Specifies the test file. The entire tests folder is search so there is no need to pass
             the folder the file is in. Partial names also work.

            Ex. test -f test_s -> runs all functions of files under test that match the pattern test_s{...}.py.

        -m ) Specifies a function to run.

            Ex. test -f test_s -m test_func-> runs the function test_func() of files under test that match
                the pattern test_s{...}.py, if available.

        -a ) Run all test files and functions under tests folder. Pytest requires test files be named either test_*.py 
             or *_test.py where * is any combination of characters.

            Ex. test -a -> runs all test files.

        -h) Display help/usage. If no valid flag combinations or unrecognized flags are provided, help/usage
            will display.

END

    exit 0;
}

run_specific_tests(){
    
    for file in $filename; do

        # append function name to files.
        if ! [ -z "${funcname}" ]; then
            full_test_path="${file}::funcname"
        else
            full_test_path="${file}"
        fi

        python -m pytest -v -rpfs -s ${full_test_path}

    done

    exit 0;
}

run_all_tests() {
    # run all tests of the format test_*.py or *_test.py
    python -m pytest -v -rpfs -s ${test_dir}
}

find_file() {

    # find all files matching passed substring.
    filename=$(find ${test_dir} -name ${filename})

    if [ -z "${filename}" ]; then

        echo "File not found under ${test_dir}"
        exit 0;
    fi

    run_specific_tests
}

# create temp dir in test suite
if [ ! -d "${temp_dir}" ]; then
    mkdir ${temp_dir}
fi

while getopts "f:m:a" flag; do
    case $flag in
    f ) # filename to search for.
        filename="${OPTARG%.*}*.py" ;;

    m ) # method to search for.
        funcname="${OPTARG}" ;;

    a ) # run all tests.
        run_all=true ;;

    h | * ) # display help
        usage ;;
    esac
done

if [ "${run_all}" = true ]; then
    run_all_tests
elif [ -z "${filename}" ]; then
    echo -e "No file specified \n" && usage
else
    find_file
fi

