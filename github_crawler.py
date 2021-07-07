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


def crawl(keywords_list, proxy_dict, type_str):
    url = "https://github.com/search?q="
    for keyword in keywords_list:
        url += f"{keyword}+"
    if type_str:
        url += f"&type={type_str}"
    page = requests.get(url, proxies=proxy_dict)
    tree = html.fromstring(page.content)

    if type_str == 'Issues':
        html_data = tree.xpath('//div[@class="f4 text-normal markdown-title"]//@href')
    elif type_str == 'Repositories':
        html_data = tree.xpath('//a[@class="v-align-middle"]//@href')
    elif type_str == 'Wikis':
        html_data = tree.xpath('//div[@class="f4 text-normal"]//@href')
    print("-----html_data=",html_data)

    output_data = [f"https://github.com{item}" for item in html_data]
    output_data = [{'url': item} for item in output_data]
    print("-----output_data=",output_data)
    return output_data


def export_json(data):
    with open("output.json", "w+") as output_file:
        json.dump(data, output_file)


if __name__ == '__main__':
    input_keywords, input_proxies, input_type = get_args()
    transformed_proxy = transform_args(input_proxies)
    output_data = crawl(input_keywords, transformed_proxy, input_type)
    export_json(output_data)
