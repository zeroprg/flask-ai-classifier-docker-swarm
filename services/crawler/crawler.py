import requests
from bs4 import BeautifulSoup
import re

from reg_express import accumulate_regexes

def search_and_traverse_urls(file_name):
    # load websites list from file
    with open(file_name, "r") as f:
        websites = f.read().splitlines()

    regex_dict = accumulate_regexes()
    all_urls = set()
    visited = set()
    image_urls = []

    # loop over websites
    for website in websites:
        for operator, value in regex_dict.items():
            if operator == "inurl":
                # search for URLs that contain the pattern
                urls = [url for url in websites if value in url]
            else:
                # send GET request to website
                res = geSession().get(url).get(website)
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
                all_urls.add(url)
                traverse_internal_urls(url, visited, regex_dict, image_urls)
    return all_urls, image_urls

def geSession():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    
    session = requests.Session()
    session.headers.update(headers)
    return session;

def traverse_internal_urls(url, visited, regex_dict, image_urls):
    visited.add(url)
    print(url)   

    res = geSession().get(url)
        
    soup = BeautifulSoup(res.text, "html.parser")
    internal_urls = [a["href"] for a in soup.select("* a[href^='/']")]
    print("internal_urls : {} ".format(internal_urls))
    images = [img["src"] for img in soup.select("* img[src]")]
    print("images : {} ".format(images))
    for operator, regex in regex_dict.items():
        print("regex: ".format(regex))
        if operator == "inurl":
            # search for URLs that contain the pattern
            found_urls = [img for img in images if any(re.search(regex_pattern, img) for regex_pattern in regex)]            
            image_urls += found_urls
            
        if operator == "inip":
            # search for URLs that contain the pattern
            found_urls = [img for img in images if any(re.search(regex_pattern, img) for regex_pattern in regex)]
            image_urls += found_urls
            
    print(image_urls)
    for internal_url in internal_urls:
        if internal_url not in visited:
            if internal_url.startswith("/"):
                internal_url = url + internal_url
            traverse_internal_urls(internal_url, visited, regex_dict, image_urls)

def test_search_and_traverse_urls():
    # Test 1: Check if search_and_traverse_urls is able to search all urls in a file and traverse internal urls
    file_name = "test_websites.txt"
    with open(file_name, "w") as f:
        f.write("www.example.com\nwww.test.com")

    expected_urls = set(["www.example.com", "www.example.com/internal", "www.test.com", "www.test.com/internal"])

    all_urls,_ = search_and_traverse_urls("test_websites.txt")
    assert all_urls == expected_urls

def test_traverse_internal_urls():
    # Test 1: Check if traverse_internal_urls is able to traverse internal urls and find images
    regex_dict = accumulate_regexes()

    visited = set()
    image_urls = []
    traverse_internal_urls("http://insecam.org", visited, regex_dict, image_urls)
    assert len(image_urls) == 2


if __name__ == '__main__':
    test_traverse_internal_urls()