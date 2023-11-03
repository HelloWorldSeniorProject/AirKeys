# Provides a series of useful functions for use within the Software Test Environment.

import os, logging, json
from textwrap import wrap
import pandas as pd


# Globals
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
LOG_FILE = os.path.join(TEMP_DIR, "test_logs.log")
TEMP_MAP_FILE = os.path.join(TEMP_DIR, "temp_req-test_map.json")
DOCUMENTATION_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "documentation", "code")
REPORT_FILE = os.path.join(DOCUMENTATION_DIR, "TestReport.txt")
REQUIREMENTS_FILE = os.path.join(DOCUMENTATION_DIR, "Requirements.csv")

logger = logging.getLogger(__name__)
max_line_length = 70
divider = "-" * max_line_length
mapped_requirements = {"unique_requirements_tested" : []}
run_test = True


def truncate_str(string: str) -> list[str]:
    """Returns an array of strings truncated to an approximate size.

    Args:
        string: a string to be wrapped.
    """
    return wrap(string, max_line_length, break_long_words=False, break_on_hyphens=False)


def large_banner(string: str):
    """Prints a string in a divider seperated format with extra whitespace.

    Args:
        string: a string containing the desired text.
    """
    msg = truncate_str(string)

    # beginning space
    logger.info(f"{divider}")
    logger.info(f"")

    for s in msg:
        logger.info(f"- {s}")

    # end space
    logger.info(f"")
    logger.info(f"{divider}")


def small_banner(string: str):
    """Prints a string in a divider seperated format without extra whitespace.

    Args:
        string: a string containing the desired text.
    """
    msg = truncate_str(string)
    for s in msg:
        logger.info(f"{s}")


def conditional(test_func):
    """Run function only when specified.

    Note:
        When test functions are marked with this decorator, they will not run unless
        specificied using the test script. A commented reason should be included when using
        unless reason is obvious.
    """

    # forward all function parameters to test_func
    def wrapper(*args, **kwargs):
        
        global run_test
        run_test = True
        
        if os.environ["TEST_LEVEL"] != "all":
            run_test = False
        
        if (test_func.__name__  == "wrapper" or run_test):
            test_func(*args, **kwargs)
        else:
            logger.info(f"Skipped - {test_func.__name__}")
            run_test = True

    return wrapper

def requirements(*reqs):
    """Specify the requirement the test satisfies.

    Note:
        Used in test report generation.
    """
    
    def inner_func(test_func):
        
        # add test name to requirement map and save distinct requirement tested
        for req in reqs:
            if (mapped_requirements.get(req, None)):
                mapped_requirements[req].append(test_func.__name__)
            else:
                mapped_requirements[req] = [test_func.__name__]
            
            if req not in mapped_requirements["unique_requirements_tested"]:
                mapped_requirements["unique_requirements_tested"].append(req)
                
        # save data to file
        with open(TEMP_MAP_FILE, 'w') as f:
            json.dump(mapped_requirements, f, indent=4)
            
        def wrapper(*args, **kwargs):
            global run_test
            if run_test:
                test_func(*args, **kwargs)
            else:
                logger.info(f"Skipped - {test_func.__name__}")
            
            run_test = True
        return wrapper
    
    return inner_func
    

def compile_requirements_report():
    """Create Test to Requirement Mapping Report.
    """
    
    logger.info("Generating Requirements-to-Test Mapping")
    requirements = get_requirements()
    output = ""
    
    with open(TEMP_MAP_FILE, 'r') as f:
        mapped_requirements = json.load(f)
        
    title = "{:20}{:^}".format("Requirement #", "Test Cases\n")
    output+=title
    
    separator = "{}\n".format(("- "* 50))
    output += separator
    
    for key, value in mapped_requirements.items():
        prefix = key
        line = ' '.join(value)
        output += auto_wrap(line_to_wrap=line, prefix=prefix, padding_str=" "*20, per_line=80) + "\n"
        
    print(output)
    
def get_requirements():
    """Parses requirements file to 

    Returns:
        A pandas dataframe containing all the requirements, they're descriptions, and additional comments.
    """
    

    labels = ["Category", "Requirement", "Description","Comments"]

    # read in csv file
    df = pd.read_csv(REQUIREMENTS_FILE, skiprows=4, header=0, names=labels)

    # drop any rows where there is not a requirement # specified.
    df = df[df["Requirement"].notna()]

    # drop label rows
    df = df[df["Requirement"] != "Req #"]


    
def auto_wrap(line_to_wrap, prefix , padding_str, per_line):
    
    max_output = 117
    # reduce chars per line of wrapped line(s) if output will not fit on one line.
    if (len(padding_str)+len(prefix)+per_line > max_output):
        per_line =(max_output - len(padding_str) )

    words = line_to_wrap.split()
    formatted_words = []
    line = ""
        
    # go through each whole word and attempt to fit on current line; otherwise, add to next line.      
    for i in range(len(words)):
        word = words[i]

        # compare current line + word to line limit; account for spacing between words.
        if ((len(line) + len(word) + 1) <= per_line):

            # handle new word
            if(len(line) == 0):
                line = word
            else:
                line = line + ", " + word
        else: 
            formatted_words.append(line)
            line = word

        # handle case where len(line) < per_line and there are no more words.
        if (i == (len(words)-1)):
            formatted_words.append(line)
            
    # strip characters from back of padding str to accomadate prefix on first line. Print first line.
    first_pad = padding_str[:(-1 * len(prefix))] 
    formatted_str = '\n{}{}{:{per_line}}'.format(prefix, first_pad, formatted_words[0], per_line=per_line)
    
    # print remaining lines with proper spacing, if any.
    if(len(formatted_words)> 1):
        for remaining_line in formatted_words[1:]:
            formatted_str += '\n{}{:{per_line}}'.format(padding_str, remaining_line, per_line=per_line)
            
    return formatted_str