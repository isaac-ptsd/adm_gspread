import gspread
from gspread import Spreadsheet
from gspread import utils
import csv


# authorize, and open a google spreadsheet
gc = gspread.oauth()
sh: Spreadsheet = gc.open_by_key('1cek2uerqbb1Der0jPL-VV_YlDCBRXFjNsr5I6rsyWCQ')  # full copy of comb_adm
# sh: Spreadsheet = gc.open_by_key('1woYgnf3cL5oLr57Yr7bKrEB2-ZU5RvjQA0ZtTkENMO4') # live adm_comb file
worksheet = sh.sheet1

# pulling all data from the spreadsheet with one API call
list_of_dicts = worksheet.get_all_records()  # spreadsheet data saved as a list of dictionaries


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
    if ret_val:
        print("\nRECORDS MISSING DATA FOUND")
    else:
        print("\nNO RECORDS MISSING DATA FOUND")
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
    try:
        keys = list_of_dicts_in[0].keys()
        with open(name_of_csv_to_create, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(list_of_dicts_in)
    except Exception as e:
        print(e)


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


def check_admprog_type_2(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: bool
    """
    if list(filter(lambda type2: type2['ADMProgTypCd'] == 2, list_of_dicts_in)):
        print("\nADM PROGRAM TYPE 2 RECORDS ARE PRESENT")
        return True
    else:
        print("\nADM PROGRAM TYPE 2 RECORDS ARE NOT PRESENT")
        return False


def check_admprog_type_14(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: no return value; will print results to stdout
    """
    if list(filter(lambda type14: type14['ADMProgTypCd'] == 14, list_of_dicts_in)):
        print("\nADM PROGRAM TYPE 14 RECORDS ARE PRESENT")
        return True
    else:
        print("\nADM PROGRAM TYPE 14 RECORDS ARE NOT PRESENT")
        return False


def check_econ_flag_k8(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of dictionaries of K-8 students with EconDsvntgFg not set to 'Y'
    """
    set_grade_lvl = ['KG', 1, 2, 3, 4, 5, 6, 7, 8]
    k_8_list = list(filter(lambda k8: k8['EnrlGrdCd'] in set_grade_lvl, list_of_dicts_in))
    k8_w_N_list = list(filter(lambda econ_check: econ_check['EconDsvntgFg'] != 'Y', k_8_list))

    if k8_w_N_list:
        print("\nK-8 students with EconDsvntgFg not set to 'Y' are PRESENT")
        return k8_w_N_list
    else:
        print("\nK-8 students with EconDsvntgFg not set to 'Y' are NOT PRESENT")


def check_eth_flags(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of dictionaries containing all records that do not have an ethnic flag set
    """
    no_eth_flag_set = []
    for x in list_of_dicts_in:
        flag_comp = (x['HispEthnicFg'] + x['AmerIndianAlsknNtvRaceFg'] + x['AsianRaceFg'] + x['BlackRaceFg'] + x['WhiteRaceFg'] + x['PacIslndrRaceFg'])
        if flag_comp == "NNNNNN":
            no_eth_flag_set.append(x)
    if no_eth_flag_set:
        print("\nSTUDENTS WITHOUT AN ETHNIC FLAG SET WERE FOUND")
        return no_eth_flag_set
    else:
        print("\nSTUDENTS WITHOUT AN ETHNIC FLAG SET WERE *NOT* FOUND")


def add_wsheet(data_in, sheet_name, email_in='isaac.stoutenburgh@phoenix.k12.or.us'):
    """
    :param data_in: List of dictionaries
    :param sheet_name: String
    :param email_in: String: defaults to 'isaac.stoutenburgh@phoenix.k12.or.us'
    :return: No return value
             Will add a new worksheet to the spreadsheet
    """
    try:
        if data_in[0]:
            headers = list(data_in[0].keys())
        else:
            headers = list(data_in.keys())
        sheet = sh.add_worksheet(sheet_name, len(data_in), len(headers))
        sheet.append_row(headers)
        last_cell = gspread.utils.rowcol_to_a1(len(data_in), len(headers))
        cell_range = sheet.range('A2:'+last_cell)
        flattened_test_data = []
        for row in data_in:
            for column in headers:
                flattened_test_data.append(row[column])

        for i, cell in enumerate(cell_range):
            cell.value = flattened_test_data[i]

        sheet.update_cells(cell_range)
    except TypeError as e:
        print("\nEmpty List passed as argument - no worksheet will be created")


# check that records where ELFg = yes, also have a program type 2 record
def check_elfg(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return:
    """
    elfg_flag_set = list(filter(lambda elfg_check: elfg_check['ELFg'] == 'Y', list_of_dicts_in))
    type_2 = list(filter(lambda prog2_check: prog2_check['ADMProgTypCd'] == 2, elfg_flag_set))
    type_1 = list(filter(lambda prog2_check: prog2_check['ADMProgTypCd'] == 1, elfg_flag_set))
    list_diff = []
    for stu_1 in type_1:
        if not any(stu_2["DistStdntID"] == stu_1["DistStdntID"] for stu_2 in type_2):
            list_diff.append(stu_1)
    return list_diff


# calculate CalcADMAmt =(BL2+BM2)/BK2/BO2

# print("\nChecking for missing data:")
# add_wsheet(find_all_missing_data(list_of_dicts), "records_missing_data")
#
# print("\nChecking ethnic flags:")
# add_wsheet(check_eth_flags(list_of_dicts), "missing_eht_flag")
#
# print("\nChecking KG - 8 for econ EconDsvntgFg set to 'Y':")
# add_wsheet(check_econ_flag_k8(list_of_dicts), "k8_N_econ_flag")
#
# print("\nChecking for attendance anomalies:")
# add_wsheet(find_attendance_anomalies(list_of_dicts), "attendance_anomalies")
#
# print("\nChecking for ADM program type 14 students:")
# check_admprog_type_14(list_of_dicts)
#
# print("\nChecking for ADM program type 2 students:")
# check_admprog_type_2(list_of_dicts)

print("Checking for type 2 matches:")
add_wsheet(check_elfg(list_of_dicts), "no_matching_ADMProgTypCd2")


