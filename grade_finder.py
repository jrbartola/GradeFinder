__author__ = 'Jesse'

import sys
import mechanize
import cookielib
from bs4 import BeautifulSoup

def moodle_login(username, password):
    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)

    moodle_url = 'https://moodle.umass.edu/login/index.php'

    br.open(moodle_url)
    br.select_form(nr=0)

    br.form['j_username'] = username
    br.form['j_password'] = password
    br.submit()
    br.select_form(nr=0)
    br.submit()

    # Now we should be on the login page
    if br.geturl() != 'https://moodle.umass.edu/':
        print("Could not log in for some reason. Aborting...")
        return

    br.open('https://moodle.umass.edu/grade/report/overview/index.php')

    scraping = br.response().read()
    soup = BeautifulSoup(scraping, "html.parser")
    grades = []

    for n in range(0,5):
        grade = soup.select("#grade-report-overview-107960_r" + str(n) + "_c1")[0].text
        class_ = soup.select("#grade-report-overview-107960_r" + str(n) + "_c0 a")[0].text
        print(class_ + ": " + grade)

    # print("Calc 3: " + grades[0].text)
    # print("Physics: " + grades[1].text)
    # print("Physics Lab: " + grades[2].text)
    # print("Compsci 230: " + grades[3].text)
    # print("Compsci 250: " + grades[4].text)


#moodle_l

if __name__ == "__main__":
    if len(sys.argv[1:]) != 2:
        print("\nYou must specify a username and password for moodle.\n")
        print("Usage: \n\tpython grade_finder.py <username> <password>")
    else:
        moodle_login(sys.argv[1:][0], sys.argv[1:][1])