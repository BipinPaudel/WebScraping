import time
def checkShowAllImage(soup):
    allImg=soup.find_all('img',{"src":True})
    imagesList=[]
    for a in allImg:
        if a['src'].endswith("/2916/29161613/default_name.jpg") or a['src'].endswith("/2973/29734734/default_name.jpg"):
            imagesList.append(a['src'])
    return imagesList

def grabEverythingFromProductList(productUrl):
    productListUrl=productUrl
    wholeLinkList=[]
    while True:
        driver.get(productListUrl)
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        productThumbNail=soup.find_all("div",{"id":"sbprodgrid"})
        print(productThumbNail)
        try:
            aList=productThumbNail[0].find_all("a",{"class":"SbProductBlock js-product-bottom-link js-prod-content "})
        except:
            time.sleep(5)
            continue
        for a in aList:
            print(a['href'])
            wholeLinkList.append(a['href'])
        if soup.find_all("span",{"class":"Pagination-item is-inactive Pagination-icon--next js-next-page"}):
            break
        try:

            productListUrl=soup.find("a",{"class":"js-next-page Pagination-item Pagination-icon--next Pagination-link"})['href']

        except:
            continue
    print("There are total "+ str(len(wholeLinkList)) +"items in this category");
    
    for singleItemUrl in wholeLinkList:
        driver.get(singleItemUrl)
        html=driver.page_source
        soup=BeautifulSoup(html,"lxml")
        productTitle=soup.find("span",{"class":"ProductDetailInfoBlock-header-title js-product-title-name"})
        productPriceHead=soup.find("div",{"class":"ProductDetailInfoBlock-pricing-amount js-price-format"})
        productPrice = soup.find("span",{"class":""})
        productUrl=singleItemUrl
        productImageUrl=soup.find("img",{"class":"ProductDetailImagesBlock-carousel-image"})
        productImageUrl=productImageUrl['src'].replace("%20","")
        
        productDescription=soup.find("div",{"class":"js-content-contain"})
        descriptionSplit=productDescription.find("p")
        description=''
        features=productDescription.find_all("li")

        for p in descriptionSplit:
      
            description+= str(p)+' '
        description+="Features\n"
        for li in features:
            reqstring1=str(li.text)
            description+=str(reqstring1)+', '
        
        outputWriter.writerow([productTitle.text,productPrice.text,productUrl,productImageUrl,description])
        print("This product written")




import csv
outputFile = open('output.csv', 'a', newline='')
outputWriter = csv.writer(outputFile)
outputWriter.writerow(['product title','product price','product url','product image','product description'])
homeUrl="https://www.wayfair.com"
from bs4 import BeautifulSoup 
from selenium import webdriver
driver=webdriver.Firefox()
driver.get(homeUrl)
html=driver.page_source
homeSoup=BeautifulSoup(html,"lxml")
print("We are going to the index page header to extract all categories")
mainHeadingBlock=homeSoup.find_all("div",{"class":"nav_link_block_links nav_link_block_text"})
mainLinks=[]#contains all link from header bar
for req in mainHeadingBlock:
    hrefsFromHeader=req.find_all("a",{"class":"js-cms-link cms_add_link "})
    for headerLinkElement in hrefsFromHeader:
        mainLinks.append(headerLinkElement['href'])
print("Categories are extracted and will be used further")
print("there are total "+str(len(mainLinks)) + "categories")

i=0
for categoryUrl in mainLinks[i:]:
    driver.get(categoryUrl)
    html=driver.page_source
    soup=BeautifulSoup(html,"lxml")
    imageList=checkShowAllImage(soup)
    print(str(i) + " position " + str(categoryUrl) + " has been started----------------")
    if len(soup.find_all("a",{"class":"sbprodgrid"}))>0:
        grabEverythingFromProductList(categoryUrl)
    
    elif len(imageList)>0:

        imageTag=soup.find('img',{'src':imageList[0]})
        productListUrl=imageTag.parent['href']
        print("len imagelist is > 0 " + productListUrl)
        grabEverythingFromProductList(productListUrl)
            
    else:
        allCategoryGrid=homeSoup.find_all("span",{"class":"js-lego-data lego_text_field "})
        for a in allCategoryGrid:
            if a.text.endswith('by Category'):
                bigBrother=a.parent.parent.findNextSibling('div')
                firstCategoryList=[]
                while True:
                    insideCategory=bigBrother.find_all('a',{"class":"js-cms-link cms_add_link "})
                    firstCategoryList.append(insideCategory[0]['href'])
                    bigBrother=bigBrother.findNextSibling('div')
                    if 'TextUnderImg--subCat' not in bigBrother['class']:
                        break
                for links in firstCategoryList:
                    driver.get(links)
                    html=driver.page_source
                    categorySoup=BeautifulSoup(html,"lxml")
                    if len(links.find_all("div",{"id":"sbprodgrid"}))>0:
                        grabEverythingFromProductList(links)
                    else:
                        imageList=checkShowAllImage(categorySoup)
                        if len(imageList)>0:
                            imageTag=soup.find('img',{'src':imageList[0]})
                            productListUrl=imageTag.parent['href']
                            wholeLinkList=[]
                            grabEverythingFromProductList(productListUrl)
    print(str(i) + "category finished successfully")  
    i=i+1                      

                        
outputFile.close()
        