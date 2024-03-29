from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pymongo
import time

# Set up connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.nhl_db
collection = db.articles

# Define scrape funtion to pull the scraped info out
def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    listings = {}

# Visit the Mars news site
    browser.visit('https://redplanetscience.com/')
# # STEP ONE: Scrapping

# ## NASA Mars News

# HTML object
    html = browser.html
# Parse HTML with Beautiful Soup
    n_soup = soup(html, 'html.parser')

# Get the first list_text in the div tag, this is info about the lastest news
    n_soup.select_one('div.list_text')

# Assign variables
    news_title = 'NASA Administrator Statement on Moon to Mars Initiative, FY 2021 Budget'
    news_p = 'Jim Bridenstine addresses NASAs ambitious plans for the coming years, including Mars Sample Return'


# Print variables
    news_title


    news_p


# ## JPL Mars Space Images - Featured Image

# Visit the Mars news site
    url_2 = 'https://spaceimages-mars.com/'
    browser.visit(url_2)

    html = browser.html
    soup = soup(html, 'html.parser')

    print(html)

    print(soup)
# Ask Splinter to Go to Site and Click Button with Class Name full_image
    full_image_button = browser.find_by_tag("button")[1]
    full_image_button.click()


# In[ ]:


# Save this new page into a variable
    html = browser.html
    soup_1 = soup(html, 'html.parser')

# Use
    soup_1 = soup(html, 'html.parser')

# Save the image url into a variable
    featured_image_url = 'http://spaceimage-mars.com/image/featured/mars2.jpg'
# ## Mars Fact

# Use pandas to scrape the table containing the planet including Diameter, mass, etc.

    url = 'https://galaxyfacts-mars.com'

    tables = pd.read_html(url)
    tables

    df = tables[0]
    df.head()

# Convert dataframe to html
    html_table = df.to_html()
    html_table


# ## Mars Hemispheres

# Go to the website to obtain high resolution image for each Mar's hemispheres
    url = 'https://marshemispheres.com'
    browser.visit(url)

    html = browser.html
    mars_hem = soup(html, 'html.parser')


# ## Search for hemisphere titles
    hemi_names = []

# Search for the names of all four hemispheres
    results = mars_hem.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

# Get text and store in list
    for name in hemispheres:
        hemi_names.append(name.text)

    hemi_names

# Search for thethumbnail links
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:

        # If the thumbnail element has an image...
        if (thumbnail.img):

            # then grab the attached link
            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']

        # Append list with links
            thumbnail_links.append(thumbnail_url)

        thumbnail_links

    full_imgs = []

    for url in thumbnail_links:

        # Click through each thumbanil link
        browser.visit(url)

        html = browser.html
        full_img = soup(html, 'html.parser')

    # Scrape each page for the relative image path
        results = full_img.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']

    # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path

    # Add full image links to a list
        full_imgs.append(img_link)

    full_imgs


#  ## Store a list of dictionaries

# Zip together the list of hemisphere names and hemisphere image links
    mars_hemi_zip = zip(hemi_names, full_imgs)

    hemisphere_image_urls = []

# Iterate through the zipped object
    for title, img in mars_hemi_zip:

        mars_hemi_dict = {}
    # Add hemisphere title to dictionary
        mars_hemi_dict['title'] = title
    # Add image url to dictionary
        mars_hemi_dict['img_url'] = img
    # Append the list with dictionaries
        hemisphere_image_urls.append(mars_hemi_dict)
    hemisphere_image_urls

    browser.quit()

    return listings