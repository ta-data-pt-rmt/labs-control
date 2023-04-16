"""Specify project settings, such as student names, emails, 
constant paths and current week number"""
import pathlib
import logging

# main path
DATA_PATH =  pathlib.Path().parent
SECRETS_PATH =  pathlib.Path().resolve() / 'secrets'

# cohort main teaching ironhack email
TEACHING_EMAIL = "ta-data-pt-rmt@ironhack.com"

# cohort main teaching ironhack email
SENDING_EMAIL = "ta.data.ironhack@gmail.com"

# cohort campus tools link:
COHORT_LINK = "https://campus-tools.ironhack.com/#/cohorts/6308c6dca5eeff002c60c2bc/show/course_progress/students"

# cohort student emails
# !Important- Use the exact names that appear on student portal:
STUDENT_EMAILS = {
    "Andreia Jardim" : "jardim.andreia@outlook.pt",
    "André Fontoura Faria" : "fontourafaria@hotmail.com",
    "Anna Schemuth" : "anna.schemuth@gmail.com",
    "David Santos" : "vonfiggy@icloud.com",
    "Erica Saito Neves" : "ericaneves.mkt@gmail.com",
    "Flor Maria Roa" : "florma67@gmail.com",
    "Geetu -" : "geetver10@gmail.com",
    "Iñigo Auzmendi" : "iauzmendipinedo@gmail.com",
    "Kathryn Nicholson" : "kgcnkgcn@gmail.com",
    "Marcello Gelormini" : "marcello.gelormini@gmail.com",
    "Mario Carmona Rodríguez" : "carmonarodriguez.mario@gmail.com",
    "Marta Fernández Piñeiro" : "martafp11@gmail.com",
    "Miquele Luce" : "miquelemelo@gmail.com",
    "Sabir Kerimov" : "sabirkmv99@gmail.com",
    "Vladimir Tesar" : "tsrvldmr@gmail.com"
}

# dropped students - place here students that are moved out of the bootcamp
DROPPED_STUDENTS = []

# number of bootcamp weeks
BOOTCAMP_WEEKS = 26

WEEKS_DICT = {
    'Week 1': ['Lab Strings', 'Lab Dicts, sets, tuples', 'Lab Lists', 'Lab Git'],
    'Week 2': [
        'Lab DataFrame Calculations','Lab Data Cleaning',
        'Lab Import-Export','Lab Intro to pandas'],
    'Week 3': ['Lab Descriptive Stats', 'Lab Advanced Pandas'],
    'Week 4': [
        'Lab Regression Analysis', 'Lab Matplotlib & Seaborn',
        'Lab Subsetting and Descriptive Stats'],
    'Week 6': ['Lab MySQL Actions', 'Lab MySQL First Queries'],
    'Week 7': [
        'Lab MySQL Select', 'Lab Advanced MySQL | Optional'],
    'Week 8': [
        'Lab Map-Reduce-Filter | OPTIONAL', 'Lab Lambda Functions | Optional'],
    'Week 9': ['Lab API Scavenger', 'Lab Web Scraping'],
    'Week 10': ['Lab StackAPI | OPTIONAL'],
    'Week 11': ['Lab Parallelization | Optional', 'Lab Confidence Intervals',
                'Lab Pandas Deep-dive'],
    'Week 12': ['Lab Advanced Charts - Tableau [OPTIONAL]',
                'Lab BI Analysis - Tableau', 'Lab Intro to BI - Tableau'],
    'Week 13': ['Lab Goodness of Fit', 'Lab Hypothesis Testing 1',
                'Lab Hypothesis Testing 2','Lab Pivot Tables | Optional'],
    'Week 15': ['Lab Intro  to Probability [OPTIONAL]'], 
    'Week 18': ['Lab Intro to AI'],
    'Week 19': ['Lab Imbalance', 'Lab Supervised Learning - Regression',
    'Lab Supervised Learning - Classification', 'Lab Feature Extraction'],
    'Week 21': ['Lab Unsupervised Learning', 'Lab Problems in ML'],
    'Week 22': ['Lab NLP', 'Lab Deep Learning']
}

# setting up logging configuration
logging.basicConfig(level=logging.INFO)