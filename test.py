from github_crawler import get_args, transform_args, crawl, export_json


def test_get_args(mocker):
    mocker.patch("sys.argv", ["test", "./input_example.json"])
    keywords_list, proxies_list, type_str = get_args()
    assert all([a == b for a, b in zip(keywords_list, ["openstack", "nova", "css"])])
    assert all([a == b for a, b in zip(proxies_list, ["194.126.37.94:8080", "13.78.125.167:8080"])])
    assert type_str == "Repositories"


def test_transform_args():
    proxies_list = ["194.126.37.94:8080", "13.78.125.167:8080"]
    assert next(iter(transform_args(proxies_list).values())) in proxies_list


def test_crawl_issues():
    keywords_list = ["aviones", "python", "css"]
    proxy_dict = {'http': '194.126.37.94:8080', 'http': '13.78.125.167:8080'}
    type_str = "Issues"
    assert len(crawl(keywords_list, proxy_dict, type_str)) == 1
    assert [{'url': 'https://github.com/ZR-TECDI/zrstats/issues/13'}] == crawl(keywords_list, proxy_dict, type_str)


def test_crawl_repositories():
    keywords_list = ["openstack", "nova", "css"]
    proxy_dict = {'http': '194.126.37.94:8080', 'http': '13.78.125.167:8080'}
    type_str = "Repositories"
    assert len(crawl(keywords_list, proxy_dict, type_str)) == 2
    assert all([a == b for a, b in zip(crawl(keywords_list, proxy_dict, type_str),
                                       [{'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'},
                                        {'url': 'https://github.com/michealbalogun/Horizon-dashboard'}])])


def test_crawl_wikis():
    keywords_list = ["superman", "python", "españa"]
    proxy_dict = {'http': '194.126.37.94:8080', 'http': '13.78.125.167:8080'}
    type_str = "Wikis"
    assert len(crawl(keywords_list, proxy_dict, type_str)) == 1
    assert [{'url': 'https://github.com/lucanag/emotet/wiki/password-list'}] == crawl(keywords_list, proxy_dict, type_str)
