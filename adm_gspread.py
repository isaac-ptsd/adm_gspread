import gspread
import pprint

gc = gspread.oauth()
sh = gc.open_by_key('1QE6fZP7YsLY1RRVS9HG6ru1O7sC63LEWxaBjDJXkvUg')
worksheet = sh.sheet1

list_of_dicts = worksheet.get_all_records()  # all data in the spreadsheet saved as a list of dictionaries
list_of_lists = worksheet.get_all_values()  # all data in the spreadsheet saved as a list of lists

# cell_list = worksheet.range('A1:A26')
# values_list = worksheet.col_values(1)

# new_values = ['0' + value for value in values_list]
# for i, val in enumerate(new_values):
#     cell_list[i].value = val
# worksheet.update_cells(cell_list)

def find_missing_ssid():
    """ Function to find students with missing SSID's
        Returns: list
            list of worksheet rows; one row of complete ADM data for each record missing an SSID
    """
    return list(filter(lambda missing: missing['ChkDigitStdntID'] == '', list_of_dicts))


