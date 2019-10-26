## *Mission to Mars*

> In this assignment, we build a web application that scrapes various websites for data related
> to NASA's Mission to Mars and displays the information in a single Web (HTML) page.


### Flow control

* Jupyter notebook Python script was used to code and develop program to visit web pages
    and retrieve data (Mission_to_Mars_Midlomarie.ipynb)
* Notebook script was downloaded and converted to Python script to run at the command line, includes
    import of splinter to browse webpages, and PyMongo (local connection to MongoDB) to save data in 
    database document(scrape_mars_Midlomarie.py)
* index.html script was designed to display output data about Mars on a single Web page (index.html)
* A Flask app, a popular Python web framework, sets up the Web page and calls the Python script
    to scrape and insert Mars data in HTML template  (app.py)
    
###
   