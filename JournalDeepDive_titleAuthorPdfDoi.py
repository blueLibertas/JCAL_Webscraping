from bs4 import BeautifulSoup

__author__ = "Jinho Kim"
__status__ = "Fin"
__version__ = "1.0.1"
__date__ = '2023/09/20'
__about__ = 'Extract & save title, author, pdf link, doi from a issue page (html) of Journal of Computer Assisted Learning'

def extract_info_row(html_name, file):

    with open(html_name, "r", encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    temp = soup.find_all(class_="issue-items-container bulkDownloadWrapper")
    section_count = 0

    for item in temp:
        section_count += 1
        heading = item.find("h3").text

        print("="*50, file=file)
        print(heading, file=file)
        print("="*50, file=file)

        papers = item.find_all(class_="issue-item")

        for paper in papers:
            title = paper.find("h2").text

            element = paper.find(class_="loa comma loa-authors-trunc")
            if element:
                author = element.get_text(strip=True).strip(",").replace(',', ", ")
            else:
                author = ""

            pdf = paper.find(class_="PdfLink") 
            if pdf:
                pdf_href = pdf.find('a')['href']
            else:
                pdf_href = ""

            doi = paper.find(class_="issue-item__title visitable")
            doi_href = "https://onlinelibrary.wiley.com"+doi['href']
            
            print("-"*50, file=file)
            print(title, file=file)
            print(author, file=file)
            print(pdf_href, file=file)
            print(doi_href, file=file)

def extract_info_col(html_name, file):

    with open(html_name, "r", encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    temp = soup.find_all(class_="issue-items-container bulkDownloadWrapper")
    section_count = 0

    for item in temp:
        section_count += 1
        heading = item.find("h3").text

        print("="*50, file=file)
        print(heading, file=file)
        print("="*50, file=file)

        papers = item.find_all(class_="issue-item")

        for paper in papers:
            title = paper.find("h2").text

            element = paper.find(class_="loa comma loa-authors-trunc")
            if element:
                author = element.get_text(strip=True).strip(",").replace(',', ", ")
            else:
                author = ""

            pdf = paper.find(class_="PdfLink") 
            if pdf:
                pdf_href = pdf.find('a')['href']
            else:
                pdf_href = ""

            doi = paper.find(class_="issue-item__title visitable")
            doi_href = "https://onlinelibrary.wiley.com"+doi['href']
            
            print("{}\t{}\t{}\t{}\t".format(title, author, pdf_href, doi_href), file=file)

def output_row(volumns, issues):
    with open("output_row.txt", 'w', encoding="utf-8") as file:
        for i in range (6):
            volumn = volumns[i]
            for no in range(issues[i]):
                html_name = "Journal of Computer Assisted Learning_ Vol {}, No {}.html".format(volumn, no+1)
        
                print("{}Volume: {} Issue: {}{}".format("+"*15,volumn, no+1,"+"*15), file=file)
                extract_info_row(html_name, file)  

def output_col(volumns, issues):
    with open("output_column.txt", 'w', encoding="utf-8") as file:
        for i in range (6):
            volumn = volumns[i]
            for no in range(issues[i]):
                html_name = "Journal of Computer Assisted Learning_ Vol {}, No {}.html".format(volumn, no+1)
        
                print("{}Volume: {} Issue: {}{}".format("+"*15,volumn, no+1,"+"*15), file=file)
                extract_info_col(html_name, file) 

def main():
    output_as_row = True
    output_as_col = True
    volumns = [28, 35, 36, 37, 38, 39]
    issues = [6, 6, 6, 6, 6, 5]

    if output_as_row:
        output_row(volumns, issues)

    if output_as_col:
        output_col(volumns, issues)



if __name__ == "__main__":
    main()
