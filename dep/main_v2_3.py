from utils_v2_2 import *
from tkinter import *

'''
DISCLAIMER

© ME 2021 All rights reserved

In case of malfunction contact author via eli23dex@gmail.com

Internal version: 2.3
Release version: 1

______________________________________________________________


'''

'''
CONFIG SECTION - Parameters you need to adjust in order to get the script working properly
'''
# input file
dp_csv_filename = "lgateCfgV03.dpcsv"

# out file
output_filename = "result.csv"

test_abb_one = "RMC0001MWB"
test_abb_two = "UKG0001_TempAdjust"

dp_states = ['Send', 'Receive']
first_text = dp_states[0]
sec_text = dp_states[1]

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
last_log = 0

files_loaded = False

# styling
lbl_font = ("Arial Bold", 10)
list_font = ('Arial Bold', 9)
entry_font = ('Arial Bold', 10)
dropd_font = ('Helvetica', 10)
error_font = ('Arial Bold', 12)

# main window
root = Tk()
root.title('MartyCon')
root.geometry('1200x800')
'''
Event handling 
'''


def log(text):
    global last_log

    lst_log.insert(last_log, text)
    lst_log.yview(END)
    last_log += 1


def reset_error():
    lbl_error.configure(text='')


def load_file():
    global files_loaded

    reset_error()

    # read all data points from file
    if not os.path.exists(os.path.join(res_dir, dp_csv_filename)):
        lbl_error.configure(text=f'{ERROR} Invalid filename specified!')
        return

    dp_helper.get_datapoints_and_config_from_file(dp_csv_filename)
    files_loaded = True
    log(f'{INFO} File loaded successfully')


def perform_search():
    global files_loaded
    global lst_origin
    global names_first_abb
    global paths_first_abb
    global names_sec_abb
    global paths_sec_abb
    global output_filename

    reset_error()

    if not files_loaded:
        lbl_error.configure(text='You have to load a file before starting a search!')
        return

    abb_1 = txt_abb1.get()
    abb_2 = txt_abb2.get()

    if abb_1 == '' or abb_2 == '' or abb_1 == abb_2:
        lbl_error.configure(text='You have to specify two different abbreviations!')
        return

    output_filename = 'Conn_' + abb_1 + '__' + abb_2 + '.csv'

    log(f'{INFO} New filename specified: {output_filename}')

    found_dps_first_abb = dp_helper.get_dps_from_abb(abb_1)

    # retrieve parameters for found matches (abb_1)
    paths_first_abb = list()
    names_first_abb = list()
    for dp in found_dps_first_abb:
        paths_first_abb.append(get_path_from_dp(dp))
        names_first_abb.append(get_name_from_dp(dp))

    # retrieve dps for second abb
    found_dps_second_abb = list()
    dp_with_no_match = list()

    for i, name in enumerate(names_first_abb):
        try:
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

    log(f'{INFO} Connection Sources - {len(names_first_abb)} possible connection sources')

    log(f'{INFO} Connection Destination - data points that correspond to Names from {abb_1} and {abb_2}: Found {len(found_dps_second_abb)}')

    # retrieve parameters for found matches (abb_2)
    paths_sec_abb = list()
    names_sec_abb = list()
    for dp in found_dps_second_abb:
        paths_sec_abb.append(get_path_from_dp(dp))
        names_sec_abb.append(get_name_from_dp(dp))

    log(f'{INFO} Found {len(paths_sec_abb)} Names')

    log(f'{INFO} Found {len(dp_with_no_match)} mismatches')

    # check if length of to be connected lists match
    log(validate_lists(found_dps_first_abb, found_dps_second_abb, 'origin data points'))
    log(validate_lists(names_first_abb, names_sec_abb, 'connection names'))
    log(validate_lists(paths_first_abb, paths_sec_abb, 'connection paths'))

    lst_origin.delete(0, END)
    lst_dest.delete(0, END)

    for i, name in enumerate(names_first_abb):
        lst_name = name + ', STATE: ' + dp_states[0]
        lst_origin.insert(i, lst_name)

    for i, name in enumerate(names_sec_abb):
        lst_name = name + ', STATE: ' + dp_states[1]
        lst_dest.insert(i, lst_name)

    log(f'{INFO} Search performed')


def write_res_to_file():
    reset_error()

    dp_conn = list()
    for first_path, name, sec_path in zip(paths_first_abb, names_first_abb, paths_sec_abb):
        conn_string = get_connection_from_dps(conn_name=name, dest_path=sec_path, orig_path=first_path,
                                              index=index, first_text=sec_text, second_text=first_text)
        dp_conn.append(conn_string)

    # print result to file
    print_connection_to_file(dp_conn, output_filename)

    log(f'{INFO} successfully wrote {len(dp_conn)} connection strings to {output_filename}')

'''
Init Interface
'''
btn_file = Button(root, text="Load File", command=load_file)
btn_file.place(x=80, y=60)

lbl_abb = Label(root, text='Source abb:', font=lbl_font)
lbl_abb2 = Label(root, text='Destination abb:', font=lbl_font)

lbl_abb.place(x=205, y=60)
lbl_abb2.place(x=650, y=60)

txt_abb1 = Entry(root, width=47, font=entry_font)
txt_abb1.place(x=285, y=60)
txt_abb1.insert(END, test_abb_one)

txt_abb2 = Entry(root, width=43, font=entry_font)
txt_abb2.place(x=765, y=60)
txt_abb2.insert(END, test_abb_two)

btn_conn = Button(root, text="Search", command=perform_search)
btn_conn.place(x=80, y=100)

btn_write = Button(root, text="Write File", command=write_res_to_file)
btn_write.place(x=80, y=600)

lst_origin = Listbox(root, font=list_font)
lst_origin.place(x=200, y=100, width=420, height=480)

lst_dest = Listbox(root, font=list_font)
lst_dest.place(x=650, y=100, width=420, height=480)

lbl_error = Label(root, font=error_font, width=50)
lbl_error.place(x=202, y=700)

lst_log = Listbox(root, font=list_font)
lst_log.place(x=200, y=600, width=873, height=90)

root.mainloop()
