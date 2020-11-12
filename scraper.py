import requests
from bs4 import BeautifulSoup as soup


url = "https://thehimalayantimes.com"

# Load webpage content
req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Convert to beautiful soup object
page_soup = soup(req.content, "html.parser")

print("Homepage loaded...")

# main_news_list = page_soup.find_all("ul", {"class": "mainNews"})
main_news_list = page_soup.select("ul.mainNews li a")

article_links = []

# Get links to actual complete articles from the main homepage
# for news_ul in main_news_list:
#     for anchor in news_ul.select("li a"):
#         article_links.append(anchor["href"])

for main_news in main_news_list:
    article_links.append(main_news["href"])


# Removing duplicate links
article_links = list(dict.fromkeys(article_links))

print("Scraped individual article links...")

# creating csv file to store articles
filename = "scraped_articles.csv"
f = open(filename, "w")

headers = "title, post\n"
f.write(headers)


def clean_text(text):
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    text = text.replace("Follow The Himalayan Times onTwitterandFacebook", "")
    return text


for link in article_links:
    # For each article, create new connection and scrape title and details
    article_req = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    article_soup = soup(article_req.content, "html.parser")
    article_title = article_soup.find("h2").getText()

    postDetails = ""
    post = article_soup.select("div.mainPost p")
    for p in post:
        postDetails += clean_text(p.getText()) + " "

    f.write(article_title.replace(",", "") + "," +
            postDetails.replace(",", "") + "\n")

f.close()

print("Individual articles scraped and added to csv...")

print("\nCOMPLETED!")
