# IH DA RMT Labs Control

![IH logo](/res/ironhack_logo.png)

### Repo for automation of Labs, improving productivity of TA's and allowing a better follow-up of student's labs and needs.

#### With this repo, all this tasks are going to be taken care of:

- Check on a weekly basis, student submission of labs;
- Track of unsubmitted labs;
- Submission rate until the 80% for aproving students;
- Submission rate of the total available and mandatory labs;
- Sending e-mails to the students with their KPI's

## Motivation:

- IH Data Analytics PT RMT Courses take 6 months to complete, having in the meantime around 34 labs that the students are asked to complete.
- Checking submissions, following up and keeping track of their submission rates takes a fair amount of time on a weekly basis.
- Based on the advances that the TA's of Lisbon have done, we picked their scripts and created a new one, specifically made for Remote DA Cohorts.

## Project Structure:

- Scraper that enters IH Campus Software and retrieves info regarding student submissions.
- Script that creates a DataFrame and updates for each student, week and lab if they have submitted or not.
- Script that sends e-mails to all of the students

**Project Owners**: 
- Gonçalo Jardim - TA
- Miguel Simón - TA
- Supervised by: David Henriques - LT

## User Guide:

### Environment and dependencies:

1. Clone this repo to your personal GitHub account.
2. If you are not in this directory already, `cd` into it.
3. Create a virtual environment with `python -m venv .venv`
4. Activate the virtual environment with source `.venv/bin/activate` or `.venv\Scripts\activate` on Windows
5. Install its dependencies on editable mode with `pip install -e .[dev]` OR `python -m pip install .`  .
