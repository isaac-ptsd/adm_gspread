import adm_library
import gspread
from gspread import Spreadsheet
from gspread import utils
import csv
import time
import pprint

# TODO:
#   -> Add function that checks for records that have 0 attendance. - exclude record type 2, and 14(?)
#       -> add to attendance anomalies function?
#   -> check for enrolled date after end date
#   -> check/validate program type 10; enrollment cannot overlap with type 1 record.


def main():
    list_of_dicts = adm_library.gen_list_of_dicts()
    # adm_library.add_wsheet(adm_library.check_non_type2_dups(list_of_dicts), "duplicates_exclude_type2")
    #
    # print("\nChecking for SpEd Students:")
    # adm_library.add_wsheet(adm_library.generate_sped_list(list_of_dicts), "SpEd_students")
    # adm_library.add_wsheet(adm_library.find_no_dup_sped(list_of_dicts), "SpEd_no_dup_record")
    #
    # print("\nCalculating ADM Amount:")
    # calculate_update_calcadmamt(list_of_dicts)
    #
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
    #
    # print("\nChecking for type 2 matches:")
    # add_wsheet(check_elfg(list_of_dicts), "no_matching_ADMProgTypCd2")

    # print("\nComparing student count to calculated ADM amount:")
    # adm_library.compare_calcadm_school_counts(list_of_dicts)

    print("records with no attendance")
    adm_library.check_for_no_att(list_of_dicts)

    print("records with enrolled date after end date")
    adm_library.enrolled_after_end(list_of_dicts)


if __name__ == '__main__':
    main()
