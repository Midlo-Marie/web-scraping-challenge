#Conversion of Mission to Mars Jupyter Notebook to Python Script

### *Mission to Mars*

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

# executable_path = {"executable_path": "./chromedriver.exe"}
# browser = Browser("chrome", **executable_path)


# Initialize browser
def init_browser(): 
    exec_path = {'executable_path': "./chromedriver.exe" }
    return Browser('chrome', headless=True, **exec_path)

###############################
# Visit the NASA Mars News Site
###############################
def mars_news():

    browser = init_browser()

#   What's going on with NASA Mars missions?
#   Visit the News on the mars.nasa.gov web page  through splinter module
#   and put the most recent article into an html object
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html

# > From "inspection" of activated NASA Mars Web page using Devtools, we note that the Title 
# > and "teaser" body of each article are found under the 
# >      ul class="item list" li class=slide
# >         div class="content title"
# >         div class="article_teaser_body"
# Parse Results HTML with BeautifulSoup
#   <ul class="item_list">
#     <li class="slide">
    
    NASAnews_soup = BeautifulSoup(html, "html.parser")

    try:

        element = NASAnews_soup.select_one("ul.item_list li.slide")

    # Now find just the title of the latest article (first one in the list) and article text
        news_date = element.find("div", class_="list_date").get_text()
        news_title = element.find("div", class_="content_title").get_text()
        news_teaser = element.find("div", class_="article_teaser_body").get_text()

        # print(f"From mars.nasa.gov on {news_date} we learn that: \n\t'{news_title}'")
        # print(f"\t{news_teaser}")
    except AttributeError:
        return
    browser.quit()
    return news_title, news_teaser

###############################################################################################
#  Now we look for space imagery from NASA Jet Propulsion Laboratory Featured Space Image site
###############################################################################################

# > From "inspection" of activated NASA JPL Web page and using Devtools, we find the 
# > featured image at the top of the page is id'd as a "full_image". 
# > The featured image may not be the same as the latest news article on the NASA news page.

def featured_image():
    browser = init_browser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Use Splinter to find the featured image by its id='full_image' in the HTML code
    # <button class="full_image">Full Image</button>
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

# Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    browser.quit()
    return img_url

########################################################################
# Now let's find out about Martian weather from the Mars Twitter account
########################################################################

def twitter_weather():

    browser = init_browser()

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    # print(weather_soup.prettify())

    # Find a Tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find("div", 
                                        attrs={
                                            "class": "tweet", 
                                                "data-name": "Mars Weather"
                                            })
    # print(mars_weather_tweet.prettify())

    # Search Within Tweet for <p> Tag Containing Tweet Text
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    # print(mars_weather)
    browser.quit()
    return mars_weather


################################################################################################
# Now look at Mars Facts site to scrape the table for data about the planet including size, mass
################################################################################################
# Use Pandas to convert the DataFrame to an HTML table string
def mars_facts():
    try:
        mars_df = pd.read_html("https://space-facts.com/mars/")[0]   
        # print(mars_df)
    except BaseException:               
        return

    mars_df.columns=["Description", "Mars", "Earth"]
    mars_facts_df=mars_df.drop(columns=["Earth"])
    mars_facts_df.set_index("Description",inplace=True)
    mars_facts = mars_facts_df.to_html()
    # data = mars_facts.to_dict(orient='records')
    return mars_facts

#####################################################################################################
## Look for images of Mars Hemispheres
# The two hemispheres of Mars are dramatically different from each other—a characteristic not seen on any other planet in our
# solar system. Non-volcanic, flat lowlands characterize the northern hemisphere, while highlands punctuated by countless 
# volcanoes extend across the southern hemisphere.Jan 29, 2015
# https://www.futurity.org/mars-hemispheres-846802/

# Visit the USGS Astrogeology Science Center Site
def hemisphere():

    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

# Find all of the level 3 header information for hemisphere products.  Loop through images based on number of products.
    hemisphere_image_urls = []

    products = browser.find_by_css("a.product-item h3")

    for i in range(len(products)):
        # initialize hemisphere dictionary
        hemisphere = {}
        # click on each product link to get to actual image
        browser.find_by_css("a.product-item h3")[i].click()
        
        # get url (href) for the "Sample" image option since full-res images are very large
        sample_product = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_product["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Go back to product screen to move to next product on the page
        browser.back()
    browser.quit()
    return hemisphere_image_urls

##  Another function to separate the title and image location for use in HTML
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = ""
        sample_element = "" 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere
    
#################################################
# Main Web Scraping function that runs all of the
# functions and stores returned data in a dictionary
# for storage in Mongo database
#################################################
def scrape_all():
    
    browser = init_browser()

    #mars_date = news_date 
    news_title, news_teaser = mars_news()
    img_url = featured_image()
    mars_weather = twitter_weather()
    facts = mars_facts()
    hemisphere_image_urls = hemisphere()
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_image": img_url,
        "weather": mars_weather,
        "facts": facts,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    # print(f"Data dictionary is {data}")
    return data 
    
    
if __name__ == "__main__":
    print(scrape_all())
