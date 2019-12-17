from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd



def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    #get news data
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    browser.quit()
    slides = soup.find_all('li', class_='slide')
    slide = slides[0]
    news_title = slide.find('div', class_='content_title').text
    news_para = slide.find('div', class_='article_teaser_body').text
    #get featured image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser_jpl = init_browser()
    browser_jpl.visit(url)
    time.sleep(1)
    browser_jpl.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    html = browser_jpl.html
    soup = bs(html, 'html.parser')
    browser_jpl.quit()
    img = soup.find('div', class_='fancybox-inner')
    img_url = img.find('img')['src']
    img_url_start = 'https://www.jpl.nasa.gov'
    full_image_url = img_url_start + img_url
    #get twitter weather 
    url = 'https://twitter.com/marswxreport?lang=en'
    browser_twit = init_browser()
    browser_twit.visit(url)
    time.sleep(1)
    html = browser_twit.html
    soup = bs(html, 'html.parser')
    browser_twit.quit()
    tweet = soup.find('li', class_='js-stream-item')
    mars_weather = tweet.find('p', class_='tweet-text').text
    mars_weather = mars_weather.replace('\n', ', ')
    mars_weather = mars_weather.split('pic.')
    mars_weather = mars_weather[0]
    #get hemisphere photos
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser_ast = init_browser()
    browser_ast.visit(url)
    time.sleep(2)
    browser_ast.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    time.sleep(2)
    html_cerb = browser_ast.html
    soup_cerb = bs(html_cerb, 'html.parser')
    time.sleep(2)
    browser_ast.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    time.sleep(2)
    html_vall = browser_ast.html
    soup_vall = bs(html_vall, 'html.parser')
    time.sleep(2)
    browser_ast.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    time.sleep(2)
    html_syr = browser_ast.html
    soup_syr = bs(html_syr, 'html.parser')
    time.sleep(2)
    browser_ast.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    time.sleep(2)
    html_schi = browser_ast.html
    soup_schi = bs(html_schi, 'html.parser')
    browser_ast.quit()
    cerb_img_end = soup_cerb.find('img', class_='wide-image')['src']
    cerb_img_start = 'https://astrogeology.usgs.gov'
    cerb_url = cerb_img_start + cerb_img_end
    vall_img_end = soup_vall.find('img', class_='wide-image')['src']
    vall_img_start = 'https://astrogeology.usgs.gov'
    vall_url = vall_img_start + vall_img_end
    syr_img_end = soup_syr.find('img', class_='wide-image')['src']
    syr_img_start = 'https://astrogeology.usgs.gov'
    syr_url = syr_img_start + syr_img_end
    schi_img_end = soup_schi.find('img', class_='wide-image')['src']
    schi_img_start = 'https://astrogeology.usgs.gov'
    schi_url = schi_img_start + schi_img_end
    hemi_dict = [
        {'title':'Cerberus Hemisphere Enhanced','url':cerb_url},
        {'title':'Valles Marineris Hemisphere Enhanced','url':vall_url},
        {'title':'Syrtis Major Hemisphere Enhanced','url':syr_url},
        {'title':'Schiaparelli Hemisphere Enhanced','url':schi_url},
    ]
    responce_dict = {
        'news_title':news_title,
        'news_para':news_para,
        'featured_img_url':full_image_url,
        'mars_weather':mars_weather,
        'hemisphere_dict':hemi_dict
    }
    return responce_dict



