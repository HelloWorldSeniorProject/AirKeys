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

            Ex. test -f test_file -> runs all functions of files under test that match the pattern test_s{...}.py.

            Note: No need to include .py extension.

        -m ) Specifies a function(s) to run.

            Ex. test -f test_file -m test_func-> runs the function test_func() of files under test that match
                the pattern test_file{...}.py, if available.

            Note: To specify multiple tests, use quotes '' and 'or' in-between each test name.

            Ex. test -f test_file -m 'test_setup or test_singleton' -> runs the functions test_setup and test_singleton 
            if they exist within any file pattern matching test_file{...}.py, if available.

            Note: Removes conditional check for specified test function(s). Be sure to run only tests you are comfortable with.

        -a ) Run all test files and functions under tests folder. Pytest requires test files be named either test_*.py 
             or *_test.py where * is any combination of characters.

            Ex. test -a -> runs all test cases for every test file.

        -h) Display help/usage. If no valid flag combinations or unrecognized flags are provided, help/usage
            will display.

END

    exit 0;
}

run_specific_tests(){

    for file in $filename; do

        cmd="pytest -v -rpfs -s --random-order-bucket=class ${file}"
        # append function name to files.
        if ! [ -z "${funcname}" ]; then
            full_test_path="${file}::${funcname}"
            cmd="${cmd} -k '${funcname}'"
        fi

        eval "${cmd}"

    done

    exit 0;
}

run_all_tests() {
    # run all tests of the format test_*.py or *_test.py and are not marked 'conditional'
    pytest -v -rpfs -s ${test_dir} --random-order-bucket=class
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

set_test_level() {
    level=""
    if [ "${run_all}" = true ]; then
        level="unconditional"
    else
        level="all"
    fi
    export TEST_LEVEL=${level}
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

# set test level based on passed params
set_test_level

if [ "${run_all}" = true ]; then
    run_all_tests
elif [ -z "${filename}" ]; then
    echo -e "No file specified \n" && usage
else
    find_file
fi

