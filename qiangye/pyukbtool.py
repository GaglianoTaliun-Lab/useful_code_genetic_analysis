import sys
import re
import gzip
import argparse
import time
from util import TAB_DELIMITER, SPACE_DELIMITER
from util import get_line, split_line, get_column_index, get_line_count
from util import write2file
from progress import print_progress




module = __import__('__main__') # not use "pyukbtool"

argparser = argparse.ArgumentParser(description = "Basic analysis tools for UKBioBank")
argparser.add_argument('method_name', help = 'method name')
argparser.add_argument('input_filename', help = 'filename to analyze')
#argparser.add_argument('-i', '--input', metavar = 'filename', type = str,
#    dest = 'input_filename', required = True, help = 'filename to analyze')
argparser.add_argument('-f', '--datafields', metavar = 'string', type = str,
    dest = 'datafields', required = False, help = 'datafields joined by comma(,)')
argparser.add_argument('-d', '--delimiter', metavar = 'delimiter', 
    dest = 'delimiter', default = r'\t', required = False, 
    help = 'delimiter of the input filename')
argparser.add_argument('-v', dest = 'verbose', action = 'store_true', 
    help = 'output more detailed information')
argparser.add_argument('-c', '--count', metavar = 'count', type = int,
    dest = 'count', default = 10, help = 'number or rows that will be displayeded')
argparser.add_argument('-l', '--log', metavar = 'filename',  type = str,
    dest = 'log_filename', default = 'log.txt', help = 'log file')
argparser.add_argument('-o', '--output', metavar = 'filename',  type = str,
    dest = 'output_filename', help = 'filename to output')

verbose, log_filename = False, None

def log(*infos):
    if verbose:
        print(*infos)
    if log_filename is not None:
        if type(infos) in [list, tuple]:
            content = "\t".join(infos)
        elif type(infos) in [str]:
            content = infos
        else:
            content = str(infos)
        write2file(content, log_filename, overwrite = False)


def _header(args):
    filename = args.input_filename
    delimiter = args.delimiter
    output = args.output_filename
    header(filename, delimiter, output)
    pass

def header(filename, delimiter, output = None, split = True):
    '''
    get names of all columns of a file
    '''
    header = get_line(filename, 0, delimiter, split)
    header_str = "\t".join(header)
    log("{} columns: {}".format(len(header), header_str))
    if output is not None:
        try:
            header_str = "\t".join(header)
            write2file(header_str, output)
            log("header saved to {}".format(output))
        except:
            log("error in writing to file")
    
    pass


def _head(args):
    filename = args.input_filename
    count = args.count
    head(filename, count)
    pass

def head(filename, count):
    pass

def _col_index(args):
    pass

def col_index(filename, datafield_id):
    log("in method get_col_index")
    pass


def _filter_one_row(line: str, sorted_indices: list, delimiter = TAB_DELIMITER) -> str:
    if line == "\n" or line is None:
        return line
    line += delimiter
    result = ""
    start, end = 0, 0
    num_delimiter_passed = 0
    cur_index = 0
    for i, char in enumerate(line):
        if char == delimiter:
            end = i
            num_delimiter_passed += 1
            if num_delimiter_passed-1 == sorted_indices[cur_index]:
                if result == "":
                    result += line[start: end]
                else:
                    result += delimiter + line[start: end]
                cur_index += 1
                if cur_index >= len(sorted_indices):
                    break

            start = i+1
    return result + "\n"


def _parse_datafields(datafields: str) -> list:
    # accepted datafields:
    # "eid, 23, 22001.0.0, 22009.0.1-10"
    # the datafields is a string seperatd by semicolon(";"), comma(","), 
    # comma with a space(", "), and multiple consecutive spaces(" ", "   ", etc)
    # a datafield name can be "f.eid", "f.nnn.n.n"
    df_list = re.split(';|,|, | +', datafields)
    p_eid = re.compile(r'^(f\.)?eid$')
    p_main = re.compile(r'^[0-9]+$')
    p_main_minor = re.compile(r'^[0-9]+\.[0-9]+$')
    p_main_minors = re.compile(r'^[0-9]+\.[0-9]+-[0-9]+$')
    p_main_minor_mini = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$')
    p_main_minor_minis = re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+-[0-9]+$')
    result = []
    prefix = "f."
    for df in df_list:
        if p_eid.match(df):
            result.append("f.eid")
        elif p_main.match(df) or p_main_minor.match(df):
            # put "." at the end to prevent unexpectd mismatching
            # since later search use contains not exact match
            # ex. f.31 may match both f.31.0.0 and f.3100.0.0
            # if there is a "." at the end, then f.31. will only match f.31.0.0,
            # which is expected.
            result.append(prefix + df + ".")  
        elif p_main_minor_mini.match(df):
            result.append(prefix + df)
        elif p_main_minors.match(df):
            nums = re.split(r'\.', df)
            main, minors = nums[0], re.split(r'-', nums[1])
            start, end = int(minors[0]), int(minors[1])
            for i in range(start, end+1):
                new_df = prefix + main + "." + str(i) + "."
                result.append(new_df)
        elif p_main_minor_minis.match(df):
            nums = re.split(r'\.', df)
            main, minor, minis = nums[0], nums[1], re.split(r'-', nums[2])
            start, end = int(minis[0]), int(minis[1])
            for i in range(start, end+1):
                new_df = prefix + main + "." + minor + "." + str(i)
                result.append(new_df)
        else:
            pass

    return result


def _get_indices(header: list, parsed_datafields: list) -> list:
    #df_list = re.split(';|,|, | +', datafields)
    indices_set = set()
    p_main_minor_mini = re.compile(r'^f\.[0-9]+\.[0-9]+\.[0-9]+$')
    for i, col_name in enumerate(header):
        for df in parsed_datafields:
            need_full_match = (p_main_minor_mini.match(df) is not None)
            if need_full_match and df == col_name: 
                print("match! {} -- {}".format(df, col_name))
                # if df is like "f.major.minor.mini", we need df strictly equal col_name
                indices_set.add(i)
            elif (not need_full_match) and df in col_name:
                # if df not like "f.major.minor.mini", don't need strictly equal
                indices_set.add(i)
    
    result = list(indices_set)
    result.sort()
    #print("result: {}".format(result))
    # force to add eid column
    #if len(result) > 0 and result[0] != 0:
    #    result.insert(0, 0)

    return result


def _filter_col(args):
    filename = args.input_filename
    output = args.output_filename
    datafields = args.datafields
    delimiter = args.delimiter
    log_filename = args.log_filename
    filter_col(filename, datafields, output, delimiter)
    if log_filename is not None:
        log("log file: {}".format(log_filename))
    pass

def filter_col(filename: str, datafields: str, output_filename = None, 
               delimiter = TAB_DELIMITER):
    '''filter
    '''
    log("use delimiter: {}".format(delimiter))
    log("getting line count...")
    line_count = get_line_count(filename)
    log("got {} samples(indivisuals, rows)".format(line_count))
    log("getting header info...")
    header = get_line(filename, 0) # list of column names
    log("got header with {} columns".format(len(header)))
    log("parsing datafields: {}".format(datafields))
    parsed_datafields = _parse_datafields(datafields)
    log("got {} parsed_datafields:{}".format(len(parsed_datafields), parsed_datafields))
    log("analyzing indices of parsed datafields...")
    indices = _get_indices(header, parsed_datafields)
    log("got {} sorted indices: {}".format(len(indices), indices))
    log("starting filtering datafields...")
    f_read = open(filename, "r")
    f_write = None
    if output_filename is not None:
        f_write = open(output_filename, "w")
    lines_read = 0

    start = time.time()
    estimated_interval = int(line_count // 100)
    for i in range(line_count): 
        line = f_read.readline()
        lines_read += 1
        if line == "":# or lines_read == 2: #EOF
            break
        else:
            filtered_data = _filter_one_row(line, indices, delimiter = TAB_DELIMITER)
            f_write.write(filtered_data)
        if i % estimated_interval == 0 or i == line_count -1:
            print_progress(i/(line_count-1), time.time()-start)

    f_read.close()
    f_write.close()
    log("\ncompleted filtering datafields.")
    if output_filename is not None:
        log("output file: {}".format(output_filename))
    pass


def _brief_info(args):
    pass

def brief_info(args):
    log("in get basic info")
    pass


def _row_count(args):
    pass

def row_count(args):
    log("in get row count")
    pass


def _col_count(args):
    pass

def col_count(args):
    log("in get col count")
    pass



if __name__ == '__main__':
    args = argparser.parse_args()
    verbose = args.verbose
    log_filename = args.log_filename
    print("verbose: ", verbose)
    methods = dir(module)
    if args.method_name in methods:
        private_method_name = "_" + args.method_name
        method = getattr(module, private_method_name)
        method(args)
        print("Done.")
    else:
        print("{} doesn't exists.".format(args.method_name))
