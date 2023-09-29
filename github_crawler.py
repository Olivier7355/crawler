"""
Crawler that implements the GitHub search and returns all the links from the search result 
as well as the owner of each repository and the language stats.
"""

import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class GitHubCrawler:
    def __init__(self, configuration):
        config = json.loads(configuration)
        self.search_keywords = config["search_keywords"]
        self.proxy_list = config["proxy_list"]
        self.search_type = config["search_type"]

    def initialize_selenium(self, proxy):
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={}'.format(proxy))
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        try :
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        except :
            print('Error loading ChromeDriver.')
        
        return driver
    
    def crawl_extra_information(self, profile_url, selected_proxy):
        data = {'owner':{},'language_stats':{}}

        driver = self.initialize_selenium(selected_proxy)
        driver.get(profile_url)

        try :
            owner = driver.find_element(By.CSS_SELECTOR, 'span.author a.url.fn')
            data['owner'] = owner.text
            languages = driver.find_elements(By.CSS_SELECTOR, 'span.color-fg-default.text-bold')
            percentages = driver.find_elements(By.CSS_SELECTOR, 'li.d-inline a span:last-child')

            for language, percentage in zip(languages, percentages):
                language_name = language.text
                percentage_value = percentage.text
                data['language_stats'][language_name] = float(percentage_value[:-1])
        except :
             print('Some data could not be extracted.')

        time.sleep(3)
        return data

    def perform_github_search(self):
        base_url = "https://github.com"
        keywords = "%20".join(self.search_keywords)
        search_url = f"{base_url}/search?q={keywords}&type={self.search_type}"
        
        selected_proxy = random.choice(self.proxy_list)
        driver = self.initialize_selenium(selected_proxy)
        driver.get(search_url)

        try :
            results = driver.find_elements(By.CSS_SELECTOR, 'div.Box-sc-g0xbh4-0.bBwPjs.search-title > a')
            result_links = [result.get_attribute("href") for result in results]
        except :
            print('Links could not be extracted.')

        result_json = []
        other_valid_search_types = ['issues', 'wikis']

        if self.search_type.lower() == 'repositories' :
            for profile in result_links :
                result_json.append({"url": profile, "extra":self.crawl_extra_information(profile, selected_proxy)})        
        elif (self.search_type.lower() in other_valid_search_types):
            for link in result_links :
                result_json.append({"url": link})
        else :
            result_json.append({"url": 'search_type_ERROR'})

        json_result = json.dumps(result_json, indent=4)

        driver.quit()
        return json_result

if __name__ == "__main__":
    
    config = {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Repositories"
    }
    json_config = json.dumps(config)

    github_crawler = GitHubCrawler(json_config)
    result_urls = github_crawler.perform_github_search()
    print(result_urls)

