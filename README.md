# Web scraper
A basic web-scraper to view property listings.  
Built with Scrapy and scrapy-splash in Python.

### Requirements:
scrapy-splash is a dependency, and requires Splash and Docker.

### To run:
In terminal, run the Splash Docker image:
```
$ docker run -p 8050:8050 scrapinghub/splash
```

Navigate to the project folder:

```
~/scrapy-spider/property$ scrapy crawl svn
~/scrapy-spider/property$ scrapy crawl amreal
```
Scraper output is saved to a file automatically: `scrapy-spider/property/property.json`  
__Note:__ file contents are overwritten each time a crawl is run.
