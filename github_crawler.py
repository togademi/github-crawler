from datetime import datetime
import json
from lxml import html
import random
import requests
import sys


def get_args():
    """
    Read variables from the JSON passed as argument
    :return: The input to our program: list of keywords, list of proxies and type of data to search for on GitHub
    """
    input_filename = sys.argv[1]
    try:
        with open(input_filename) as input_json:
            args = json.load(input_json)
    except Exception as e:
        print(e)

    keywords_list = args.get('keywords')
    proxies_list = args.get('proxies')
    search_type = args.get('type')
    if search_type.lower() not in ['repositories', 'issues', 'wikis']:
        raise ValueError(f'Type "{search_type}" unsupported, only repositories, issues or wikis.')

    return keywords_list, proxies_list, search_type


def transform_args(proxies_list):
    """
    Transform the input list of proxies in a dictionary to be accepted by requests.get()
    :param proxies_list: List of proxies (strings)
    :return: Dictionary in the form of {'http': <random proxy of the list>}
    """
    proxy_index = random.randint(0, len(proxies_list) - 1)
    return {"http": proxies_list[proxy_index]}


def get_tree(url):
    """
    Get the HTML scheme of a page
    :param url: URL of the page to get the HTML from
    :return: The HTML of the page as a lxml.html.HtmlElement object
    """
    try:
        page = requests.get(url, proxies=PROXY_DICT)
    except NameError:
        page = requests.get(url)
    return html.fromstring(page.content)


def crawl_search_results(keywords_list, search_type):
    """
    Get the partial path of the search results on GitHub for repositories, issues or wikis
    :param keywords_list: List of terms to search for
    :param search_type: Type of data to search for (repositories, issues or wikis)
    :return: html_data, a list of partial paths (list of strings)
    """
    url = "https://github.com/search?q="
    for keyword in keywords_list:
        url += f"{keyword}+"
    url += f"&type={search_type}"

    tree = get_tree(url)

    if search_type == 'Issues':
        html_data = tree.xpath('//div[@class="f4 text-normal markdown-title"]//@href')
    elif search_type == 'Repositories':
        html_data = tree.xpath('//a[@class="v-align-middle"]//@href')
    elif search_type == 'Wikis':
        html_data = tree.xpath('//div[@class="f4 text-normal"]//@href')

    if not html_data:
        print("No results found.")
        sys.exit(0)

    return html_data


def crawl_repository_page(path):
    """
    Get the languages used in a repository and their percentage of appearance
    :param path: Partial path of a repository (/<username>/<repository-name>/)
    :return: html_data, a list of languages and their percentage, like: ['Python 31.0', 'Java 9.0', 'C 60.0']
    """
    url = f"https://github.com/{path}"
    tree = get_tree(url)
    html_data = tree.xpath('//div[@class="mb-2"]//@aria-label')
    return html_data


def process_html_data(html_data_search, search_type):
    """
    Convert the crawled data into formatted dictionaries. Crawl for extra data when processing repositories
    :param html_data_search: List of partial paths of the URLs of search results
    :param search_type: Type of data to search for (repositories, issues or wikis)
    :return: processed_data, a list of dictionaries with each search result
    """
    processed_data = [{'url': f"https://github.com{item}"} for item in html_data_search]

    if search_type == "Repositories":
        owner_list = [item.split('/')[1] for item in html_data_search]
        for i in range(len(processed_data)):
            language_stats = crawl_repository_page(html_data_search[i])
            language_stats_copy = []

            # convert 'language percentage' (str) into {language: percentage} (dict)
            for item in language_stats:
                language_stats_copy.extend(item.split())
            language_stats_dict = {language_stats_copy[i]: float(language_stats_copy[i + 1]) for i in
                                   range(0, len(language_stats_copy), 2)}
            processed_data[i]["extra"] = {"owner": owner_list[i],
                                          "language_stats": language_stats_dict}

    return processed_data


def export_json(data):
    """
    Save the processed data into a JSON file
    :param data: Processed data in a format of list of dicts, parsable by JSON
    :return: None
    """
    now = datetime.now().strftime("%Y%m%d_%I%M%S")
    with open(f"output_github_crawler_{now}.json", "w+") as output_file:
        json.dump(data, output_file)


if __name__ == '__main__':
    keywords_list, proxies_list, search_type = get_args()
    PROXY_DICT = transform_args(proxies_list)

    html_data_search = crawl_search_results(keywords_list, search_type)
    processed_data = process_html_data(html_data_search, search_type)

    export_json(processed_data)
