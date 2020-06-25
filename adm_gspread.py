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


def find_all_missing_data(list_of_dicts_in, column_list_to_check=["ChkDigitStdntID",
                                                                  "DistStdntID",
                                                                  "ResdDistInstID",
                                                                  "ResdSchlInstID",
                                                                  "AttndDistInstID",
                                                                  "AttndSchlInstID",
                                                                  "LglLNm",
                                                                  "LglFNm",
                                                                  "BirthDtTxt",
                                                                  "GndrCd",
                                                                  "HispEthnicFg",
                                                                  "AmerIndianAlsknNtvRaceFg",
                                                                  "AsianRaceFg",
                                                                  "BlackRaceFg",
                                                                  "WhiteRaceFg",
                                                                  "PacIslndrRaceFg",
                                                                  "LangOrgnCd",
                                                                  "EnrlGrdCd",
                                                                  "Addr",
                                                                  "City",
                                                                  "ZipCd",
                                                                  "ResdCntyCd",
                                                                  "Phn",
                                                                  "EconDsvntgFg",
                                                                  "Ttl1Fg",
                                                                  "SpEdFg",
                                                                  "Sect504Fg",
                                                                  "MigrntEdFg",
                                                                  "IndianEdFg",
                                                                  "ELFg",
                                                                  "DstncLrnFg",
                                                                  "HomeSchlFg",
                                                                  "TAGPtntTAGFg",
                                                                  "TAGIntlctGiftFg",
                                                                  "TAGAcdmTlntRdFg",
                                                                  "TAGAcdmTlntMaFg",
                                                                  "TAGCrtvAbltyFg",
                                                                  "TAGLdrshpAbltyFg",
                                                                  "TAGPrfmArtsAbltyFg",
                                                                  "TrnstnProgFg",
                                                                  "AltEdProgFg",
                                                                  "ADMProgTypCd",
                                                                  "ADMEnrlDtTxt",
                                                                  "ADMEndDtTxt",
                                                                  "ADMEndDtCd",
                                                                  "ADMSessDays",
                                                                  "ADMPrsntDays",
                                                                  "ADMAbsntDays",
                                                                  "ADMFTE",
                                                                  "ADMTuitionTypCd",
                                                                  "RdEsntlSkillCd",
                                                                  "WrEsntlSkillCd",
                                                                  "SkEsntlSkillCd",
                                                                  "MaEsntlSkillCd",
                                                                  "DistSpEdProgFg",
                                                                  "FullAcdmYrSchlFg",
                                                                  "FullAcdmYrDistFg",
                                                                  "MltryCnctFg"]):
    """ Function to find students with missing data in a any column
        Parameter:
            column_list_to_check; can pass in a list of column names, defaults to a pre-built whitelist
        Parameter:
            list_of_dicts_in; this function operates on a list of dictionaries
        Returns: list
             list of worksheet rows; one row of complete ADM data for each record missing data in the specified column
     """
    missing_val_list = []
    for name in column_list_to_check:
        missing_val_list += find_missing_data(list_of_dicts_in, name)
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
        if x['ADMSessDays'] != ((x['ADMPrsntDays'] + x['ADMAbsntDays']) / 10):
            ret_val.append(x)
    return ret_val


# check for program type 2 (ADMProgTypCd==2)
if list(filter(lambda type2: type2['ADMProgTypCd'] == 2, list_of_dicts)):
    print("\nADM PROGRAM TYPE 2 RECORDS ARE PRESENT\n")
else:
    print("\nADM PROGRAM TYPE 2 RECORDS ARE NOT PRESENT\n")

# check for program type 14 (ADMProgTypCd==14)
if list(filter(lambda type14: type14['ADMProgTypCd'] == 14, list_of_dicts)):
    print("\nADM PROGRAM TYPE 14 RECORDS ARE PRESENT\n")
else:
    print("\nADM PROGRAM TYPE 14 RECORDS ARE NOT PRESENT\n")

# check for k-8 students that do not have EconDsvntgFg == Y
set_grade_lvl = ['KG', 1, 2, 3, 4, 5, 6, 7, 8]
k_8_list = list(filter(lambda k8: k8['EnrlGrdCd'] in set_grade_lvl, list_of_dicts))
k8_w_N_list = list(filter(lambda econ_check: econ_check['EconDsvntgFg'] != 'Y', k_8_list))

if k8_w_N_list:
    print("\nK-8 students with EconDsvntgFg not set to 'Y' are PRESENT \n")
    to_csv(k8_w_N_list, "k8_w_N.csv")
else:
    print("\nK-8 students with EconDsvntgFg not set to 'Y' are NOT PRESENT \n")

missing_data_list = find_all_missing_data(list_of_dicts)
to_csv(missing_data_list, "students_missing_data.csv")

attendance_anomalies = find_attendance_anomalies(list_of_dicts)
to_csv(attendance_anomalies, "attendance_anomalies.csv")
