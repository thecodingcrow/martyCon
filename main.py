from utils import *
from tkinter import *
'''
DISCLAIMER

© ME 2021 All rights reserved

In case of malfunction contact author via eli23dex@gmail.com

Internal version: 3.1
Release version: 2

______________________________________________________________
'''


'''
CONFIG SECTION - Parameters you need to adjust in order to get the script working properly
'''
# input file
dp_csv_filename = "bacDP.dpcsv"

# out file
output_filename = "result.csv"

# default search config
default_abb_one = "RMC0001MWB"
default_abb_two = "UKG0001_TempAdjust"

# default state config
dp_states = ['Receive', 'Send']

first_text = dp_states[0]
sec_text = dp_states[1]

# currently the same index gets set for each line
index = "0x1000"

'''
VARIABLES SECTION - DO NOT TOUCH THESE UNLESS YOU ARE ELIGIBLE 
'''
# utils
fileMan = FileHelper()

header = ''

# data point handling
all_data_points = list()
all_connections = list()

# logging
last_log = 0

# state
file_loaded = False

# styling
lbl_font = ("Arial Bold", 10)
list_font = ('Arial Bold', 9)
entry_font = ('Arial Bold', 10)
dropd_font = ('Helvetica', 10)
error_font = ('Arial Bold', 12)

# main window
root = Tk()
root.title(f'MartyCon v{version}')
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
    global file_loaded
    global all_data_points
    global header

    reset_error()

    # read all data points from file
    if not os.path.exists(os.path.join(res_dir, dp_csv_filename)):
        lbl_error.configure(text=f'{ERROR} Invalid filename specified!')
        return
    try:
        header, all_data_points = fileMan.read_data_points_and_header_from_file(dp_csv_filename)
    except Exception as e:
        print(f'{ERROR} Message: {e}')

    file_loaded = True
    log(f'{INFO} File {dp_csv_filename} loaded successfully')
    log(f'{INFO} Successfully extracted {len(all_data_points)} data points')


def perform_search():
    global file_loaded
    global lst_origin
    global output_filename
    global all_connections

    reset_error()

    if not file_loaded:
        lbl_error.configure(text='You have to load a file before starting a search!')
        return

    source_abb = txt_abb1.get()
    dest_abb = txt_abb2.get()

    if source_abb == '' or dest_abb == '' or source_abb == dest_abb:
        lbl_error.configure(text='You have to specify two different abbreviations!')
        return

    output_filename = 'Conn_' + source_abb + '__' + dest_abb + '.csv'

    log(f'{INFO} New filename specified: {output_filename}')

    source_data_points = fileMan.find_source_data_points_by_abb(source_abb)

    # retrieve connection lists for each data point
    connection_lists = list()
    unmatched_sources = list()

    print(len(source_data_points))

    for i, source_dp in enumerate(source_data_points):
        try:

            res = fileMan.find_destination_data_points_to_source(source_dp, source_abb, dest_abb)
            connection_lists.append(res)
        except InvalidCombinationException as invalid:
            log(f'{FATAL} {invalid}')
        except NoMatchFoundException as noMatch:
            log(f'{ERROR} {noMatch}')
            unmatched_sources.append(source_dp)

    for unmatched_dp in unmatched_sources:
        source_data_points.remove(unmatched_dp)

    # log search result and statistics
    log(f'{INFO} {len(source_data_points) + len(unmatched_sources)} possible connection sources were found')
    log(f'{INFO} {len(source_data_points)} suitable connection sources are displayed')
    log(f'{INFO} {sum([len(ls) - 1 for ls in connection_lists])} connection destinations were found')
    log(f'{INFO} Mean: {sum([len(dp) - 1 for dp in connection_lists]) / len(source_data_points):.2f} connections per source')

    for conn in connection_lists:
        source_dp = conn[0]
        for dest in conn[1:]:
            conn_string = get_connection_from_dps(conn_name=source_dp.name, dest_path=dest.id_path,
                                                  orig_path=source_dp.id_path, index=index, first_text=first_text,
                                                  second_text=sec_text)
            all_connections.append(conn_string)

    lst_origin.delete(0, END)
    lst_dest.delete(0, END)

    for i, source_dp in enumerate(source_data_points):
        lst_name = source_dp.name + ', STATE: ' + dp_states[0]
        lst_origin.insert(i, lst_name)

    for conn in connection_lists:
        for i, dest_dp in enumerate(conn[1:]):
            lst_name = dest_dp.name + ', STATE: ' + dp_states[1]
            lst_dest.insert(i, lst_name)

    log(f'{INFO} Search performed successfully')


def write_res_to_file():
    global all_connections
    reset_error()

    # print result to file
    print_connection_to_file(all_connections, output_filename)

    log(f'{INFO} successfully wrote {len(all_connections)} connection strings to {output_filename}')

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
txt_abb1.insert(END, default_abb_one)

txt_abb2 = Entry(root, width=43, font=entry_font)
txt_abb2.place(x=765, y=60)
txt_abb2.insert(END, default_abb_two)

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

# initiate logging
print_welcome_msg()

root.mainloop()
