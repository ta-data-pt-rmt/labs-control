"""Main script to run weekly labs control."""
import logging
import pathlib
import sys
import pandas as pd
import argparse
from scraper import campus_tools_connection, get_macro_student_table, create_students_table, clean_students_table
from email_sender import send_emails, obtain_ta_secrets
from settings import WEEKS_DICT, STUDENT_EMAILS, TEACHING_EMAIL, SENDING_EMAIL, BOOTCAMP_WEEKS

# logger
logger = logging.getLogger(__name__)

def main(
    current_week : int,
    ta_ironhack_email : str = TEACHING_EMAIL,
    ta_gmail_email : str = SENDING_EMAIL,
    email_dict : dict = STUDENT_EMAILS,
    weeks_organization : dict = WEEKS_DICT,
    )-> str:
    """Runs all weekly pipeline. 
    Scrapes students portal;
    Creates Dataframe;
    Cleans table;
    Sends e-mail of their current lab status;
    """

    secrets = obtain_ta_secrets()

    # main ironhack ta email
    ta_ironhack_password = secrets[0]

    # token for sending emails in secondary gmail account
    ta_gmail_token = secrets[1]

    # create driver instance and connection to campus tools
    driver = campus_tools_connection(
        ta_ironhack_password,
        ta_ironhack_email)

    macro_results = get_macro_student_table(driver)
    logger.info("Macro table created")
    logger.info(f"Added information for {len(macro_results)} students.")
    logger.info(f"Students added were : {macro_results['student_name'].unique()}")

    # list with all students
    students_list = macro_results['student_name'].unique().tolist()

    # students performance table
    labs_overall = create_students_table( students_list, driver)
    

    # clean table
    labs_overall = clean_students_table(labs_overall)
    labs_overall.to_csv("labs_without_weeks.csv")
    # dictionary with labs per week number key into DataFrame 
    weeks_df = (
        pd.DataFrame.
        from_dict(weeks_organization, orient='index').
        stack().
        reset_index()
    )

    weeks_df.columns = ['Week', 'row', 'Lab_name']
    weeks_df = weeks_df.drop('row', axis=1)

    # merge with labs_overall
    labs_with_weeks = labs_overall.merge(
        weeks_df,
        how="left",
        left_on = "lab",
        right_on = "Lab_name")

    labs_with_weeks["week_nr"] = labs_with_weeks['Week'].str.extract('(\d+)').astype(int)
    # filter based on current week input
    labs_with_weeks = (
        labs_with_weeks.loc[labs_with_weeks["week_nr"] <= int(current_week)]
    )

    # send emails for all students:
    send_emails(
        current_week,
        labs_with_weeks,
        macro_results,
        ta_gmail_token,
        ta_gmail_email,
        email_dict
    )
    

    return "tables saved."

if __name__ == "__main__": # pragma: no cover

    parser = argparse.ArgumentParser(
        description='Add current week to filter labs submission dates.')
    parser.add_argument(
        '-w',
        '--week',
        type=int,
        help="Specify current week."
    )

    args = parser.parse_args()

    current_week = args.week

    # check if week is less than total bootcamp weeks for part-time (22)
    if int(current_week) > BOOTCAMP_WEEKS:
        logger.error("Please input week value smaller than 23.")
        sys.exit()


    #run script
    main(current_week)





