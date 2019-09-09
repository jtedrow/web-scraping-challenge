# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser


def scrape():
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    news_title = soup.find_all('div', class_="content_title")[0].text.strip()
    news_p = soup.find_all('div', class_="rollover_description_inner")[
        0].text.strip()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    browser.quit()

    article = soup.find("a", class_='button fancybox')
    featured_image = article["data-fancybox-href"]
    base_url = url.split("/")
    base_url = base_url[2]

    featured_image_url = base_url + featured_image

    twitter_url = "https://twitter.com/marswxreport?lang=en"

    # Retrieve page with the requests module
    response = requests.get(twitter_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    mars_weather = soup.find_all(
        "div", class_="js-tweet-text-container")[0].p.text

    mars_facts = "https://space-facts.com/mars/"
    mars_df = pd.read_html(mars_facts)[1]
    mars_df = mars_df.rename(columns={0: "Category", 1: "Value"})
    mars_df = mars_df.set_index("Category")

    usgs_url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(usgs_url)
    usgs_html = browser.html
    browser.quit()
    soup = BeautifulSoup(usgs_html, 'lxml')

    hemispheres = soup.find_all("h2")
    titles = []

    for h in hemispheres:
        titles.append(h.text + " Hemisphere")

    del titles[-1]

    usgs_url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"
    browser = Browser('chrome', **executable_path, headless=False)

    links = []

    for t in titles:
        browser.visit(usgs_url)
        browser.click_link_by_partial_text(f'{t} Enhanced')
        hemisphere_html = browser.html
        hemi_soup = BeautifulSoup(hemisphere_html, 'lxml')
        link = hemi_soup.find("a", target="_blank")["href"]
        links.append(link)

    browser.quit()

    joined = list(zip(titles, links))

    hemisphere_image_urls = []

    for t, l in joined:
        dictionary = {"title": t, "img_url": l}
        hemisphere_image_urls.append(dictionary)

    dictionary = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_df": mars_df,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return dictionary
