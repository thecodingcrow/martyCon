from utils_v2 import *
from tkinter import *

'''
DISCLAIMER

© ME 2021
All rights reserved

In case of malfunction contact author via eli23dex@gmail.com

version: 1.1


______________________________________________________________

TODO: Error handling
TODO: Indexing 
TODO: Custom Send REceive Texts

'''

'''
CONFIG SECTION - Parameters you need to adjust in order to get the script working properly
'''

dp_csv_filename = "all_dp_error.dpcsv"

number_of_abbs = 3
abbs = list()

test_abb_one = "UKG0001_TempAdjust"
test_abb_two = "RMC0001MWB"

# currently every line looks like that: first_DP:Send;sec_DP:Receive
dp_states = ['Send', 'Receive']

# currently the same index gets set for each line
index = "0x1000"

'''
VARIABLES SECTION - DO NOT TOUCH THESE UNLESS YOU ARE ELIGIBLE 
'''
# utils
dp_helper = DataPointsHelper()
paths_first_abb = list()
paths_sec_abb = list()
names_first_abb = list()
names_sec_abb = list()

# styling
lbl_font = ("Arial Bold", 14)
list_font = ('Arial Bold', 9)
entry_font = ('Arial Bold', 10)
dropd_font = ('Helvetica', 12)

# main window
root = Tk()
root.title('MartyCon')
root.geometry('1100x666')
'''
Event handling 
'''


def load_file():
    # read all data points from file
    dp_helper.get_datapoints_and_config_from_file(dp_csv_filename)
    print('File loaded')


def origin_state_listener(*args):
    update_origin_dp(origin_state.get())


def dest_state_listener(*args):
    update_dest_dp(dest_state.get())


def update_dest_dp(new_state):
    i = lst_dest.curselection()
    if len(i) is 0:
        print('You have to select a data point to change its state')
        return

    selected_dp = lst_dest.get(i)
    print(selected_dp)

    selected_dp = switch_state(new_state=new_state, dp=selected_dp)

    lst_dest.delete(i)
    lst_dest.insert(i, selected_dp)


def update_origin_dp(new_state):
    i = lst_origin.curselection()
    if len(i) is 0:
        print('You have to select a data point to change its state')
        return

    selected_dp = lst_origin.get(i)
    print(selected_dp)

    selected_dp = switch_state(new_state=new_state, dp=selected_dp)

    lst_origin.delete(i)
    lst_origin.insert(i, selected_dp)


def switch_state(new_state, dp):
    dp_start_index = dp.index('STATE') + 7

    curr_state = dp[dp_start_index:]
    print(f'dp state {curr_state}, new_state {new_state}')

    if new_state == curr_state:
        return dp
    elif new_state == dp_states[0] and curr_state == dp_states[1]:
        dp = dp.replace(curr_state, dp_states[0])
    elif new_state == dp_states[1] and curr_state == dp_states[0]:
        dp = dp.replace(curr_state, dp_states[1])

    curr_state = dp[dp_start_index:]
    print(f'dp state {curr_state}')

    return dp


def perform_search():
    global lst_origin
    global names_first_abb
    global paths_first_abb
    global names_sec_abb
    global paths_sec_abb

    abb_1 = txt_abb1.get()
    abb_2 = txt_abb2.get()

    found_dps_first_abb = dp_helper.get_dps_from_abb(abb_1)

    # retrieve parameters for found matches (abb_1)
    paths_first_abb = list()
    names_first_abb = list()
    for dp in found_dps_first_abb:
        paths_first_abb.append(get_path_from_dp(dp))
        names_first_abb.append(get_name_from_dp(dp))

    # just a bit of spacing for the sake of beauty
    print_spacer()

    # retrieve dps for second abb
    found_dps_second_abb = list()
    dp_with_no_match = list()

    for i, name in enumerate(names_first_abb):
        try:
            # for dp in dp_helper.get_dp_by_abb_with_same_name(name, abb_1, abb_2):
            #     found_dps_second_abb.append(dp)
            res = dp_helper.get_dp_by_abb_with_same_name(name, abb_1, abb_2)
            found_dps_second_abb.append(res)
        except:
            dp_with_no_match.append(name)
            del_dp_by_name(found_dps_first_abb, name)

    names_first_abb = list()
    paths_first_abb = list()
    for dp in found_dps_first_abb:
        paths_first_abb.append(get_path_from_dp(dp))
        names_first_abb.append(get_name_from_dp(dp))

    print(f'\nFound {len(names_first_abb)} possible connection origins:')
    print_list(names_first_abb, no_empty_elem=True)

    print_spacer()

    print(f'Connection Destination - data points that correspond to Names from {abb_1} and {abb_2}: Found {len(found_dps_second_abb)}')

    # retrieve parameters for found matches (abb_2)
    paths_sec_abb = list()
    names_sec_abb = list()
    for dp in found_dps_second_abb:
        paths_sec_abb.append(get_path_from_dp(dp))
        names_sec_abb.append(get_name_from_dp(dp))

    print(f'\nFound {len(paths_sec_abb)} Names:')
    print_list(names_sec_abb)

    print(f'Found {len(dp_with_no_match)} mismatches')
    print_list(dp_with_no_match, no_empty_elem=True)

    # another bit of spacing for the sake of beauty
    print_spacer()

    # check if length of to be connected lists match
    print_validity(found_dps_first_abb, found_dps_second_abb, 'origin data points')
    print_validity(names_first_abb, names_sec_abb, 'connection names')
    print_validity(paths_first_abb, paths_sec_abb, 'connection paths')

    lst_origin.delete(0, END)
    lst_dest.delete(0, END)

    for i, name in enumerate(names_first_abb):
        lst_name = name + ', STATE: ' + dp_states[0]
        lst_origin.insert(i, lst_name)

    for i, name in enumerate(names_sec_abb):
        lst_name = name + ', STATE: ' + dp_states[1]
        lst_dest.insert(i, lst_name)

    #
    # dp_conn = list()
    # for first_path, name, sec_path in zip(paths_first_abb, names_first_abb, paths_sec_abb):
    #     conn_string = get_connection_from_dps(conn_name=name, dest_path=sec_path, orig_path=first_path,
    #                                   index=index, first_text=first_text, second_text=second_text)
    #     dp_conn.append(conn_string)
    # # print result to file
    # # print_connection_to_file(dp_conn)
    #
    # # yet another bit of spacing for the sake of beauty
    # print_spacer()
    #
    # # success!
    # print(success_msg)

    print('Search performed')


def write_res_to_file():
    dp_conn = list()
    for first_path, name, sec_path in zip(paths_first_abb, names_first_abb, paths_sec_abb):
        first_text = get_state_from_origin_dp(names_first_abb.index(name))
        sec_text = get_state_from_dest_dp(names_first_abb.index(name))

        conn_string = get_connection_from_dps(conn_name=name, dest_path=sec_path, orig_path=first_path,
                                              index=index, first_text=first_text, second_text=sec_text)
        dp_conn.append(conn_string)

    # print result to file
    print_connection_to_file(dp_conn)

    print(success_msg)


def get_state_from_origin_dp(index):
    dp = lst_origin.get(index)
    dp_start_index = dp.index('STATE') + 7

    return dp[dp_start_index:]


def get_state_from_dest_dp(index):
    dp = lst_dest.get(index)
    dp_start_index = dp.index('STATE') + 7

    return dp[dp_start_index:]


'''
Init Interface
'''
lbl_file = Label(root, text='Select Files', font=lbl_font)
lbl_file.place(x=20, y=20)

btn_file = Button(root, text="Load File", command=load_file)
btn_file.place(x=20, y=40)

lbl_abb = Label(root, text='Enter abb', font=lbl_font)
lbl_abb.place(x=200, y=20)

txt_abb1 = Entry(root, width=10, font=entry_font)
txt_abb1.place(x=200, y=40)
txt_abb1.insert(END, test_abb_one)
txt_abb2 = Entry(root, width=10, font=entry_font)
txt_abb2.place(x=330, y=40)
txt_abb2.insert(END, test_abb_two)

btn_conn = Button(root, text="Search for Connections", command=perform_search)
btn_conn.place(x=200, y=70)

btn_write = Button(root, text="Write to file", command=write_res_to_file)
btn_write.place(x=390, y=70)

lst_origin = Listbox(root, font=list_font)
lst_origin.place(x=150, y=100, width=420, height=480)

lst_dest = Listbox(root, font=list_font)
lst_dest.place(x=600, y=100, width=420, height=480)

origin_state = StringVar(root)
origin_state.set(dp_states[0])

dest_state = StringVar(root)
dest_state.set(dp_states[0])

opt = OptionMenu(root, origin_state, *dp_states)
opt.config(font=dropd_font)
opt.place(x=20, y=80)


opt = OptionMenu(root, dest_state, *dp_states)
opt.config(font=dropd_font)
opt.place(x=20, y=180)

origin_state.trace('w', origin_state_listener)
dest_state.trace('w', dest_state_listener)

root.mainloop()

# # ______________________________________________________________________________________________________________________
# print_welcome_msg()
#

#
#
# # print all lines - debugging
# # print(all_dp_lines)
# # print_whole_file(filename=dp_csv_filename)
# # for line in all_dp_lines:
# #     print(type(line))
#
# retrieve occurrences of first abb
# found_dps_first_abb = dp_helper.get_dps_from_abb(test_abb_one)
# print(f'Connection Origins - data points that correspond to given abb: {test_abb_one}')
# print_list(found_dps_first_abb)
#
# # retrieve parameters for found matches (abb_1)
# paths_first_abb = list()
# names_first_abb = list()
# for dp in found_dps_first_abb:
#     paths_first_abb.append(get_path_from_dp(dp))
#     names_first_abb.append(get_name_from_dp(dp))
#
# print(f'\nFound {len(names_first_abb)} Names:')
# print_list(names_first_abb)
#
# # just a bit of spacing for the sake of beauty
# print_spacer()
#
# # retrieve second datapoint
# found_dps_second_abb = list()
# for name in names_first_abb:
#     found_dps_second_abb.append(dp_helper.get_dp_by_abb_with_same_name(name, test_abb_one, test_abb_two))
# print(f'Connection Destination - data points that correspond to {test_abb_two}')
# print_list(found_dps_second_abb)
#
# # retrieve parameters for found matches (abb_2)
# paths_second_abb = list()
# names_second_abb = list()
# for dp in found_dps_second_abb:
#     paths_second_abb.append(get_path_from_dp(dp))
#     names_second_abb.append(get_name_from_dp(dp))
#
# print(f'\nFound {len(paths_second_abb)} Names:')
# print_list(names_second_abb)
#
# # another bit of spacing for the sake of beauty
# print_spacer()
#
# # check if length of to be connected lists match
# print_validity(found_dps_first_abb, found_dps_second_abb, 'origin data points')
# print_validity(names_first_abb, names_second_abb, 'connection names')
# print_validity(paths_first_abb, paths_second_abb, 'connection paths')
#
#
# # create connection strings from found paths
# dp_conn = list()
# for first_path, name, sec_path in zip(paths_first_abb, names_first_abb, paths_second_abb):
#     dp_conn.append(get_connection_from_dps(conn_name=name, dest_path=sec_path, orig_path=first_path,
#                                   index=index, first_text=first_text, second_text=second_text))
#     # print result to file
#     print_connection_to_file(dp_conn)
#
# # yet another bit of spacing for the sake of beauty
# print_spacer()
#
# # success!
# print(success_msg)
