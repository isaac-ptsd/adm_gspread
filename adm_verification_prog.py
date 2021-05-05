import adm_library as adm
import gspread
from gspread import Spreadsheet
from gspread import utils
import csv
import time
import pprint


def main():
    # print("\nDid you run the \"Refresh Attendance Views Data\" function!?!?!?!?!?!\n\n")
    # time.sleep(4)
    # #
    list_of_dicts = adm.gen_list_of_dicts()

    # print("\nChecking for duplicate records (excluding program type 2):")
    # adm.add_wsheet(adm.check_non_type2_dups(list_of_dicts), "duplicates_exclude_type2")
    #
    # print("\nChecking for SpEd Students:")
    # adm.add_wsheet(adm.generate_sped_list(list_of_dicts), "SpEd_students")

    # print("\nChecking for missing data:")
    # adm.add_wsheet(adm.find_all_missing_data(list_of_dicts), "records_missing_data")
    #
    # print("\nChecking ethnic flags:")
    # adm.add_wsheet(adm.check_eth_flags(list_of_dicts), "missing_eht_flag")
    #
    # print("\nChecking KG - 8 for econ EconDsvntgFg set to 'Y':")
    # adm.add_wsheet(adm.check_econ_flag_k8(list_of_dicts), "k8_N_econ_flag")
    #
    # print("\nChecking for attendance anomalies:")
    # adm.add_wsheet(adm.find_attendance_anomalies(list_of_dicts), "attendance_anomalies")
    #
    # print("\nChecking for ADM program type 14 students:")
    # adm.check_admprog_type_14(list_of_dicts)
    #
    # print("\nChecking for ADM program type 2 students:")
    # adm.check_admprog_type_2(list_of_dicts)
    #
    # print("\nChecking for type 2 matches:")
    # adm.add_wsheet(adm.check_elfg(list_of_dicts), "no_matching_ADMProgTypCd2")

    # print("\nChecking for records with no attendance:")
    # adm.add_wsheet(adm.check_for_no_att(list_of_dicts), "No_Attendance_Data")
    #
    # print("\nChecking for records with enrolled date after end date:")
    # adm.add_wsheet(adm.enrolled_after_end(list_of_dicts), "End Date greater than or equal to Enroll Date")
    #
    # print("Checking for missing implicit 0's")
    # adm.add_wsheet(adm.validate_present_absent_days(list_of_dicts), "bad days")

    # print("\nCalculating ADM Amount:")
    # adm.calculate_update_calcadmamt(list_of_dicts)

    print("\nComparing student count to calculated ADM amount:")
    time.sleep(4)  # ensures adm amount has been writen to google sheet
    adm.compare_calcadm_school_counts(list_of_dicts)


if __name__ == '__main__':
    main()
