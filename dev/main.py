import pandas as pd
import argparse
from scraper import get_students_table, clean_labs_table
from email_sender import send_emails
from settings import STUDENT_EMAILS

def main(
    current_week: int
)-> str:
    """Runs all weekly pipeline. 
    Scrapes students portal;
    Creates Dataframe;
    Cleans table;
    Sends e-mail of their current lab status;
    """

    labs_df = (
        get_students_table()
        .pipe(clean_labs_table)
    )

    send_emails(
        labs_df,
        current_week,
        "ta-data-pt-rmt@ironhack.com",
        STUDENT_EMAILS)

    return "E-mails sent. Repeat process next week (:"

if __name__ == "__main__": # pragma: no cover

    parser = argparse.ArgumentParser(
        description='Add current week to filter labs submission dates.')
    parser.add_argument(
        '-w',
        '--week',
        type=int,
        help="Specify current week."
    )

    parser.add_argument(
        '-p',
        '--password',
        type = str,
        help = "Pass teaching email's password."
    )

    args = parser.parse_args()

    current_week = args.week
    teaching_password = args.password

    #run script:
    main(current_week)





