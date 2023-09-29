import json
import pytest
from github_crawler import GitHubCrawler

test_configs = [
    {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Repositories"
    },
    {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Issues"
    },
    {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Wikis"
    },
    {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "blablabla"
    },
]

@pytest.mark.parametrize("config_json", test_configs)
def test_github_crawler(config_json):
    config_json = json.dumps(config_json)
    github_crawler = GitHubCrawler(config_json)

    config_dict = json.loads(config_json)
    result_urls = github_crawler.perform_github_search()
    result_data = json.loads(result_urls)
    
    # Assert that the result is a list
    assert isinstance(result_data, list)

    for result in result_data:
        # Assert that for every search type we can extract the url
        assert "url" in result

        # Assert that only the "Repository" search type extracts the extra information
        if config_dict['search_type'] == 'Repositories':
            assert "extra" in result
            extra_info = result.get("extra", {})
            assert "owner" in extra_info
            assert "language_stats" in extra_info
        else :
            assert "extra" not in result

        # Assert that the output shows a customized error when the type of search is unknown
        valid_search_types = ['repositories', 'issues', 'wikis']
        if config_dict['search_type'].lower() not in valid_search_types:
            assert result == {"url": 'search_type_ERROR'}


# Assert that the Selenium web driver initializes successfully
def test_initialize_selenium():
    config = {
        "search_keywords": ["openstack", "nova", "css"],
        "proxy_list": ["http://82.67.20.218:3129", "http://51.15.242.202:8888"],
        "search_type": "Repositories"
    }
    json_config = json.dumps(config)
    github_crawler = GitHubCrawler(json_config)
    driver = github_crawler.initialize_selenium("http://82.67.20.218:3129")

    assert driver is not None
    driver.quit()
        
if __name__ == "__main__":
    pytest.main()
