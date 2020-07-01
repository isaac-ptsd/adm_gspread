# adm_gspread

For authorization set up see: https://gspread.readthedocs.io/en/latest/oauth2.html

This script makes heavy use of the gspread python library
gspread documentation: https://gspread.readthedocs.io/en/latest/index.html

This script will automate some of the tedious work required to verify data in an ADM.

Functions available:


`find_missing_data(list_of_dicts_in, column_name_to_check):`

    """ Function to find students with missing data in a specified column
        Parameter:
            list_of_dicts_in; this function operates on a list of dictionaries
        Parameter:
            column_name_to_check; this is the column the function checks for missing data
        Returns: list
            list of worksheet rows; one row of complete ADM data for each record missing data in the specified column
    """           each record missing data in the specified column
   
            
`find_all_missing_data(list_of_dicts_in, column_list_to_check):`
 
    """ Function to find students with missing data in a any column
        Parameter:
            column_list_to_check; can pass in a list of column names, defaults to a pre-built whitelist
        Parameter:
            list_of_dicts_in; this function operates on a list of dictionaries
        Returns: list
             list of worksheet rows; one row of complete ADM data for each record missing data in the specified column
     """
     
`to_csv(list_of_dicts_in, name_of_csv_to_create):`

    """ Function that takes a list of dictionaries and creates a csv file.
    Parameter: list of dictionaries
        list_of_dicts_in; the list of dictionaries to create a csv out of
    Parameter: string
        name_of_csv_to_create; this will be the name of the resulting csv file - NOTE: include .csv
    Returns: no return value
        will create a csv file in current directory
    """
    
`find_attendance_anomalies(list_of_dicts_in):`
 
    """
    Function that will find and return ADM attendance data that does not add up correctly
    :param list_of_dicts_in:
    :return: list of dictionaries with each record that has attendance data that does not add up
    """
    
`check_admprog_type_2(list_of_dicts_in):`
 
    """
    :param list_of_dicts_in:
    :return: bool
    """
    
`check_admprog_type_14(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: no return value; will print results to stdout
    """
    
`check_econ_flag_k8(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: list of dictionaries of K-8 students with EconDsvntgFg not set to 'Y'
    """
    
`check_eth_flags(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: list of dictionaries containing all records that do not have an ethnic flag set
    """
    
`add_wsheet(data_in, sheet_name, email_in='isaac.stoutenburgh@phoenix.k12.or.us'):`

    """
    :param data_in: List of dictionaries
    :param sheet_name: String
    :param email_in: String: defaults to 'isaac.stoutenburgh@phoenix.k12.or.us'
    :return: No return value
             Will add a new worksheet to the spreadsheet
    """
    
`def check_elfg(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: list of dicts, containing all records (program type 1) that have ELFg set,
             but no corresponding program type two record
    """
    
`def calculate_update_calcadmamt(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: list of calculated adm values,
             NOTE: will also update the CalcADMAmt column associated with the open worksheet
    """
    
`def compare_calcadm_school_counts(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: no return value will print to stdout a comparison of the ADM amount and school attendance numbers
    """
    
`def generate_sped_list(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: List of students with SpEdFg == 'Y'
    """
    
`def find_no_dup_sped(list_of_dicts_in):`

    """
    :param list_of_dicts_in:
    :return: list of SpEd students who have only 1 record in the ADM
    """
    
`def check_non_type2_dups(list_of_dicts_in):`
    
      """
    :param list_of_dicts_in: 
    :return: returns a list of students with duplicate records - excluding program type 2
    """
    
    
    