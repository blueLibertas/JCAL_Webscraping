from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


__author__ = "Jinho Kim"
__status__ = "Fin"
__version__ = "1.0.1"
__date__ = '2023/09/20'
__about__ = 'Extract & save keyword from doi page of Journal of Computer Assisted Learning'

def extract_keywords(delay):
    with open("PDFlinks.txt", "r", encoding='utf-8') as f:
        links = f.read()

    count = 0
    with open("output_keywords.txt", 'w', encoding="utf-8") as file:

        for link in links.split("\n"):
            count += 1
            if count % 20 == 0:
                print("Finished {} out of 527".format(count))
            try: 
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                temp = link + "\t"
                url = link.replace("epdf", "abs")
                driver.get(url)
                time.sleep(delay)

                html = driver.page_source    
                soup = BeautifulSoup(html, 'html.parser')    

                keyword_tags = soup.find_all('meta', {"name": "citation_keywords"})

                keywords = [tag['content'] for tag in keyword_tags]

                # Print the extracted keywords
                formatted_keywords = ', '.join(keywords)
                temp += formatted_keywords
                print(temp, file=file)
                driver.quit()

            except Exception:
                print("ERROR for {}".format(link), file=file)
                print(link)

def format_keywords():
    with open("output_keywords.txt", "r", encoding='utf-8') as f:
        content = f.read()
    with open("output_keywords_formatted.txt", 'w', encoding="utf-8") as file:
        for line in content.split("\n"):
            try:
                link, keyword = line.strip("\n").split("\t")
                formatted_keyword = modify_string(keyword)
                print("{}\t{}\t{}".format(link, keyword, formatted_keyword), file = file)
            except Exception:
                print("{}\t{}".format(link, "ERROR"), file = file)


def modify_string(input_string):
    words = input_string.split(", ")
    num_words = len(words)
    
    first_part = words[:min(5, num_words)]  
    second_part = words[min(5, num_words):]  
    
    modified_string = '\t'.join(first_part)
    if second_part:
        modified_string += ', ' + ', '.join(second_part)
        
    return modified_string

def main():
    delay = 0.5
    extract_keywords = True
    format_keywords = True

    if extract_keywords:
        extract_keywords(delay)

    if format_keywords:
        format_keywords()



if __name__ == "__main__":
    main()