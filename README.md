# github-crawler

### Crawl Github search results of repositories, issues or wikis.

## How to use

1.  At the root of the project, run `pip install -r requirements/common.txt`


2.  You need a JSON file to specify the arguments. In this format:
```json
{
  "keywords": [
    "openstack",
    "nova",
    "css"
  ],
  "proxies": [
    "194.126.37.94:8080",
    "13.78.125.167:8080"
  ],
  "type": "Repositories"
}
```


3. Run `python github_crawler.py <path_to_your_JSON_file>`


4. The results of the crawling get stored in `output_github_crawler_<date>.json`, at the root of the project.

## Testing

First, install the testing libraries with `pip install -r requirements/test.txt`

### Testing without coverage

```shell
pytest test.py
```

### Testing with coverage

```shell
coverage run -m pytest test.py
coverage report -m *.py
```
