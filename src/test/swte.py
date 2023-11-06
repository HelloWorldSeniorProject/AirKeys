# Provides a series of useful functions for use within the Software Test Environment.

import os, logging, json
from textwrap import wrap
import pandas as pd


# Globals
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
LOG_FILE = os.path.join(TEMP_DIR, "test_logs.log")
TEMP_MAP_FILE = os.path.join(TEMP_DIR, "temp_req-test_map.json")
DOCUMENTATION_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "documentation", "code"
)
REPORT_FILE = os.path.join(DOCUMENTATION_DIR, "TestReport.txt")
REQUIREMENTS_FILE = os.path.join(DOCUMENTATION_DIR, "Requirements.csv")

logger = logging.getLogger(__name__)
max_line_length = 70
divider = "-" * max_line_length
mapped_requirements = {}
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

        if test_func.__name__ == "wrapper" or run_test:
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
            if mapped_requirements.get(req, None):
                mapped_requirements[req].append(test_func.__qualname__)
            else:
                mapped_requirements[req] = [test_func.__qualname__]

        # save data to file
        with open(TEMP_MAP_FILE, "w") as f:
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
    """Create Test to Requirement Mapping Report."""

    logger.info("Generating Requirements-to-Test Mapping")

    # constants
    per_line = 80

    separator = "{}\n".format(("- " * 50))

    requirements, _ = _get_requirements()
    output = ""

    # retreive test-requirement mappings as specified in test enviornment.
    with open(TEMP_MAP_FILE, "r") as f:
        mapped_requirements = json.load(f)

    # add requirements satisfied through standard modules, external modules, or hardware (i.e. unnecessary tests).
    satisfied = {
        1.2: "Satisfied by hardware",
        1.3: "Satisfied by hardware",
        7.1: "Satisfied by hardware",
        8.1: "Satisfied by hardware",
        15.3: "Satisfied by visual inspection of functionality provided through standard module",
        15.4: "Satisfied by visual inspection of functionality provided through standard module",
        15.5: "Satisfied by visual inspection of functionality provided through standard module",
        16.1: "Satisfied by hardware",
    }
    for key, value in satisfied.items():
        mapped_requirements[str(key)] = value

    # calculate coverage stats
    reqs_needed = requirements["Requirement"].values.tolist()
    coverage = {
        "covered": mapped_requirements.keys(),
        "needed": [req for req in reqs_needed if req not in mapped_requirements.keys()],
    }
    stats = {
        "Requirement Coverage (%)": f"{round((len(coverage['covered'])/ len(reqs_needed))*100,2)}%",
        "Number of Requirements Covered": f"{len(coverage['covered'])}",
        "Number of Remaining Requirements": f"{len(coverage['needed'])}",
    }

    # format requirement coverage stats.
    title = "{:^100}\n\n".format("Coverage Stats")
    table_heading = "{:40}{:^}\n".format("Description", "Statistic")
    output += title
    output += separator
    for desc, stat in stats.items():
        output += (
            _auto_wrap(line_to_wrap=stat, prefix=desc, padding_str=" " * 40, per_line=per_line)
            + "\n"
        )
    output += "\n\n"

    # format test-requirement mapping.
    title = "{:^100}\n\n".format("Requirement-to-Test Mapping")
    table_heading = "{:20}{:^}\n".format("Requirement #", "Test Cases")
    output += title
    output += table_heading
    output += separator
    for req, justification in mapped_requirements.items():
        line = " ".join(justification) if type(justification) == list else justification
        output += (
            _auto_wrap(line_to_wrap=line, prefix=req, padding_str=" " * 20, per_line=per_line)
            + "\n"
        )
    output += "\n\n"

    # format remaining requirements.
    title = "{:^100}\n\n".format("Remaining Requirements")
    table_heading = "{:20}{:^}\n".format("Requirement #", "Description")
    output += title
    output += table_heading
    output += separator
    for req, desc in _get_requirement_descriptions(requirements, coverage["needed"]).items():
        output += (
            _auto_wrap(line_to_wrap=desc, prefix=req, padding_str=" " * 20, per_line=per_line)
            + "\n"
        )
    output += "\n\n"

    # save report to file.
    with open(REPORT_FILE, "w") as f:
        f.write(output)


def _get_requirements() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parses requirements file into two dataframes.

    Returns:
        Two pandas dataframes containing all the requirements, they're descriptions, and additional comments. The first data frame
        contains the essentials requirements while the second dataframe contains the optional requirements.
        
    Notes:
        Expects CSV file in `documentation/code` named `Requirements.csv`. File can be split into two sections as shown in
        here : https://docs.google.com/spreadsheets/d/1KDWr5lpKnlF1U20N45R3keTzLomTzltnJHnH2cv9Ryc/edit?usp=sharing.
        The delimiter "Req #" (1st match ignored) must be located in the Requirement # column.
    """
    # labels as defined in requirements spreadsheet.
    labels = ["Category", "Requirement", "Description", "Comments"]

    # read in csv file.
    df = pd.read_csv(REQUIREMENTS_FILE, skiprows=4, header=0, names=labels)

    # drop any rows where there is not a requirement # specified.
    df = df[df["Requirement"].notna()]

    # split data frame based on "Essential" vs "As Time Allows" requirements
    split = df.index.get_loc(df.loc[df["Requirement"].str.contains("Req #", na=False)].index[0])
    required = df.iloc[:split]
    as_time_allows = df.iloc[split + 1 :]

    return (required, as_time_allows)


def _get_requirement_descriptions(df: pd.DataFrame, reqs: list[str]) -> dict[str, str]:
    """Retrieves the descriptions of specified requirements.

    Args:
        df: The dataframe the requirements can be found in.
        reqs: The list of requirements to search for.
    Returns:
        A dictionary containing the each specified requirement and its description.
    """

    # retreive rows based on requirement.
    temp = df.loc[df["Requirement"].isin(reqs)]

    return pd.Series(temp["Description"].values, index=temp["Requirement"]).to_dict()


def _auto_wrap(line_to_wrap, prefix, padding_str, per_line):
    max_output = 117
    # reduce chars per line of wrapped line(s) if output will not fit on one line.
    if len(padding_str) + len(prefix) + per_line > max_output:
        per_line = max_output - len(padding_str)

    words = line_to_wrap.split()
    formatted_words = []
    line = ""

    # go through each whole word and attempt to fit on current line; otherwise, add to next line.
    for i in range(len(words)):
        word = words[i]

        # compare current line + word to line limit; account for spacing between words.
        if (len(line) + len(word) + 1) <= per_line:
            # handle new word
            if len(line) == 0:
                line = word
            else:
                # place commas between function names and spaces between regular words.
                line = line + (", " if "_" in word else " ") + word
        else:
            formatted_words.append(line)
            line = word

        # handle case where len(line) < per_line and there are no more words.
        if i == (len(words) - 1):
            formatted_words.append(line)

    # strip characters from back of padding str to accomadate prefix on first line. Print first line.
    first_pad = padding_str[: (-1 * len(prefix))]
    formatted_str = "\n{}{}{:{per_line}}".format(
        prefix, first_pad, formatted_words[0], per_line=per_line
    )

    # print remaining lines with proper spacing, if any.
    if len(formatted_words) > 1:
        for remaining_line in formatted_words[1:]:
            formatted_str += "\n{}{:{per_line}}".format(
                padding_str, remaining_line, per_line=per_line
            )

    return formatted_str
