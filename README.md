Python script for a GitHub crawler that searches for repositories, issues, or wikis on GitHub based on certain keywords. It uses the Selenium web automation framework to interact with Google Chrome and scrape data from GitHub pages.

**Web scraping and automation may be subject to terms of service and usage policies of websites. Always respect the website's policies and use web scraping responsibly and ethically.**

# How to use the code

 - Install the required Python libraries
   ```
   pip install -r requirements.txt
   ```
 - The script defines a class called **GitHubCrawler** and a method called **perform_github_search()**.
   The method performs the GitHub search based on the configuration. It navigates to the search results page, extracts the links to GitHub profiles or repositories, and, if the search type is "Repositories," it also crawls additional information for each repository.
   ```python
   from github_crawler import GitHubCrawler

   config = {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Repositories"
    }
    json_config = json.dumps(config)

    github_crawler = GitHubCrawler(json_config)
    result_urls = github_crawler.perform_github_search()
   ```
- Examples of output
  ```json
  [
    {
        "url": "https://github.com/atuldjadhav/DropBox-Cloud-Storage",
        "extra": {
            "owner": "atuldjadhav",
            "language_stats": {
                "CSS": 52.0,
                "JavaScript": 47.2,
                "HTML": 0.8
            }
        }
    },
    {
        "url": "https://github.com/michealbalogun/Horizon-dashboard",
        "extra": {
            "owner": "michealbalogun",
            "language_stats": {
                "Python": 100.0
            }
        }
    }
]
