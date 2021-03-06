import adm_library as adm
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
    list_of_dicts = adm.gen_list_of_dicts()
    adm.add_wsheet(adm.check_non_type2_dups(list_of_dicts), "duplicates_exclude_type2")

    print("\nChecking for SpEd Students:")
    adm.add_wsheet(adm.generate_sped_list(list_of_dicts), "SpEd_students")
    adm.add_wsheet(adm.find_no_dup_sped(list_of_dicts), "SpEd_no_dup_record")

    print("\nCalculating ADM Amount:")
    adm.calculate_update_calcadmamt(list_of_dicts)

    print("\nChecking for missing data:")
    adm.add_wsheet(adm.find_all_missing_data(list_of_dicts), "records_missing_data")

    print("\nChecking ethnic flags:")
    adm.add_wsheet(adm.check_eth_flags(list_of_dicts), "missing_eht_flag")

    print("\nChecking KG - 8 for econ EconDsvntgFg set to 'Y':")
    adm.add_wsheet(adm.check_econ_flag_k8(list_of_dicts), "k8_N_econ_flag")

    print("\nChecking for attendance anomalies:")
    adm.add_wsheet(adm.find_attendance_anomalies(list_of_dicts), "attendance_anomalies")

    print("\nChecking for ADM program type 14 students:")
    adm.check_admprog_type_14(list_of_dicts)

    print("\nChecking for ADM program type 2 students:")
    adm.check_admprog_type_2(list_of_dicts)

    print("\nChecking for type 2 matches:")
    adm.add_wsheet(adm.check_elfg(list_of_dicts), "no_matching_ADMProgTypCd2")

    print("\nComparing student count to calculated ADM amount:")
    adm.compare_calcadm_school_counts(list_of_dicts)

    print("records with no attendance")
    adm.check_for_no_att(list_of_dicts)

    print("records with enrolled date after end date")
    time.sleep(2)
    adm.enrolled_after_end(list_of_dicts)


if __name__ == '__main__':
    main()
