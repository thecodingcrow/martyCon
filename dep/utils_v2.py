import os
from pprint import pprint

'''
INTERNAL CONFIG SECTION - DO NOT MODIFY THESE UNLESS YOU KNOW WHAT YOU ARE DOING
'''
# terminal messages
start_msg = r"Hi, I'm Marty!"
success_msg = r"Successfully wrote connected datapoints to out_file!"

# file-specific config
dp_csv_filename = "all_datapoints.csv"
delimiter = ";"
newline = "\n"
dp_file_header_start_char = '#'
start_char_utf16 = r'\ufeff'
file_encoding = 'utf-8-sig'

# resources
res_dir = "res"

# result
output_dir = "out"
output_filename = "result.csv"

# schema of resulting csv
# header
# ID;ConnectionName;ConnectionDescription;TargetDPName
result_header = "#connection_csv_ver;3" + \
                newline + \
                "#ID;ConnectionName;ConnectionDescription;TargetDPName" + \
                newline


def print_spacer():
    print('\n' * 1)


def print_welcome_msg():
    char = '*'
    num_chars = 18
    print(char * num_chars)
    print(char + ' ' + start_msg + ' ' + char)
    print(char * num_chars)
    print_spacer()


def print_whole_file(filename):
    with open(os.path.join(res_dir, filename), mode='r+') as dp_file:
        for line in dp_file.readlines():
            print(line)


def print_connection_to_file(conn_result):
    with open(os.path.join(output_dir, output_filename), 'a+') as out_file:
        if os.stat(os.path.join(output_dir, output_filename)).st_size == 0:
            out_file.write(result_header)
        for line in conn_result:
         out_file.write(line)


def get_name_from_dp(datapoint):
    if datapoint and len(datapoint) >= 2:
        return datapoint[2]
    else:
        raise Exception(f"No name found for {datapoint}!")


def get_path_from_dp(datapoint):
    if datapoint and len(datapoint) >= 2:
        return datapoint[1]
    else:
        raise Exception(f"No path found for {datapoint}!")


def get_connection_from_dps(dest_path, orig_path, conn_name, index='', first_text='', second_text=''):
    return index + delimiter + \
           conn_name + delimiter + \
           dest_path + delimiter + \
           dest_path + delimiter + \
           first_text + delimiter * 2 + \
           orig_path + delimiter + \
           second_text + delimiter + \
           newline


def __validate_found_matches(matches_first_abb, matches_sec_abb):
    return len(matches_first_abb) == len(matches_sec_abb)


def print_validity(list_one, list_two, scope):
    is_valid = __validate_found_matches(list_one, list_two)
    if not is_valid:
        print(len(list_one))
        print(len(list_two))
        raise Exception("Invalid match found!")
    print(f'The {len(list_one)} found {scope} have {len(list_two)} matches and are therefore ' +
          f'{"valid" if is_valid else "invalid"}')


def print_list(data_points, no_empty_elem=False):
    for dp in data_points:
        if no_empty_elem:
            if len(dp) > 0 and dp is not None:
                print(dp)
        else:
            print(dp)


def del_dp_by_name(list_dp, name):
    for dp in list_dp:
        if get_name_from_dp(dp) is name:
            list_dp.remove(dp)
            return
    raise Exception("Couldn't delete data point")


class DataPointsHelper:
    all_dp_lines = list()
    config_lines = list()

    def __init__(self):
        pass

    def get_datapoints_and_config_from_file(self, filename):
        with open(os.path.join(res_dir, filename), encoding=file_encoding, mode='r+') as dp_file:
            for line in dp_file.readlines():
                if not line.startswith(dp_file_header_start_char) and not line.startswith(start_char_utf16):
                    self.all_dp_lines.append(line)
                else:
                    self.config_lines.append(line)
        return self.all_dp_lines, self.config_lines

    def get_dps_from_abb(self, abb, print_matches=False):
        raw_matches = list()
        response = list()
        for dp in self.all_dp_lines:
            if abb in dp:
                raw_matches.append(dp)

        if len(raw_matches) >= 1:
            print(f"Found {len(raw_matches)} matches for abb: {abb} \n")
            if print_matches:
                print(raw_matches)
            # raise Exception("Too many matches! Aborting...")
        elif len(raw_matches) < 1:
            raise Exception("No datapoint found!")

        for match in raw_matches:
            response.append(match.split(delimiter))

        return response

    def get_dp_by_abb_with_same_name(self, first_dp_name, first_abb, second_abb):
        matches = list()
        if first_abb in first_dp_name:
            first_dp_name = first_dp_name.replace(first_abb, second_abb)
        else:
            raise Exception("Wrong combination of first dp_name and abb! Aborting...")

        for dp in self.all_dp_lines:
            dp = dp.split(delimiter)
            if first_dp_name in get_name_from_dp(dp):
                matches.append(dp)
        if len(matches) < 1:
            raise Exception(f"No datapoint found for {first_dp_name}")
            # return f"No datapoint found for {first_dp_name}"
            pass
        elif len(matches) == 1:
            return matches[0]

        return matches
