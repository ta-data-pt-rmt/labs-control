"""Sends cohort students emails info regarding their lab statuses."""
import pandas as pd
from email.message import EmailMessage
import ssl
import smtplib
import time

from settings import STUDENT_EMAILS


def send_emails(
    labs_overall : pd.DataFrame,
    week_number_email : int,
    email_sender : str,
    email_password: str, 
    email_dict : dict = STUDENT_EMAILS
    ) -> str:

    student_names = list(email_dict.keys())


    for student in student_names:
        
        # Filtering by student
        student_sub = labs_overall[labs_overall["student_name"] == student]
        
        # Filtering by week number
        student_sub_week = student_sub[student_sub["week_num"] <= week_number_email]
        
        # Count delivered and not delivered labs
        submissions = student_sub_week["lab_status"].value_counts()
        delivered = submissions["Delivered"]
        try:
            not_delivered = submissions[""]
        except:
            not_delivered = 0
        
        # Get the lab names of non delivered ones
        pending_labs = student_sub_week[student_sub_week["lab_status"] == ""]["lab_name"].values.tolist()
        pending_labs_strings = "\n".join(pending_labs)
        
        # Calculate the percentage of delivered labs
        lab_percent = round((delivered / (delivered+not_delivered))*100)
                            
        if lab_percent < 80:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status. From a total of {delivered + not_delivered} labs, you have submitted {delivered}, this represents the {lab_percent}% of the total until now.
    Remember that ironhack rules mark 80% as the threshold to complete the course. Don't hesitate in contacting us if you need help to meet that threshold. We will be happy to support you!

    The labs that you are missing are:
    {pending_labs_strings}
            
    Ironhack Teaching Team
            '''
                            
        elif lab_percent == 100:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status. From a total of {delivered + not_delivered} labs, you have submitted {delivered}, this represents the {lab_percent}% of the total until now.
    You have submitted all the labs so far, so congratulations for this hard job!
            
    Ironhack Teaching Team
            '''
        
        else:
            body = f'''Dear {student.split()[0]}, we have been checking your lab sumissions status. From a total of {delivered + not_delivered} labs, you have submitted {delivered}, this represents the {lab_percent}% of the total until now.
    You are over the 80% threshold marked by Ironhack to complete the course so congratulations! You are properly following the course progress.
    Anyway,there are some labs that are still missing:
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
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
                            
        time.sleep(2)
    
    return "E-mails sent to all students. Repeat proccess next week (:"