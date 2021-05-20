import os
from datapoint import Datapoint
from pprint import pprint
import re

'''
DISCLAIMER

© ME 2021 All rights reserved

In case of malfunction contact author via eli23dex@gmail.com

Internal version: 2.3
Release version: 2

______________________________________________________________
'''

'''
INTERNAL CONFIG SECTION - DO NOT MODIFY THESE UNLESS YOU KNOW WHAT YOU ARE DOING
'''
# terminal messages
start_msg = r"Hi, I'm Marty!"

# file-specific config
delimiter = ";"
newline = "\n"
dp_file_header_start_char = '#'
start_char_utf16 = r'\ufeff'
file_encoding = 'utf-8-sig'

# resources
res_dir = "res"

# result
output_dir = "out"

# utils
base_regex = r"(\d{1,2})?$"

# logging
INFO = '[INFO]'
ERROR = '[ERROR]'
FATAL = '[FATAL]'

# versioning
version = 2

# schema of resulting csv
# header
# ID;ConnectionName;ConnectionDescription;TargetDPName
result_header = "#connection_csv_ver;3" + \
                newline + \
                "#ID;ConnectionName;ConnectionDescription;TargetDPName" + \
                newline


def print_welcome_msg():
    char = '*'
    num_chars = 18
    print(char * num_chars)
    print(char + ' ' + start_msg + ' ' + char)
    print(f'You are running version {version}')
    print(char * num_chars)


def print_connection_to_file(conn_result, output_filename):
    print('\n' * 1)
    print('*' * 10, ' PRINT CONNECTION STRINGS START ', '*' * 10)
    print('\n' * 2)

    with open(os.path.join(output_dir, output_filename), 'w+') as out_file:
        if os.stat(os.path.join(output_dir, output_filename)).st_size == 0:
            out_file.write(result_header)
            print(f'{INFO} Wrote file header: {result_header}')
        for line in conn_result:
            out_file.write(line)
            print(f'{INFO} Wrote line: {line}')

    print('\n' * 1)
    print('*' * 10, ' PRINT CONNECTION STRINGS END ', '*' * 10)
    print('\n' * 2)


def get_name_from_dp(datapoint):
    if datapoint and len(datapoint) >= 3:
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


def validate_lists(list_one, list_two, scope):
    is_valid = __validate_found_matches(list_one, list_two)
    if not is_valid:
        return f'{FATAL} Invalid matching detected, {len(list_one)} sources but {len(list_two)} destinations'
    return (
            f'{INFO if is_valid else ERROR} The {len(list_one)} found {scope} have {len(list_two)} matches and are therefore ' +
            f'{"valid" if is_valid else "invalid"}')


def map_file_header(header_param):
    if header_param == 'UID':
        return 'uid'
    elif header_param == 'IdPath':
        return 'id_path'
    elif header_param == 'Name':
        return 'name'
    elif header_param == 'Description':
        return 'description'
    elif header_param == 'SrvObj Name':
        return 'server_object_name'
    elif header_param == 'Obj Description':
        return 'object_description'
    elif header_param == 'COV Increment':
        return 'cov_increment'
    elif header_param == 'Obj Type':
        return 'object_type'
    elif header_param == 'Obj Inst':
        return 'object_instance'
    elif header_param == 'CliMap Inst\n':
        return 'cli_map_instance'

    raise InvalidHeaderException(f"{FATAL} Invalid parameter found {header_param}")


def get_regex_from_abb(abb):
    return abb + base_regex


class FileHelper:
    header = ""
    data_points = list()

    __all_dp_lines = list()
    __config_lines = list()

    def __init__(self):
        self.data_points = DictWrapper(self.data_points)
        pass

    def read_data_points_and_header_from_file(self, filename):
        with open(os.path.join(res_dir, filename), encoding=file_encoding, mode='r+') as dp_file:
            for line in dp_file.readlines():
                if not line.startswith(dp_file_header_start_char) and not line.startswith(start_char_utf16):
                    self.__all_dp_lines.append(line)
                else:
                    self.__config_lines.append(line)

        try:
            self.header = self.__read_header()
        except InvalidHeaderException as invalidHeader:
            print(invalidHeader)

        self.data_points = self.__read_data_points()

        return self.header, self.data_points

    def __read_header(self):
        header = self.__config_lines[-1].replace('#', '')

        print('\n' * 1)
        print('*' * 10, ' HEADER READ START ', '*' * 10)
        print('\n' * 2)

        if len(header.split(delimiter)) == 10:
            print(header.split(delimiter))
            print('\n' * 1)
            print('*' * 10, ' HEADER READ END ', '*' * 10)
            print('\n' * 2)

            return header.split(delimiter)
        else:
            print('\n' * 1)
            print('*' * 10, ' HEADER READ FAILED ', '*' * 10)
            print('\n' * 2)

            raise InvalidHeaderException(f'{FATAL} Invalid Header found')

    def __read_data_points(self):
        found_data_points = list()

        print('\n' * 1)
        print('*' * 10, ' DATAPOINT READ START ', '*' * 10)
        print('\n' * 2)

        for line in self.__all_dp_lines:
            try:
                dp = self.__extract_data_point(line=line)
                found_data_points.append(dp)
            except InvalidHeaderException as invalidHeader:
                print('\n' * 1)
                print('*' * 10, ' HEADER READ FAILED ', '*' * 10)
                print('\n' * 2)

                print(invalidHeader)

        print('\n' * 1)
        print('*' * 10, ' DATAPOINT READ END ', '*' * 10)
        print('\n' * 2)

        return found_data_points

    def __extract_data_point(self, line):
        line_params = line.split(delimiter)
        params = {}

        for key, value in zip(self.header, line_params):

            key = map_file_header(key)
            if '\n' in value:
                value.replace('\n', '')
            params[key] = value

        dp = Datapoint(params)
        print(f'{len(params)} params read for data point {dp.uid}')

        return dp

    def find_source_data_points_by_abb(self, abb):
        matches = list()

        print('\n' * 1)
        print('*' * 10, ' SOURCE DATA POINT SEARCH START ', '*' * 10)
        print('\n' * 2)

        for dp in self.data_points:
            pattern = get_regex_from_abb(abb)
            re.compile(pattern=pattern)
            if re.search(pattern, dp.name):
                matches.append(dp)

        if len(matches) >= 1:
            print(f"Found {len(matches)} matches for abb: {abb} \n")
            pprint(matches)
        elif len(matches) < 1:
            raise Exception("No datapoint found!")

        print('\n' * 1)
        print('*' * 10, ' SOURCE DATA POINT SEARCH END ', '*' * 10)
        print('\n' * 2)

        return matches

    def find_destination_data_points_to_source(self, source_dp, source_abb, dest_abb):
        matches = list()

        print('-' * 135)

        if source_abb in source_dp.name:
            destination = source_dp.name.replace(source_abb, dest_abb)
        else:
            raise InvalidCombinationException(f"Wrong combination! {source_abb} not in {source_dp.name}")

        print(f'Query:\n For dp {source_dp} find destination(s) {destination}')

        for dp in self.data_points:
            if re.search(get_regex_from_abb(destination), dp.name):
                matches.append(dp)

        if len(matches) >= 1:
            print('\n')
            print(f"Found {len(matches)} destination data points for source {destination}")
            pprint(matches)
            print('-' * 135)
            print('\n' * 2)
        elif len(matches) < 1:
            raise NoMatchFoundException(f"No datapoint found for {destination}")

        return [source_dp] + matches


class DictWrapper(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class InvalidCombinationException(Exception):
    pass


class NoMatchFoundException(Exception):
    pass


class InvalidHeaderException(Exception):
    pass
