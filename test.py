import pytest
from github_crawler import (get_args, transform_args, get_tree, crawl_search_results, crawl_repository_page,
                            process_html_data)


def test_get_args(mocker):
    """
    Read a JSON file and try to assign its values to variables
    - OK: the values are properly assigned to the variables
    """
    mocker.patch("sys.argv", ["test", "./test_input_scenarios/test_input_scenario.json"])
    keywords_list, proxies_list, search_type = get_args()
    assert all([a == b for a, b in zip(keywords_list, ["openstack", "nova", "css"])])
    assert all([a == b for a, b in zip(proxies_list, ["194.126.37.94:8080", "13.78.125.167:8080"])])
    assert search_type == "Repositories"


def test_get_args_read_error(mocker):
    """
    Read a faulty JSON file and try to assign its values to variables
    - OK: the function raises a general Exception
    """
    mocker.patch("sys.argv", ["test", "./test_input_scenarios/test_input_scenario_error_read.json"])
    with pytest.raises(Exception):
        keywords_list, proxies_list, search_type = get_args()


def test_get_args_value_error(mocker):
    """
    Read a faulty JSON file and try to assign its values to variables
    - OK: the function raises a ValueError
    """
    mocker.patch("sys.argv", ["test", "./test_input_scenarios/test_input_scenario_error_value.json"])
    with pytest.raises(ValueError):
        keywords_list, proxies_list, search_type = get_args()


def test_transform_args():
    """
    Input a list of proxies and get a dictionary with only one random proxy
    - OK: the result is a dictionary and its proxy is in the input list
    """
    proxies_list = ["194.126.37.94:8080", "13.78.125.167:8080"]
    assert next(iter(transform_args(proxies_list).values())) in proxies_list


def test_get_tree():
    """
    Request a page
    - OK: the page is of the HtmlElement type
    """
    assert get_tree('https://www.google.com/').__class__.__name__ == 'HtmlElement'


def test_crawl_search_results_repositories():
    """
    Crawl the Github search results for repositories
    - OK: the values returned are the ones we expect
    """
    keywords_list = ["openstack", "nova", "css"]
    search_type = "Repositories"
    assert ['/atuldjadhav/DropBox-Cloud-Storage',
            '/michealbalogun/Horizon-dashboard'] == crawl_search_results(keywords_list, search_type)


def test_crawl_search_results_issues():
    """
    Crawl the Github search results for issues
    - OK: the values returned are the ones we expect
    """
    keywords_list = ["aviones", "python", "css"]
    search_type = "Issues"
    assert ['/ZR-TECDI/zrstats/issues/13'] == crawl_search_results(keywords_list, search_type)


def test_crawl_search_results_wikis():
    """
    Crawl the Github search results for wikis
    - OK: the values returned are the ones we expect
    """
    keywords_list = ["superman", "python", "españa"]
    search_type = "Wikis"
    assert ['/lucanag/emotet/wiki/password-list'] == crawl_search_results(keywords_list, search_type)


def test_crawl_search_results_unicode():
    """
    Crawl the Github search results, searching for weird unicode characters
    - OK: the function doesn't fail
    """
    keywords_list = ["邏樂洛", "✈✉✌"]
    search_type = "Issues"
    assert type(crawl_search_results(keywords_list, search_type)) is list


def test_crawl_search_results_no_results_found():
    """
    Crawl the Github search results, but no result is found
    - OK: the function exits with code 0
    """
    keywords_list = ["grgaf3444", "cvavs", "4dccc"]
    search_type = "Repositories"
    with pytest.raises(SystemExit) as e:
        crawl_search_results(keywords_list, search_type)
    assert e.type == SystemExit
    assert e.value.code == 0


def test_crawl_repository_page():
    """
    Crawl a Github repository for its language stats
    - OK: the values returned are the ones we expect
    """
    path = '/atuldjadhav/DropBox-Cloud-Storage'
    assert ['CSS 52.0', 'JavaScript 47.2', 'HTML 0.8'] == crawl_repository_page(path)


def test_process_html_data_repositories():
    """
    Transform the data (of type repositories) we crawled into formatted dictionaries
    - OK: the values returned are the ones we expect
    """
    html_data_search = ['/atuldjadhav/DropBox-Cloud-Storage', '/michealbalogun/Horizon-dashboard']
    search_type = "Repositories"
    assert process_html_data(html_data_search, search_type) == \
           [{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
             'extra': {'owner': 'atuldjadhav', 'language_stats': {'CSS': 52.0, 'JavaScript': 47.2, 'HTML': 0.8}}},
            {'url': 'https://github.com/michealbalogun/Horizon-dashboard',
             'extra': {'owner': 'michealbalogun', 'language_stats': {'Python': 100.0}}}]


def test_process_html_data_other():
    """
    Transform the data (of type other than repositories, in this case issues) we crawled into formatted dictionaries
    - OK: the values returned are the ones we expect
    """
    html_data_search = ['/atuldjadhav/DropBox-Cloud-Storage', '/michealbalogun/Horizon-dashboard']
    search_type = "Issues"
    assert process_html_data(html_data_search, search_type) == [
        {'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'},
        {'url': 'https://github.com/michealbalogun/Horizon-dashboard'}]
