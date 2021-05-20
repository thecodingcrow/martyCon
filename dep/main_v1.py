from utils_v1 import *
# from PySide6 import QtCore, QtWidgets, QtGui

'''
DISCLAIMER

© ME 2021
All rights reserved

In case of malfunction contact author via eli23dex@gmail.com
'''


'''
CONFIG SECTION - Parameters you need to adjust in order to get the script working properly
'''
number_of_abbs = 3
abbs = list()

test_abb_one = "RAU001BEL0001RM_"
test_abb_two = "RAU001BEL0002RM_"
test_abb_three = ""

first_text = "Receive"
second_text = "Send"

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

    # retrieve first datapoint
    first_dp = dp_helper.get_dp_by_abb(test_abb_one)
    print('First Datapoint - Connection Origin')
    print(first_dp)

    # get parameters for first datapoint
    first_dp_name = get_name_from_dp(first_dp)
    print('Name: ' + first_dp_name)
    first_dp_path = get_path_from_dp(first_dp)
    print('Path: ' + first_dp_path)

    # just a bit of spacing for the sake of beauty
    print_spacer()

    # retrieve second datapoint
    second_dp = dp_helper.get_dp_by_abb_with_same_name(first_dp_name, test_abb_one, test_abb_two)
    print('Second Datapoint - Connection Destination')
    print(second_dp)

    # retrieve parameters for second datapoint
    second_dp_path = get_path_from_dp(second_dp)
    print('Path: ' + second_dp_path)

    # create connection string from found paths
    dp_conn = get_connection_from_dps(dest_path=second_dp_path, orig_path=first_dp_path,
                                      index=index, first_text=first_text, second_text=second_text)

    # print result to file
    print_connection_to_file(dp_conn)

    # another bit of spacing for the sake of beauty
    print_spacer()

    # success!
    print(success_msg)
