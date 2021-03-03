import re

TAB_DELIMITER = '\t'
SPACE_DELIMITER = ' '


def write2file(content, filename, overwrite = True):
    tag = "w" if overwrite else "a"
    f = open(filename, tag)
    f.write(content)
    f.write('\n')
    f.close()
    return

def split_line(line: str, re_expression = TAB_DELIMITER) -> []:
    pattern = re.compile(re_expression)
    return pattern.split(line.strip('\n'))


def get_line(filename, line_index:int = 0, delimiter = TAB_DELIMITER, split = True):
    if line_index < 0:
        return [] if split else ""
    f = open(filename, "r")
    cur_line_index = 0
    while cur_line_index < line_index:
        cur_line_index += 1
        f.readline()
    line = f.readline()
    f.close()
    return split_line(line, delimiter) if split else line


def get_header(filename, split = True) -> []:
    return get_line(filename, 0, split)

    
def get_column_index(filename, col_name) -> int:
    header = get_line(filename, 0)
    index = -1
    try:
        index = header.index(col_name)
    except:
        index = -1
    return index
    
    
def _check_col_index_or_name(col_index_or_name = None) -> int:
    if col_index_or_name is None:
        raise Error("should provide either index or name of a column")
    if type(col_index_or_name) not in [int, str]:
        raise Error("column info should be type of either integer or string")
    if type(col_index_or_name) in [str]:
        col_index = get_column_index(filename, col_index_or_name)
    else:
        col_index = col_index_or_name
    return col_index

    
def get_column(filename, col_index_or_name = None, include_header = False) -> []:
    
    col_index = _check_col_index_or_name(col_index_or_name)
    max_col_index = get_col_count(filename) - 1
    if col_index < 0 or col_index > max_col_index:
        raise Error("can not find that column")
    
    f = open(filename, "r")
    cols = []
    if not include_header:
        f.readline()
        
    while True:
        line = f.readline()
        if line == "": # EOF
            break
        else:
            contents = split_line(line)
            cols.append(contents[col_index])
    f.close()
    return cols


def get_column_fast(filename, col_index_or_name = None, include_header = False) -> []:
    col_index = _check_col_index_or_name(col_index_or_name)
    # TODO: add more data
    pass

def get_freq(contents: []):
    freq_dict = {}
    for c in contents:
        if c in freq_dict:
            freq_dict[c] += 1
        else:
            freq_dict[c] = 1
            
    return freq_dict
    
    
def get_info(content):
    if type(content) in [str]:
        columns = split_line(content, RE_DELIMITER)
    else:
        columns = content
    info = []
    info.append(("total count", len(columns)))
    min_len_column, max_len_column = "", ""
    min_len_index, max_len_index = None, None
    min_len, max_len = 999, 0
    for i, column in enumerate(columns):
        l = len(column)
        if l < min_len:
            min_len = l
            min_len_index = i
            min_len_column = column
        elif l > max_len:
            max_len = l
            max_len_column = column
            max_len_index = i            
                
    freq = get_freq(columns)        
    info.append(("different values", len(freq.keys())))
    info.append(("min len index", min_len_index))
    info.append(("min len", min_len))
    info.append(("min len value", min_len_column))
    info.append(("max len index", max_len_index))
    info.append(("max len", max_len))
    info.append(("max len value", max_len_column))   
    show(info)
    return

        
def header_info(filename, info = None):
    header = get_header(filename)
    columns = line_info(header, info)
    return columns

def get_line_count(filename) -> int:
    f = open(filename, "r")
    count = 0
    while True:
        s = f.readline() 
        if s != "":
            count += 1
        else:
            break
        
    f.close()
    return count


def get_col_count(filename) -> int:
    return len(get_line(filename, 0))


def check_columns(filename, target_col_num):
    f = open(filename, "r")
    while True:
        s = f.readline()
        if s == "":
            return True
        elif len(split_line(s)) not in [target_col_num]:
            return False
    
def show(info):
    for line in info:
        print("{}: {}".format(line[0], line[1]))





if __name__ == '__main__':
    log(True, "abcdefg", "arg2")