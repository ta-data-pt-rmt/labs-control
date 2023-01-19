"""Sends cohort students emails info regarding their lab statuses."""
import logging
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
import time
from typing import List
import pathlib

from settings import STUDENT_EMAILS, DROPPED_STUDENTS, SENDING_EMAIL, SECRETS_PATH

# logger
logger = logging.getLogger(__name__)

def obtain_ta_secrets(
    secrets_path: pathlib.Path = SECRETS_PATH
    ) -> List[str]:

    # import secrets password and token
    with open(secrets_path.joinpath('secrets.txt')) as f:
        secrets = f.read().splitlines()

    # store TEACHING_EMAIL password
    ta_ironhack_password = secrets[0]
    # store access token of email used for sending emails
    access_token_emails = secrets[1]

    secrets = [ta_ironhack_password, access_token_emails]

    return secrets


def _get_completed_and_pending_labs(
    labs_overall : pd.DataFrame,
    student_name : str
    )->  List[str] :

    # filter by student
    student_sub = labs_overall[labs_overall["student_name"] == student_name]

    # filter only for required labs
    student_sub = student_sub[student_sub["required"]== "Required"]
    
    # count delivered and not delivered labs
    delivered_labs = (
        student_sub[student_sub["lab_status"]== "Delivered"]["Lab_name"]
        .unique()
        .tolist()
    )
    pending_labs =(
        student_sub[student_sub["lab_status"]== "Pending"]["Lab_name"]
        .unique()
        .tolist()
    )
    logger.info(f"""{len(delivered_labs)} delivered and {len(pending_labs)} pending
    labs for {student_name}, so far.""")
    # wrap up results in a list
    labs_results = [ delivered_labs, pending_labs]

    return labs_results

def _get_lab_completion_metrics(
    macro_df : pd.DataFrame,
    student_name : str,
    ) -> List[float] :

    # filter by student name
    student_df = macro_df[macro_df["student_name"]== student_name]

    # bootcamp total labs
    total_labs = student_df['total_required_labs'].iloc[0]

    logger.info(f"There is {int(total_labs)} labs in total for this cohort.")

    return total_labs

def send_emails(
    week,
    labs_overall : pd.DataFrame,
    macro_df : pd.DataFrame,
    email_token: str, 
    email_sender : str = SENDING_EMAIL,
    dropped_students : List[str] = DROPPED_STUDENTS,
    email_dict : dict = STUDENT_EMAILS
    ) -> str:

    # cohort students
    student_names = email_dict.keys()

    # iterate through all students
    for student in student_names:

        if student in dropped_students:
            pass

        logger.info(f"Preparing e-mail sending for student {student}.")
        # lists of required and pending labs
        labs_lists = _get_completed_and_pending_labs(labs_overall, student)
        completed_labs_list = labs_lists[0]
        pending_labs_list = labs_lists[1]
        current_total_labs = len(completed_labs_list) + len(pending_labs_list) 
        current_completion_pctg = round( len(completed_labs_list)/ current_total_labs, 2)*100

        # student macro metrics
        bootcamp_total_requireds = _get_lab_completion_metrics(macro_df, student)

        # add as strings lines
        delivered_labs_strings = "\n".join(completed_labs_list)
        pending_labs_strings = "\n".join(pending_labs_list)

                            
        if current_completion_pctg < 80:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status.
            So far, out of {current_total_labs} existing labs until Week {week}, you have delivered {len(completed_labs_list)},
            implying that your submission percentage is {current_completion_pctg}%.
            
            Keep in mind that the total number of required labs of this bootcamp is {bootcamp_total_requireds}, and you have submitted {len(completed_labs_list)} labs, 
            this represents {round((len(completed_labs_list)/bootcamp_total_requireds),2)*100}% of total submission completion.
            Remember that by Ironhack rules, a minimum of 80% completion on required labs is the threshold to complete the course. 
            Don't hesitate in contacting us if you need help to meet that threshold. We will be happy to support you!

            The labs that you are missing are:
            {pending_labs_strings}

            the labs you've delivered are:
            {delivered_labs_strings}
                    
            Ironhack Teaching Team
            '''
                            
        elif current_completion_pctg == 100:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status. From a total of {current_total_labs} labs existing until Week {week},
            you have submitted {len(completed_labs_list)} labs, this represents {current_completion_pctg}% of the total until now.
            You have submitted all labs, so congratulations for your hard work!
                    
            Ironhack Teaching Team
            '''
        
        else:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status. From a total of {current_total_labs} existing labs until Week {week},
            you have submitted {len(completed_labs_list)}, this represents {current_completion_pctg}% of the total.
            You are over the 80% threshold marked by Ironhack to complete the course so congratulations! You are properly following the course progress.
            Anyway, if you want to reach that beautiful 100% mark and keep practicing your skills, here are some labs that are still missing:
            {pending_labs_strings}

            Keep going with the hard job!
                    
            Ironhack Teaching Team
            '''
        #later replace with : email_dict[student]:    
        email_receiver = "miguelsimonmoya@gmail.com" 
        
        subject = "Ironhack lab status"
        
        em = EmailMessage()
        em["From"] = email_sender
        em["To"] = email_receiver
        em["subject"] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", context = context) as smtp:
            smtp.login(email_sender, email_token)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
                            
        time.sleep(2)
    
    return "E-mails sent to all students. Repeat proccess next week (:"