import requests
import csv
from bs4 import BeautifulSoup
import tldextract
import re

if __name__ == "__main__":
    print()

header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1", 
}
  

def tagfunc(url):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"}
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1", 
    }

    if (not url.startswith("https") and not url.startswith("http")):
        url='https://'+url
        
    def test(tag):
        try:
            return(int(domain.lower() in tag.lower()))
        except:
            return(0)

    def soup_test(tag):
        tagg=soup.find(tag)
        return test(tagg)

    def soup_test_with_attr(tag,attr1,arrt2):
        tagg=soup.find(tag,attrs={attr1: arrt2})
        return test(tagg)

    def test_rate(tag):
        s=0
        links = soup.find_all(tag, href=True) #a:超連結
        #print(links)
        for i in links:
            if(domain.lower() in i['href'].lower()):
                s=s+1
        try:
            rate=s/len(links)
        except:
            rate=0  #len(links)=0      division by zero
        if(rate<0.2):
            return([1,0,0,0,0])
        elif(rate>=0.2):
            return([0,1,0,0,0])
        elif(rate>=0.4):
            return([0,0,1,0,0])
        elif(rate>=0.6):
            return([0,0,0,1,0])
        elif(rate>=0.8):
            return([0,0,0,0,1])

    

    '''
    try:     #https://taiwantimes.net/   ?取不了
        print("ip:",socket.gethostbyname(urlparse(url).hostname))
    except:
        print("此url ip取得不了:",url)
    '''
    domain = tldextract.extract(url).domain
    #print("公司代碼:",domain)
    
        
    try:                                    #header (orignal)
        response = requests.get(url,headers=headers ,timeout=10,allow_redirects=True)
        #重新導向之url
        url=response.url
        # print("Final URL:", response.url)
        # print(response.status_code)
    except:
        print('response failed')
        pass

    #print("response:",response)
    soup = BeautifulSoup(response.text, "html.parser")
            

    

    #判斷有沒fb分享鍵
    def has_share(html):
        try:

            if "https://www.facebook" in html or"facebook icon" in html:
                fb=1#True
            else:
                fb=0#False

        except Exception as e:
            print(f"網址 {url} 錯誤：{e}")
            return 0#False
        
    #判斷有沒line標籤
        try:

            #判斷有沒line分享鍵
            if "https://line" in html or "line icon" in html:
                line=1#True
            else:
                line=0#False

        except Exception as e:
            print(f"網址 {url} 錯誤：{e}")
            return 0#False
        return([fb,line])
    
    result={}
    
    result.update({'https':int(url.startswith('https'))})

    result.update({'urlLength:<=50':int(len(url)<=50)})

    result.update({'urlLength:<=100':int((len(url)>50)&(len(url)<=100))})                        

    result.update({'urlLength:>100':int(len(url)>100)})

    if(re.search(r'[@%\-_]',url)):
        result.update({'Special_char':1})
    else:
        result.update({'Special_char':0})
            #Titlte  'NoneType' object has no attribute 'string'
    try:                                   
        title_text = soup.title.string
        result.update({'Title tag':test(title_text)})
    except:
        result.update({'Title tag':0})
        
    #print("title:",title_text)

    #Description tag
    result.update({'Description tag':soup_test("description")})


    #Keywords tag
    result.update({'Keywords tag':soup_test("keywords")})
    
    

    #SEO tag 中 name="title"
    result.update({'SEO tag name=title':soup_test_with_attr("meta","name","title")})
    # meta_name_title = soup.find("meta", attrs={"name": "title"})
    # test(meta_name_title)

    #SEO tag 中 name="description"
    result.update({'SEO tag name=description':soup_test_with_attr("meta","name","description")})
    # meta_name_description = soup.find("meta", attrs={"name": "description"})
    # #print("meta_des:",meta_name_description)
    # test(meta_name_description)
    
    #SEO tag 中 name="keywords"
    result.update({'SEO tag name=keywords':soup_test_with_attr("meta","name","keyword")})
    # meta_name_keywords = soup.find("meta", attrs={"name": "keyword"})
    # test(meta_name_keywords)

    #SEO tag 中 property="og:title"
    result.update({'SEO tag property=og:title':soup_test_with_attr("meta","property","og:title")})
    # meta_property_title = soup.find("meta", attrs={"property": "og:title"})
    # test(meta_property_title)

    #SEO tag 中 property="og:description"
    result.update({'SEO tag property=og:description':soup_test_with_attr("meta","property","og:description")})
    # meta_property_description = soup.find("meta", attrs={"property": "og:description"})
    # test(meta_property_description)

    #SEO tag 中 property="og:keywords"
    result.update({'SEO tag property=og:keywords':soup_test_with_attr("meta","property","og:keywords")})
    # meta_property_keywords = soup.find("meta", attrs={"property": "og:keywords"})
    # test(meta_property_keywords)

    #SEO tag 中 property="og:site"
    result.update({'SEO tag property=og:site':soup_test_with_attr("meta","property","og:site")})
    # meta_property_site = soup.find("meta", attrs={"property": "og:site"})
    # test(meta_property_site)

    
    # Corp_Rate_All (公司代碼在web context連結網址出現比率)
    temp=test_rate("a")
    for i in range(5):
        result.update({'Corp_Rate_All:'+str((i+1)*20):temp[i]})
    # Corp_Rate1 (公司代碼在web context "Link" Tag中出現比率)
    temp=test_rate("link")
    for i in range(5):
        result.update({'Corp_Rate_Link:'+str((i+1)*20):temp[i]})
    # Corp_Rate2 (公司代碼在web context "Script" Tag 中出現比率)
    temp=test_rate("Script")
    for i in range(5):
        result.update({'Corp_Rate_Script:'+str((i+1)*20):temp[i]})


    # Corp_Rate3 (公司代碼在web context hyperlink 中出現比率)  所有的hyperlink?
    #test_rate("?")

    # Corp_Rate4 (公司代碼在web context "img" Tag中出現比率)
    temp=test_rate("img")
    for i in range(5):
        result.update({'Corp_Rate_Img:'+str((i+1)*20):temp[i]})

    #Split_Cnt (公司代碼切割字串數) > 2 
    #AREA W_AREA(地域碼(WHOIS)) =D_AREA(地域碼(註冊Server))

    #Is_gverify  
    gverify = soup.find("meta", attrs={"name": "google-site-verification"})
    if gverify:
        result.update({'Is_gverify':(1)})
    else:
        result.update({'Is_gverify':(0)})
    #Is_msverify 
    msverify = soup.find("meta", attrs={"name": "msvalidate.01"})
    if msverify:
        result.update({'Is_msverify':(1)})
    else:
        result.update({'Is_msverify':(0)})
    #Is_twitter  
    twitter = soup.find("meta", attrs={"name": "twitter:card"})
    if twitter:
        result.update({'Is_twitter':(1)})
    else:
        result.update({'Is_twitter':(0)})
    #Apivoid       註冊不了



    #fb line 標籤
    
    t = has_share(response.text)
    result.update({'facebook':t[0]})
    result.update({'line':t[1]}
                  )
    #[com，net，org，edu，mil，co]'
    sw=0
    gTLD=["com","net","org","edu","mil","co"]
    for i in gTLD:
        if(i in url):
            sw=1
    result.update({'gTLD':sw})

    htmllength=len(response.text)
    if htmllength>=10000:
        temp=0
    else:
        temp=1
    result.update({'HTML_Length<10000':temp})
    

    return((result,response.status_code,response.url))


def ftestf(url):
    return(tagfunc(url))