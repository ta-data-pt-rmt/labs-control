"""Scrapes IH Student Portal and returns"""
# pylint: disable=consider-using-enumerate
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from settings import  COHORT_LINK, TEACHING_EMAIL
from bs4 import BeautifulSoup

# logger
logger = logging.getLogger(__name__)


def campus_tools_connection(
    teacher_password : str,
    teacher_email : str = TEACHING_EMAIL,
    cohort_link : str = COHORT_LINK
    )-> webdriver:
    """Creates driver connection to ironhack campus tools
    and inserts ta account credentials to log in.
    
    Args:
        -teacher_password (str) : password which will be parsed 
            when running main script.
        -teacher_email (str) : TA's teaching email

    Returns:
        - driver (webdriver) : driver for course progress for each student
    """

    # create driver instance
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    time.sleep(9.5)

    # open student lab progress page
    driver.get(cohort_link)
    time.sleep(4)

    # redirection to gmail log-in
    # e-mail box
    email_box = driver.find_element(By.ID, "identifierId")
    email_box.clear()
    email_box.send_keys(teacher_email)
    time.sleep(3)

    # advance button
    advance_1 = driver.find_element(By.ID, "identifierNext")
    advance_1.click()
    time.sleep(3.5)

    # password box
    pass_box = driver.find_element(By.NAME, "password")
    time.sleep(0.5)
    pass_box.clear()
    time.sleep(1.5)
    pass_box.send_keys(teacher_password)
    time.sleep(4)

    # advance button:
    advance_2 = driver.find_element(By.ID, "passwordNext")
    print("found it.")
    time.sleep(1.5)
    advance_2.click()
    time.sleep(4.5)

    # get student portal link again because sometimes the previous page gets stuck
    driver.get(cohort_link)
    time.sleep(3.5)
    logger.info("Sucessfully accessed campus tools website!")

    return driver

def get_macro_student_table(
    driver : webdriver
    )-> pd.DataFrame():
    """
    Based on the main table of student progress, creates a dataframe with students name, 
        number of completed required labs and total number of required labs.
        
    Args:
        - driver (webdriver): driver instance pointing to campus tools 
        course progress
        
    Returns:
        - labs_dataframe : table with students macro results.
    """
    
    time.sleep(7)
    # table with all students course progress
    students_table = (
        driver.find_element(
            By.CSS_SELECTOR,
            "div[class^='ra-field ra-field-undefined']")
    )

    # grab only table body
    students_table_body = (
        students_table.find_element(
            By.CSS_SELECTOR,
            "tbody[class^='MuiTableBody-root datagrid-body']")
    )
 
    logger.info("Starting getting macro student table.")

    # store html of driver
    html_table = students_table_body.get_attribute('outerHTML')

    soup = BeautifulSoup(html_table, 'html.parser')

    # images url
    images_url = soup.find_all('img', attrs = {'class':'MuiAvatar-img'})
    images_url = [image_link['src'] for image_link in images_url]

    # remaining student info
    students_info = soup.find_all("span", attrs = {'class':'MuiTypography-root MuiTypography-body2'})

    students_name = []
    unit_progress = []
    req_completed_labs = []
    for i in range(0, len(students_info), 5):
        group = students_info[i:i+5]
        students_name.append(group[0].text)
        unit_progress.append(group[2].text)
        req_completed_labs.append(group[3].text)

    labs_dataframe = pd.DataFrame(
            {'student_name': students_name,
            'required_labs_completion': req_completed_labs,
            'student_image_url': images_url
            }
    )

    labs_dataframe = (
        labs_dataframe.
        assign(completed_required_labs = labs_dataframe['required_labs_completion'].str.split('/').str[0]).
        assign(total_required_labs = labs_dataframe['required_labs_completion'].str.split('/').str[-1]).
        drop(columns = "required_labs_completion").
        astype({"completed_required_labs":int, "total_required_labs":int })
    )
    
    labs_dataframe["completion_pctg"] = (
        round(labs_dataframe['completed_required_labs'] / labs_dataframe['total_required_labs'], 2)
    )
        
    logger.info("Finished creating student table.")

    return labs_dataframe


def create_students_table(
    students_list : list,
    driver : webdriver,
    )-> pd.DataFrame() :
    """
    Iterates student by student, opening and closing a new tab for each student,
        to collect their submission statuses, delivery dates, lab names and
        lab required marks. Returns a main dataframe containing this information for
        all students.
    
    Args: 
        students_list : List of all bootcamp students name.
        driver : selenium instance that locates in the main page of students assignments.
    
    Returns:
        all_students_table : table with information regarding lab submission for
            all students.
    """

    # main window handle
    wait = WebDriverWait(driver, 10)
    original_window = driver.current_window_handle

    # find students rows
    students_rows = driver.find_elements(By.CSS_SELECTOR,"tr[class^='MuiTableRow-root jss']")
    print(f'Found {len(students_rows)-1} students. Starting iteration through each of them.')

    # loop each student tab
    all_students_table = pd.DataFrame()
    for i in range(1, len(students_rows)):
        # open student page 
        students_rows[i].click()

        # wait until there's a new tab or window
        wait.until(EC.number_of_windows_to_be(2))

        #switch driver to new tab
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        time.sleep(5)

        student_table = driver.find_element(By.CSS_SELECTOR, "div[class^='ra-field ra-field-course.deliveries']") 

        html_table = student_table.get_attribute('outerHTML')

        soup = BeautifulSoup(html_table, 'html.parser')

        # soup driver
        all_table_elements = soup.find_all("td")

        lab_name = []
        status = []
        submission_date = []

        for table_index in range(0, len(all_table_elements), 7):
            group = all_table_elements[table_index:table_index+7]
            lab_name.append(group[0].text)
            status.append(group[2].text)
            submission_date.append(group[4].text)
            
            
        students_df = pd.DataFrame(
            {'lab_name': lab_name,
            'lab_status': status,
            'submission_date': submission_date
            }
        )

        students_df["student_name"] = students_list[i-1]

        all_students_table = pd.concat([all_students_table, students_df])

        print(f'finished appending data for student {students_list[i-1]}.')

        # close the tab or window
        driver.close()

        # switch back to the old tab or window
        driver.switch_to.window(original_window)

        time.sleep(7)
    logger.info("Terminated collecting lab statuses for all students.")

    return all_students_table


def clean_students_table(
    students_df : pd.DataFrame
    ) -> pd.DataFrame :
    """
    Cleans and structures all_students_table DataFrame.
    
    Args:
        all_students_table : DataFrame with students lab submissions information.
    
    Returns:
        students_df : Cleaned and transformed all_students_table DataFrame.
    """

    students_df = (
        students_df.
        assign(lab = students_df["lab_name"].str.split("Required").str[0]).
        assign(required = (
            students_df["lab_name"].
            str.contains("Required").
            replace(True,"Required").
            replace(False, "Optional")
            )
        ).
        drop(columns="lab_name")
    )

    students_cols = ['student_name', 'lab', 'required', 'lab_status', 'submission_date'] 
    students_df = students_df[students_cols]

    logger.info("Finished cleaning students dataframe.")
    return students_df
