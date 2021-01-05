import gspread
from gspread import Spreadsheet
from gspread import utils
import csv
import time
from datetime import datetime as dt

sheet_key = '1ODfFFt6bjs34QPR-KPZ3A08SQJbYugzICLSG8rXwmME'  # 2nd period adm
# authorize, and open a google spreadsheet
gc = gspread.oauth()
sh: Spreadsheet = gc.open_by_key(sheet_key)
worksheet = sh.sheet1


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
    # todo: Bug when list of one element
    missing_val_list = []
    for name in column_list_to_check:
        missing_val_list += find_missing_data(list_of_dicts_in, name)
    # remove duplicates from the returned list
    ret_val = [i for n, i in enumerate(missing_val_list) if i not in missing_val_list[n + 1:]]
    if ret_val:
        print("RECORDS MISSING DATA FOUND")
    else:
        print("NO RECORDS MISSING DATA FOUND")
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
        if x['ADMProgTypCd'] != 10:
            if x['ADMSessDays'] != ((x['ADMPrsntDays'] + x['ADMAbsntDays']) / 10):
                ret_val.append(x)
    return ret_val


def check_admprog_type_2(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: bool
    """
    if list(filter(lambda type2: type2['ADMProgTypCd'] == 2, list_of_dicts_in)):
        print("ADM PROGRAM TYPE 2 RECORDS ARE PRESENT")
        return True
    else:
        print("ADM PROGRAM TYPE 2 RECORDS ARE NOT PRESENT")
        return False


def check_admprog_type_14(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: no return value; will print results to stdout
    """
    if list(filter(lambda type14: type14['ADMProgTypCd'] == 14, list_of_dicts_in)):
        print("ADM PROGRAM TYPE 14 RECORDS ARE PRESENT")
        return True
    else:
        print("ADM PROGRAM TYPE 14 RECORDS ARE NOT PRESENT")
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
        print("K-8 students with EconDsvntgFg not set to 'Y' are PRESENT")
        return k8_w_N_list
    else:
        print("K-8 students with EconDsvntgFg not set to 'Y' are NOT PRESENT")


def check_eth_flags(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of dictionaries containing all records that do not have an ethnic flag set
    """
    no_eth_flag_set = []
    for x in list_of_dicts_in:
        flag_comp = (x['HispEthnicFg'] + x['AmerIndianAlsknNtvRaceFg'] + x['AsianRaceFg'] + x['BlackRaceFg'] + x[
            'WhiteRaceFg'] + x['PacIslndrRaceFg'])
        if flag_comp == "NNNNNN":
            no_eth_flag_set.append(x)
    if no_eth_flag_set:
        print("STUDENTS WITHOUT AN ETHNIC FLAG SET WERE FOUND")
        return no_eth_flag_set
    else:
        print("STUDENTS WITHOUT AN ETHNIC FLAG SET WERE *NOT* FOUND")


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
        cell_range = sheet.range('A2:' + last_cell)
        flattened_test_data = []
        for row in data_in:
            for column in headers:
                flattened_test_data.append(row[column])
        for i, cell in enumerate(cell_range):
            cell.value = flattened_test_data[i]
        sheet.update_cells(cell_range)
    except TypeError as e:
        print("Worksheet not created - no data", e)
    except IndexError as e:
        print("\nERROR in function: add_wsheet ", e)
    except gspread.exceptions.APIError as e:
        print("ERROR ADDING WORKSHEET: ", e)


# check that records where ELFg = y, also have a program type 2 record
def check_elfg(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of dicts, containing all records (program type 1) that have ELFg set,
             but no corresponding program type two record
    """
    elfg_flag_set = list(filter(lambda elfg_check: elfg_check['ELFg'] == 'Y', list_of_dicts_in))
    type_2 = list(filter(lambda prog2_check: prog2_check['ADMProgTypCd'] == 2, elfg_flag_set))
    type_1 = list(filter(lambda prog2_check: prog2_check['ADMProgTypCd'] == 1, elfg_flag_set))
    list_diff = []
    for stu_1 in type_1:
        if not any(stu_2["DistStdntID"] == stu_1["DistStdntID"] for stu_2 in type_2):
            list_diff.append(stu_1)
    if len(list_diff) > 0:
        # todo: this breaks when list_diff has one element
        print(list_diff)
        return list_diff
    else:
        print("<=0")


def calculate_update_calcadmamt(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of calculated adm values,
             NOTE: will also update the CalcADMAmt column associated with the open worksheet
    """
    student_amd_calc = []
    for student in list_of_dicts_in:
        if ((student["ADMPrsntDays"] != 0 or
             student["ADMAbsntDays"] != 0) and
                student["ADMSessDays"] != 0 and
                student["ADMFTE"] != 0 and
                student["ADMInstrctHrs"] == 0):
            student_amd_calc.append(
                ((int(student["ADMPrsntDays"]) + int(student["ADMAbsntDays"])) / int(student["ADMSessDays"])) /
                int(student["ADMFTE"]))
        else:
            student_amd_calc.append(0)
    cell_list = worksheet.range('CC2:CC' + str(worksheet.row_count))
    for i, val in enumerate(student_amd_calc):
        cell_list[i].value = val
    worksheet.update_cells(cell_list)
    print("ADM amount calculated and written to sheet")
    return student_amd_calc


def compare_calcadm_school_counts(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: no return value will print to stdout a comparison of the ADM amount and school attendance numbers
    """
    time.sleep(1)
    type_1 = list(filter(lambda prog2_check: prog2_check['ADMProgTypCd'] == 1, list_of_dicts_in))

    i = 0
    try:
        while i < 5:
            students_list = [student for student in type_1 if (student["ResdSchlInstID"] == 370 + i)]
            # sum_cal = sum([s["CalcADMAmt"] for s in students_list])
            sum_cal = 0
            s_error_reporting = ()
            for s in students_list:
                sum_cal += s["CalcADMAmt"]
                s_error_reporting = s
            print(
                "Student count " + str(370 + i) + ": " + str(len(students_list)) + " -- Sum CalcADMAmt: " + str(
                    sum_cal))
            i += 1
    except TypeError as e:
        print("ERROR: ", e)
        print("Record: ", s_error_reporting)


def generate_sped_list(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: List of students with SpEdFg == 'Y'
    """
    return [student for student in list_of_dicts_in if (student["SpEdFg"] == 'Y')]


def find_no_dup_sped(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: list of SpEd students who have only 1 record in the ADM
    """
    # sped_list = [student for student in list_of_dicts_in if (student["SpEdFg"] == 'Y')]
    sped_list = generate_sped_list(list_of_dicts_in)
    no_dup = []
    for i in sped_list:
        count = 0
        for j in sped_list:
            if i["DistStdntID"] == j["DistStdntID"]:
                count += 1
        if count == 1:
            no_dup.append(i)
    return no_dup


def check_non_type2_dups(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: returns a list of students with duplicate records - excluding program type 2
    """
    no_type_2 = [student for student in list_of_dicts_in if (student["ADMProgTypCd"] != 2)]
    duplicate_records = []
    for i in no_type_2:
        count = 0
        for j in no_type_2:
            if i["DistStdntID"] == j["DistStdntID"]:
                count += 1
        if count > 1:
            duplicate_records.append(i)
    return duplicate_records


def gen_list_of_dicts():
    # pulling all data from the spreadsheet with one API call
    return worksheet.get_all_records()  # spreadsheet data saved as a list of dictionaries


def check_for_no_att(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return: returns all records that have no days present
    """
    list_no_att = [student for student in list_of_dicts_in if (student["ADMPrsntDays"] == 0)]
    if list_no_att:
        print("Records with no attendance found")
    else:
        print("Records with no attendance not found")
    return list_no_att


def enrolled_after_end(list_of_dicts_in):
    """
    :param list_of_dicts_in:
    :return:
    """
    # return [student for student in list_of_dicts_in if
    #         (dt.strftime(student["ADMEnrlDtTxt"], "mmddyyyy") > dt.strftime(str(student["ADMEndDtTxt"]), "mmddyyyy"))]
    for student in list_of_dicts_in:
        enroll_date = student["ADMEnrlDtTxt"]
        end_date = student["ADMEndDtTxt"]
