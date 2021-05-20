from utils_v1_1 import *
# from PySide6 import QtCore, QtWidgets, QtGui
from pprint import pprint
'''
DISCLAIMER

© ME 2021
All rights reserved

In case of malfunction contact author via eli23dex@gmail.com

version: 1.1


______________________________________________________________

TODO: Error handling
TODO: adapt output for large lists
TODO: mehrere kürzel auf einmal eingeben + send/receive pro kürzel einstellen 
TODO: Indexing 
TODO: Custom Send REceive Texts

'''


'''
CONFIG SECTION - Parameters you need to adjust in order to get the script working properly
'''

dp_csv_filename = "all_datapoints_v_1.dpcsv"

number_of_abbs = 3
abbs = list()

test_abb_one = "UKG0001_TempAdjust"
test_abb_two = "RMC0001MWB"

# currently every line looks like first_DP:Send;sec_DP:Receive
first_text = "Receive"
second_text = "Send"

# currently the same index gets set for each line
index = "0x1000"


'''
VARIABLES SECTION - DO NOT TOUCH THESE UNLESS YOU ARE ELIGIBLE 
'''
all_dp_lines = list()
config_lines = list()

if __name__ == '__main__':
    print_welcome_msg()

    dp_helper = DataPointsHelper()

    # read all data points from file
    all_dp_lines, config_lines = dp_helper.get_datapoints_and_config_from_file(dp_csv_filename)

    # print all lines - debugging
    # print(all_dp_lines)
    # print_whole_file(filename=dp_csv_filename)

    # retrieve occurrences of first abb
    found_dps_first_abb = dp_helper.get_dps_from_abb(test_abb_one)
    print(f'Connection Origins - data points that correspond to given abb: {test_abb_one}')
    print_list(found_dps_first_abb)

    # retrieve parameters for found matches (abb_1)
    paths_first_abb = list()
    names_first_abb = list()
    for dp in found_dps_first_abb:
        paths_first_abb.append(get_path_from_dp(dp))
        names_first_abb.append(get_name_from_dp(dp))

    print(f'\nFound {len(names_first_abb)} Names:')
    print_list(names_first_abb)

    # just a bit of spacing for the sake of beauty
    print_spacer()

    # retrieve second datapoint
    found_dps_second_abb = list()
    for name in names_first_abb:
        found_dps_second_abb.append(dp_helper.get_dp_by_abb_with_same_name(name, test_abb_one, test_abb_two))
    print(f'Connection Destination - data points that correspond to {test_abb_two}')
    print_list(found_dps_second_abb)

    # retrieve parameters for found matches (abb_2)
    paths_second_abb = list()
    names_second_abb = list()
    for dp in found_dps_second_abb:
        paths_second_abb.append(get_path_from_dp(dp))
        names_second_abb.append(get_name_from_dp(dp))

    print(f'\nFound {len(paths_second_abb)} Names:')
    print_list(names_second_abb)

    # another bit of spacing for the sake of beauty
    print_spacer()

    # check if length of to be connected lists match
    print_validity(found_dps_first_abb, found_dps_second_abb, 'origin data points')
    print_validity(names_first_abb, names_second_abb, 'connection names')
    print_validity(paths_first_abb, paths_second_abb, 'connection paths')


    # create connection strings from found paths
    dp_conn = list()
    for first_path, name, sec_path in zip(paths_first_abb, names_first_abb, paths_second_abb):
        dp_conn.append(get_connection_from_dps(conn_name=name, dest_path=sec_path, orig_path=first_path,
                                      index=index, first_text=first_text, second_text=second_text))
        # print result to file
        print_connection_to_file(dp_conn)

    # yet another bit of spacing for the sake of beauty
    print_spacer()

    # success!
    print(success_msg)
