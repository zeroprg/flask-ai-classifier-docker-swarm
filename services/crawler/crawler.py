
from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urlparse
from collections import deque


from project import db, populate_urls_in_db, geSession, read_info, url_to_filename, store_info

logging.basicConfig(level=logging.DEBUG)
from reg_express import accumulate_regexes

# global list of urls which store info from db
urls = []
def search_and_traverse_urls(file_name):
    global urls
    # load websites list from file
    with open(file_name, "r") as f:
        websites = f.read().splitlines()

    regex_dict = accumulate_regexes()
    
    raws = db.select_all_urls()
    for raw in raws:
        urls.append(raw['url'])
        
    # loop over websites
    for website in websites:
        filename = url_to_filename(website)
        last_visit_url, visited_urls = read_info(filename)
        if( last_visit_url is not None): website = last_visit_url
        traverse_internal_urls(website, visited_urls, regex_dict)


def traverse_internal_urls(url, visited_urls, regex_dict):
    visited = set(visited_urls)
    stack = deque([(url, visited)])
    domain = None
    while stack:
        url, visited = stack.pop()

        visited.add(url)
        print("visited:{}".format(visited))
        logging.info(url)

        if domain is None:
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            domain = scheme + "://" + parsed_url.netloc
            logging.info("domain: " + domain)

        print("url: {}".format(url))
        res = geSession().get(url)

        soup = BeautifulSoup(res.text, "html.parser")
        internal_urls = [domain + a["href"] for a in soup.select("* a[href^='/']")]
        images = [img["src"] for img in soup.select("* img[src]")]

        for operator, regex in regex_dict.items():

            if operator == "inurl":
                found_urls = [img for img in images if any(re.search(regex_pattern, img) for regex_pattern in regex)]

                for found_url in found_urls:
                    parsed_found_url = urlparse(found_url)
                    found_domain = parsed_found_url.netloc.split(':')[0]
                    if not any(found_domain == urlparse(url).netloc.split(':')[0] for url in urls):
                        populate_urls_in_db(found_url)

            found_ips = [img for img in images if bool(re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", img))]
            for found_url in found_ips:
                parsed_found_url = urlparse(found_url)
                found_domain = parsed_found_url.netloc.split(':')[0]
                print(found_domain)
                if not any(found_domain == urlparse(url).netloc.split(':')[0] for url in urls):
                    populate_urls_in_db(found_url)




        print(internal_urls)
        for internal_url in internal_urls:
            if internal_url.endswith("/"):
                internal_url = internal_url[:-1]
            print("internal_url: {} ".format(internal_url))
            if internal_url not in visited:                
                #store_info(url_to_filename(domain), internal_url, visited)
                stack.append((internal_url, visited.copy()))
    
    
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
   
    traverse_internal_urls("http://www.insecam.org", visited, regex_dict)
    


if __name__ == '__main__':
    search_and_traverse_urls("websites")
    #test_traverse_internal_urls()