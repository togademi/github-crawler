from github_crawler import (get_args, transform_args, get_tree, crawl_search_results, crawl_repository_page,
                            process_html_data)


def test_get_args(mocker):
    mocker.patch("sys.argv", ["test", "./input_example.json"])
    keywords_list, proxies_list, type_str = get_args()
    assert all([a == b for a, b in zip(keywords_list, ["openstack", "nova", "css"])])
    assert all([a == b for a, b in zip(proxies_list, ["194.126.37.94:8080", "13.78.125.167:8080"])])
    assert type_str == "Repositories"


def test_transform_args():
    proxies_list = ["194.126.37.94:8080", "13.78.125.167:8080"]
    assert next(iter(transform_args(proxies_list).values())) in proxies_list


def test_get_tree():
    assert get_tree('https://www.google.com/').__class__.__name__ == 'HtmlElement'


def test_crawl_search_results_repositories():
    keywords_list = ["openstack", "nova", "css"]
    type_str = "Repositories"
    assert ['/atuldjadhav/DropBox-Cloud-Storage',
            '/michealbalogun/Horizon-dashboard'] == crawl_search_results(keywords_list, type_str)


def test_crawl_search_results_issues():
    keywords_list = ["aviones", "python", "css"]
    type_str = "Issues"
    assert ['/ZR-TECDI/zrstats/issues/13'] == crawl_search_results(keywords_list, type_str)


def test_crawl_search_results_wikis():
    keywords_list = ["superman", "python", "españa"]
    type_str = "Wikis"
    assert ['/lucanag/emotet/wiki/password-list'] == crawl_search_results(keywords_list, type_str)


def test_crawl_repository_page():
    path = '/atuldjadhav/DropBox-Cloud-Storage'
    assert ['CSS 52.0', 'JavaScript 47.2', 'HTML 0.8'] == crawl_repository_page(path)


def test_process_html_data_repositories():
    html_data_search = ['/atuldjadhav/DropBox-Cloud-Storage', '/michealbalogun/Horizon-dashboard']
    type_str = "Repositories"
    assert process_html_data(html_data_search, type_str) == \
           [{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
             'extra': {'owner': 'atuldjadhav', 'language_stats': {'CSS': 52.0, 'JavaScript': 47.2, 'HTML': 0.8}}},
            {'url': 'https://github.com/michealbalogun/Horizon-dashboard',
             'extra': {'owner': 'michealbalogun', 'language_stats': {'Python': 100.0}}}]


def test_process_html_data_other():
    html_data_search = ['/atuldjadhav/DropBox-Cloud-Storage', '/michealbalogun/Horizon-dashboard']
    type_str = "Issues"
    assert process_html_data(html_data_search, type_str) == [{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'}, {'url': 'https://github.com/michealbalogun/Horizon-dashboard'}]
