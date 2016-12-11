def checkShowAllImage(soup):
    allImg=soup.find_all('img',{"src":True})
    
    imagesList=[]
    for a in allImg:
        if a['src'].endswith("/2916/29161613/default_name.jpg") or a['src'].endswith("/2973/29734734/default_name.jpg"):
            print(a['src'])
            imagesList.append(a['src'])
    print(len(imagesList))
    return imagesList

def grabEverythingFromProductList(productListUrl):
    wholeLinkList=[]
    while True:
        driver.get(productListUrl)
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        productThumbNail=soup.find_all("div",{"id":"sbprodgrid"})
        aList=productThumbNail[0].find_all("a",{"class":"SbProductBlock js-product-bottom-link js-prod-content"})
        for a in aList:
            print(a['href'])
            wholeLinkList.append(a['href'])
        if soup.find_all("span",{"class":"Pagination-item is-inactive Pagination-icon--next js-next-page"}):
            break
        productListUrl=soup.find("a",{"class":"js-next-page Pagination-item Pagination-icon--next Pagination-link"})['href']
        
    for singleItemUrl in wholeLinkList:
        driver.get(singleItemUrl)
        html=driver.page_source
        soup=BeautifulSoup(html,"lxml")
        productTitle=soup.find("span",{"class":"ProductDetailInfoBlock-header-title js-product-title-name"})
        productPrice=soup.find("span",{"data-id":"dynamic-sku-price"})
        productUrl=singleItemUrl
        productImageUrl=soup.find("img",{"class":"ProductDetailImagesBlock-carousel-image"})
        productImageUrl=productImageUrl['src'].replace("%20","")
        productDescription=soup.find("div",{"class":"ProductDetailInfoBlock-snippets clearfix"})
        ulList=productDescription.find("ul")
        description=''
        liInformation=ulList.find_all('li')
        for a in liInformation:
            description+=a.text+" "
    
        print(productTitle.text+productPrice.text)
        outputWriter.writerow([productTitle,productPrice,productUrl,productImageUrl,description])



#for home page
import csv
outputFile = open('output.csv', 'w', newline='')
outputWriter = csv.writer(outputFile)
outputWriter.writerow(['product title','product price','product url','product image','product description'])
homeUrl="https://www.wayfair.com"
from bs4 import BeautifulSoup 
from selenium import webdriver
driver=webdriver.Firefox()
driver.get(homeUrl)
html=driver.page_source
homeSoup=BeautifulSoup(html,"lxml")

mainHeadingBlock=homeSoup.find_all("div",{"class":"nav_link_block_links nav_link_block_text"})
mainLinks=[]#contains all link from header bar
for req in mainHeadingBlock:
    hrefsFromHeader=req.find_all("a",{"class":"js-cms-link cms_add_link "})
    for headerLinkElement in hrefsFromHeader:
        mainLinks.append(headerLinkElement['href'])
print(len(mainLinks))


for categoryUrl in mainLinks:
    driver.get(categoryUrl)
    html=driver.page_source
    soup=BeautifulSoup(html,"lxml")
    imageList=checkShowAllImage(soup)
    if len(soup.find_all("div",{"id":"sbprodgrid"}))>0:
        grabEverythingFromProductList(categoryUrl)
    elif len(imageList)>0:
        print('la dherai')
        imageTag=soup.find('img',{'src':imageList[0]})
        productListUrl=imageTag.parent['href']
        grabEverythingFromProductList(productListUrl)
            
    else:
        print('ttt')
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
                            print('ok more')
                            imageTag=soup.find('img',{'src':imageList[0]})
                            productListUrl=imageTag.parent['href']
                            wholeLinkList=[]
                            grabEverythingFromProductList(productListUrl)
                        
outputFile.close()
        