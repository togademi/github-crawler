# github-crawler

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
