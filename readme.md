# Link Checker

Link Checker is a crawler to check link status written in python scrapy framework.

## Dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```
Python >=3.6
pipenv

urllib3
scrapy >=1.5
```

## Activate env
```bash
pipenv shell
```

## Run

```bash
scrapy crawl link_checker_spider -a manifest_url=https://www.sangam.com/asset-manifest.json -a input_url=https://www.sangam.com -a fetch_from_file=true -a only_broken=true -a filepath=sangam-domains.json -o items.json
```

```python
-o output-file
-a command-line arguments

# Command-line Arguments:
manifest_url
input_url
only_broken
fetch_from_file
filepath (required only when fetch_from_file=true)
*** add your own domain list json in shared directory and provide name in filepath ***
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
