# import csv
import tag
import pandas as pd

def fttable(phish='./csvfiles/verified_online.csv',bamount=0,top10m='./csvfiles/top10milliondomains.csv',wamount=0):
    fdict={}
    failedlink=[]
    try:
        with open('./csvfiles/failedlink.txt','r')as f:
            failedlink=f.read().split()
    except:
        pass
    with open(phish, newline='',encoding="utf-8") as black:
        urls=[]
        reurls=[]
        black.readline()
        i=0
        t=0
        try:
            t=pd.read_csv('./csvfiles/phishtable.csv')
        except:
            pass
        while i<bamount:
            isin=0
            url=black.readline().split(',')[1]
            if (url in failedlink)or('google'in url):
                print('url is in failedlink list')
                print(url)
                continue
            try:
                isin=url in t.url.values
            except:
                pass
            if (url in urls) or isin:
                if isin==1:
                    i+=1
                print('url already exist')
                print(url)
                print()
                continue
            urls.append(url)
            try:
                temp=tag.tagfunc(url)                       #存函式回傳值
            except Exception as error:
                print(error)
                print(url)
                failedlink.append(url)
                print()
                continue
            try:
                isin=temp[2] in t['response url'].values
            except:
                pass
            if (temp[2] in reurls)or isin:
                if isin==1:
                    i+=1
                print('response url already exist')
                print(temp[2])
                print()
                continue
            reurls.append(temp[2])
            
            if temp[1]!=200:
                print(url)
                print(temp[2])
                print(temp[1])
                failedlink.append(url)
                print()
                continue
            feature={
                'Phish':1,
                'url':url,
                'response url':temp[2]
            }
            feature.update(temp[0])
            if fdict=={}:
                fdict={
                    'Features':feature.keys(),
                    '1':feature.values()
                }
            else:
                fdict.update({str(i+1):feature.values()})
            print(i)
            print(url)
            print(temp[2])
            print()
            i+=1


    with open(top10m, newline='',encoding="utf-8") as white:
        urls=[]
        reurls=[]
        white.readline()
        i=0
        t=0
        try:
            t=pd.read_csv('./csvfiles/top10mtable.csv')
        except:
            pass
        while i<wamount:
            isin=0
            url=white.readline().split(',')[1].replace('"','')
            if url in failedlink:
                print('url is in failedlink list')
                print(url)
                continue
            try:
                isin=url in t.url.values
            except:
                pass
            if (url in urls) or isin:
                if isin==1:
                    i+=1
                print('url already exist')
                print(url)
                print()
                continue
            urls.append(url)
            try:
                temp=tag.tagfunc(url)                       #存函式回傳值
            except Exception as error:
                print(error)
                print(url)
                failedlink.append(url)
                print()
                continue
            try:
                isin=temp[2] in t['response url'].values
            except:
                pass
            if (temp[2] in reurls)or isin:
                if isin==1:
                    i+=1
                print('response url already exist')
                print(temp[2])
                print()
                continue
            reurls.append(temp[2])
            if temp[1]!=200:
                print(url)
                print(temp[1])
                failedlink.append(url)
                print()
                continue
            feature={
                'Phish':0,
                'url':url,
                'response url':temp[2]
            }
            feature.update(temp[0])
            if fdict=={}:
                fdict={
                    'Features':feature.keys(),
                    '1':feature.values()
                }
            else:
                fdict.update({str(i+1+bamount):feature.values()})
            print(i)
            print(url)
            print()
            i+=1
    with open('./csvfiles/failedlink.txt','w')as f:
        f.write(' '.join(failedlink))
    table=pd.DataFrame(fdict)
    table.set_index('Features', inplace=True)
    table=table.T
    return(table)
#a=fttable(bamount=2,wamount=2)
#print(a)

#把函式回傳的表寫進檔案
def writetable(amount=480):
    phishtable=fttable(bamount=amount)
    top10mtable=fttable(wamount=amount)
    try:
        phish=pd.read_csv('./csvfiles/phishtable.csv')
        phishtable=pd.concat([phish,phishtable])
    except:
        pass
    try:
        top10m=pd.read_csv('./csvfiles/top10mtable.csv')
        top10mtable=pd.concat([top10m,top10mtable])
    except:
        pass


    phishtable.to_csv('./csvfiles/phishtable.csv',encoding='utf-8',index=False)
    top10mtable.to_csv('./csvfiles/top10mtable.csv',encoding='utf-8',index=False)

writetable()

'''
with open("4060.csv",'w',newline='') as csvfile:
    write=csv.writer(csvfile)
    write.writerows(phishtable)
    for i in range(1,321):
        write.writerow(top10mtable[i])

with open("5050.csv",'w',newline='') as csvfile:
    write=csv.writer(csvfile)
    for i in range(0,401):
        write.writerow(phishtable[i])
    for i in range(1,401):
        write.writerow(top10mtable[i])

with open("6040.csv",'w',newline='') as csvfile:
    write=csv.writer(csvfile)
    write.writerows(phishtable)
    for i in range(1,321):
        write.writerow(top10mtable[i])
'''