

## Project 4 - Livecoin

Target website: https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/

On splash app,

```
function main(splash, args)
    splash.private_mode_enabled = false
    
    url = args.url
    assert(splash:go(url))
    assert(splash:wait(1))

    rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
    rur_tab[5]:mouse_click()
    assert(splash:wait(1))
    splash:set_viewport_full()

    return {
        splash:png(),
        splash:html()
    }
end
```


```
scrapy startproject livecoin
scrapy genspider coin https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/
```

After installing scrapy-splash, do configuration following doc on https://github.com/scrapy-plugins/scrapy-splash

Output dataset json file by command

```
scrapy crawl coin -o dataset.json
```


