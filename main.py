import requests
import bs4


def job_parser(url: str) -> list:
    res = requests.get(url)
    res.raise_for_status()

    job_descript = bs4.BeautifulSoup(res.text, "html.parser")
    # element = job_descript.select("li")
    element = job_descript.select("#jobDescriptionText li, #jobDescriptionText p")
    print(len(element))

    bullet_list = [bullet.getText() for bullet in element]
    return bullet_list


job = job_parser(
    "https://www.indeed.com/viewjob?cmp=AAA-AIR-SUPPORT,"
    "-INC&from=iaBackPress&jk=3896b9504d7af1b0"
)
for i, part in enumerate(job):
    print(i, part)
