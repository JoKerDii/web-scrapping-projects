## Project API

Target website: https://openlibrary.org/subjects/picture_books

open developer tool -> Network -> XHR -> refresh the page -> click on the next button-> Headers -> copy URL (https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12)

Note that if there are special characters in the URL, we need double quotes it.

```
scrapy startproject book_api
cd book_api
scrapy genspider ebooks "openlibrary.org/subjects/picture_books.json?limit=12&offset=12"
```

Modify 'ebooks.py' then run

```
scrapy crawl ebooks
```

Go back to the page and the developer tool -> click on the next page again -> copy URL (https://openlibrary.org/subjects/picture_books.json?limit=12&offset=24)

It can be notice that each time we click the next page button the offset increases by 12. Therefore, we can write code to automatically turn to the next page. We stop if the offset is too large that status code == 500 (this pattern can be found by set the offset to a large number and check the Header in developer tool).

After adding the pagination feature, run

```
scrapy crawl ebooks
```

it takes a very long time to finish scraping.