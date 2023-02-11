import requests
from bs4 import BeautifulSoup
from reg_express import accumulate_regexes

# load websites list from file
with open("websites.txt", "r") as f:
    websites = f.read().splitlines()

regex_dict = accumulate_regexes()

# loop over websites
for website in websites:
    for operator, value in regex_dict.items():
        if operator == "inurl":
            # search for URLs that contain the pattern
            urls = [url for url in websites if value in url]
        else:
            # send GET request to website
            res = requests.get(website)
            # parse HTML content
            soup = BeautifulSoup(res.text, "html.parser")
            
            if operator == "intitle":
                # find all URLs with the pattern in the title
                urls = [url for url in websites if value in soup.title.string]
            elif operator == "intext":
                # find all URLs with the pattern in the text content
                urls = [url for url in websites if value in soup.get_text()]
            elif operator == "site":
                # find all URLs that belong to the specified website
                urls = [url for url in websites if website in url]
        
        # print found URLs
        print(f"Urls for operator {operator} and value {value}:")
        for url in urls:
            print(url)
