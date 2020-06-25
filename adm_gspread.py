import gspread
import pprint
import csv


gc = gspread.oauth()
# sh = gc.open_by_key('1QE6fZP7YsLY1RRVS9HG6ru1O7sC63LEWxaBjDJXkvUg')  # small sample sheet
sh = gc.open_by_key('1cek2uerqbb1Der0jPL-VV_YlDCBRXFjNsr5I6rsyWCQ')  # full copy of comb_adm
worksheet = sh.sheet1

list_of_dicts = worksheet.get_all_records()  # all data in the spreadsheet saved as a list of dictionaries
list_of_lists = worksheet.get_all_values()  # all data in the spreadsheet saved as a list of lists

# cell_list = worksheet.range('A1:A26')
# values_list = worksheet.col_values(1)

# new_values = ['0' + value for value in values_list]
# for i, val in enumerate(new_values):
#     cell_list[i].value = val
# worksheet.update_cells(cell_list)


def find_missing_ssid(list_of_dicts_in):
    """ Function to find students with missing SSID's
        Parameter:
            list_of_dicts_in; this function operates on a list of dictionaries
        Returns: list
            list of worksheet rows; one row of complete ADM data for each record missing an SSID
    """
    return list(filter(lambda missing: missing['ChkDigitStdntID'] == '', list_of_dicts_in))


def find_missing_data(list_of_dicts_in, column_name_to_check):
    """ Function to find students with missing data in a specified column
        Parameter:
            list_of_dicts_in; this function operates on a list of dictionaries
        Parameter:
            column_name_to_check; this is the column the function checks for missing data

        Returns: list
            list of worksheet rows; one row of complete ADM data for each record missing data in the specified column
    """
    return list(filter(lambda missing: missing[column_name_to_check] == '', list_of_dicts_in))


def find_all_missing_data(list_of_dicts_in):
    """ Function to find students with missing data in a any column
         Parameter:
             list_of_dicts_in; this function operates on a list of dictionaries
         Returns: list
             list of worksheet rows; one row of complete ADM data for each record missing data in the specified column
     """
    column_names = list(list_of_dicts_in[0].keys())
    missing_val_list = []
    for name in column_names:
        missing_val_list += find_missing_data(list_of_dicts, name)
    # remove duplicates from the returned list
    ret_val = [i for n, i in enumerate(missing_val_list) if i not in missing_val_list[n + 1:]]
    return ret_val


def to_csv(list_of_dicts_in, name_of_csv_to_create):
    """ Function that takes a list of dictionaries and creates a csv file.
    Parameter: list of dictionaries
        list_of_dicts_in; the list of dictionaries to create a csv out of
    Parameter: string
        name_of_csv_to_create; this will be the name of the resulting csv file - NOTE: include .csv
    Returns: no return value
        will create a csv file in current directory
    """
    keys = list_of_dicts_in[0].keys()
    with open(name_of_csv_to_create, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts_in)


def find_attendance_anomalies(list_of_dicts_in):
    """
    Function that will find and return ADM attendance data that does not add up correctly
    :param list_of_dicts_in:
    :return: list of dictionaries with each record that has attendance data that does not add up
    """
    ret_val = []
    for x in list_of_dicts_in:
        if x['ADMSessDays'] != ((x['ADMPrsntDays'] + x['ADMAbsntDays'])/10):
            ret_val.append(x)
    return ret_val


attendance_anomalies = find_attendance_anomalies(list_of_dicts)
to_csv(attendance_anomalies, "attendance_anomalies.csv")
pprint.pp(attendance_anomalies)




