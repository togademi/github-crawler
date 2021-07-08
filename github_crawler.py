import json
from lxml import html
import random
import requests
import sys


def get_args():
    input_filename = sys.argv[1]
    with open(input_filename) as input_json:
        args = json.load(input_json)
    keywords_list = args.get('keywords')
    proxies_list = args.get('proxies')
    type_str = args.get('type')
    return keywords_list, proxies_list, type_str


def transform_args(proxies_list):
    proxy_index = random.randint(0, len(proxies_list) - 1)
    return {"http": proxies_list[proxy_index]}


def get_tree(url):
    page = requests.get(url, proxies=PROXY_DICT)
    return html.fromstring(page.content)


def crawl_search_results(keywords_list, proxy_dict, type_str):
    url = "https://github.com/search?q="
    for keyword in keywords_list:
        url += f"{keyword}+"
    url += f"&type={type_str}"

    tree = get_tree(url)

    if type_str == 'Issues':
        html_data = tree.xpath('//div[@class="f4 text-normal markdown-title"]//@href')
    elif type_str == 'Repositories':
        html_data = tree.xpath('//a[@class="v-align-middle"]//@href')
    elif type_str == 'Wikis':
        html_data = tree.xpath('//div[@class="f4 text-normal"]//@href')
    print("-----html_data=",html_data)
    return html_data


def crawl_repository_page(path, proxy_dict):
    url = f"https://github.com/{path}"
    tree = get_tree(url)
    html_data = tree.xpath('//div[@class="mb-2"]//@aria-label')
    print("-----html_data=", html_data)
    return html_data


def process_html_data(html_data_search, type_str, proxy_dict):
    processed_data = [{'url': f"https://github.com{item}"} for item in html_data_search]
    if type_str == "Repositories":
        owner_list = [item.split('/')[1] for item in html_data_search]
        for i in range(len(processed_data)):
            language_stats = crawl_repository_page(html_data_search[i], proxy_dict)
            new_language_stats = []
            for item in language_stats:
                new_language_stats.extend(item.split())
            language_stats_dict = {new_language_stats[i]: float(new_language_stats[i + 1]) for i in range(0, len(new_language_stats), 2)}
            processed_data[i]["extra"] = {"owner": owner_list[i],
                                          "language_stats": language_stats_dict}
    print("-----processed_data=",processed_data)
    return processed_data


def export_json(data):
    with open("output.json", "w+") as output_file:
        json.dump(data, output_file)


if __name__ == '__main__':
    keywords_list, proxies_list, type_str = get_args()
    PROXY_DICT = transform_args(proxies_list)
    html_data_search = crawl_search_results(keywords_list, PROXY_DICT, type_str)
    processed_data = process_html_data(html_data_search, type_str, PROXY_DICT)
    export_json(processed_data)
