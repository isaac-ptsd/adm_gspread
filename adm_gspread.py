import gspread

gc = gspread.oauth()
sh = gc.open_by_key('1QE6fZP7YsLY1RRVS9HG6ru1O7sC63LEWxaBjDJXkvUg')
worksheet = sh.sheet1
cell_list = worksheet.range('A1:A26')
values_list = worksheet.col_values(1)
new_values = ['0' + value for value in values_list]
for i, val in enumerate(new_values):
    cell_list[i].value = val
worksheet.update_cells(cell_list)

def find_missing_ssid(cell_list):
    """ Function to find students with missing SSID's
        Parameters: list
            cell_list: list of google sheet cell data pulled from ChkDigitStdntID column
        Returns: list
            list of worksheet rows; one row of complete ADM data for each record missing an SSID
    """


print(new_values)
