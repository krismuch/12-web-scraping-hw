from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

mars = {}

def scrape():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    # Create HTML object, parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # get title, store in variable
    news_title = soup.find('div', class_="content_title").text

    # get paragraph text, store in variable
    news_p = soup.find('div', class_="article_teaser_body").text

    mars['news_title'] = news_title
    mars['news_p'] = news_p

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Create HTML object, parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # navigate to full image page
    browser.click_link_by_partial_text('FULL IMAGE')

    # get image url, store in variable
    featured_image_url=browser.find_by_css('.fancybox-image').first['src']

    mars['featured_image_url'] = featured_image_url

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Create HTML object, parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    tweet = news_title = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_weather = tweet[8:]
    mars_weather = mars_weather.replace('\n',' ')

    mars['mars_weather'] = mars_weather

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # grab information presented in tables
    tables = pd.read_html(url)

    # grab the table we are interested in, rename columns, replace 0,1..etc index with first column
    df = tables[1]
    df.columns = ['','Value']
    df.set_index('', inplace=True)

    #send to html table string
    html_table = df.to_html(index=True)

    #get rid of /n
    html_table.replace('\n', '')

    mars['table'] = html_table

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Create HTML object, parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # navigate to hemisphere page
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')

    # get image url, store in variable
    image1=browser.find_by_css('.wide-image').first['src']

    #repeat for next hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    image2=browser.find_by_css('.wide-image').first['src']

    #repeat for next hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    image3=browser.find_by_css('.wide-image').first['src']

    #repeat for next hemisphere
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    image4=browser.find_by_css('.wide-image').first['src']
    
    mars['image1'] = image1
    mars['image2'] = image2
    mars['image3'] = image3
    mars['image4'] = image4

    # Return results
    return mars
