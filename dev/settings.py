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

# cohort student emails
# !Important- Use the exact names that appear on student portal:
STUDENT_EMAILS = {
    "Adrian Flores" : "adrianfg88@gmail.com",
    "Aferdita Zherka Zherka" : "zherka.aferdita@outlook.com",
    "Alicia Andrés" : "aliciaandressalguero@gmail.com",
    "Amelie Haberland" : "amelie.haberland@ironhack.com",
    "Angela Arredondo Mendoza" : "angela.arredondo99@gmail.com",
    "Damiano Serra" : "damsvpn@protonmail.com",
    "Daniel J Mendez Borges" : "djmborges92@gmail.com",
    "Fabio Blank Da Costa" : "fabioblankc@gmail.com",
    "Federico Cavanagh" : "fedecavanagh@live.com",
    "Francisco Javier De Las Heras Jimenez" : "javierherasjimenez@hotmail.com",
    "Gregor Seegers" : "gregor.seegers@gmail.com",
    "Joaquin Valentin" : "quino117@hotmail.com",
    "Manouk Meilof" : "manoukmeilof@gmail.com",
    "Marc Gavaldà" : "gavalda.marc@gmail.com",
    "María Vázquez Casares" : "maria.vazquez.casares@gmail.com",
    "Max Grempel" : "maximilian.grempel@gmail.com",
    "Shilei Tan Tan" : "tanshilei@gmail.com",
    "Óscar Iglesias Roqueiro" : "roque.ourense@gmail.com",
    "Suparna Mandal" : "suparna.sahoo@gmail.com",
    "Vanessa Andrade" : "anvergara95@gmail.com"
}

# dropped students - place here students that are moved out of the bootcamp
DROPPED_STUDENTS = [
    "Manouk Meilof"
]

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
        'Lab MySQL Select', 'Lab Advanced MySQL | Optional',
        'Lab Advanced MySQL | Optional'],
    'Week 8': [
        'Lab API Scavenger','Lab Web Scraping',
        'Lab Map-Reduce-Filter | OPTIONAL', 'Lab Lambda Functions | Optional'],
    'Week 9': ['Lab StackAPI | OPTIONAL'],
    'Week 10': [
        'Lab Confidence Intervals','Lab Pandas Deep-dive',
        'Lab Parallelization | Optional'],
    'Week 11': [
        'Lab BI Analysis - Tableau', 'Lab Intro to BI - Tableau', 
        'Lab Advanced Charts - Tableau [OPTIONAL]'],
    'Week 12': [
        'Lab Goodness of Fit', 'Lab Hypothesis Testing 2',
        'Lab Hypothesis Testing 1', 'Lab Pivot Tables | Optional'],
    'Week 14': ['Lab Intro  to Probability [OPTIONAL]'], 
    'Week 18': ['Lab Feature Extraction', 'Lab Intro to AI'],
    'Week 19': ['Lab Imbalance', 'Lab Supervised Learning - Regression',
    'Lab Supervised Learning - Classification'],
    'Week 21': ['Lab Unsupervised Learning', 'Lab Problems in ML'],
    'Week 22': ['Lab NLP', 'Lab Deep Learning']
}

# setting up logging configuration
logging.basicConfig(level=logging.INFO)