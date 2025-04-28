import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Find all four letter words
        words = soup.find_all("ul", {"class": "letter_table"})
        
        # Put all words into a csv file
        with open("four_letter_words.csv", "w") as f:
            for word in words:
                f.write(word.text.strip() + "\n")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    # Example URL - replace with the website you want to scrape
    url = "https://scrabble.collinsdictionary.com/word-lists/four-letter-words-in-scrabble/"
    scrape_website(url)
