import pandas as pd
from PIL import Image

def genimage(features):
    importance=pd.read_csv('./csvfiles/importance.csv')[:15]
    size = 224
    block_count = importance.shape[1]-1
    block_width = 8
    img = Image.new("RGB", (size, size), color="white")
    pixels = img.load()
    rate=0
    colors = [
        (0, 255, 0), (0, 0, 255), (140, 230, 0), (128, 128, 255), (255, 0, 0),
        (128,0,128), (255,255,0), (128,128,128), (64,64,64), (255,165,0),
        (71,31,0), (234,205,118), (102,51,204), (148,0,211), (0,0,128)
    ]

    for i in range(block_count):
        rate=max(rate,importance.iloc[:,i+1].sum())


    for i in range(block_count):

        start_x=i+(i*block_width)
        end_x=i+(i*block_width)+8

        for j in range(size):
            pixels[(i+(i*block_width)+8),j]=(0,0,0)

        y_top = size
        count=0
        for j in importance.iloc[:,i+1]:
            
            height = int(j/rate*size)
            color = colors[count % len(colors)]

            if (features[importance.iloc[count,0]]==0):
                for x in range(start_x, end_x):
                    for y in range(y_top - height, y_top):
                        if 0 <= y < size:  # 防止超出圖片範圍
                                pixels[x, y] = (255,255,255)
            else:
                for x in range(start_x, end_x):
                    for y in range(y_top - height, y_top):
                        if 0 <= y < size:  # 防止超出圖片範圍
                                pixels[x, y] = color

            y_top -= height
            count+=1
    return img
    


genimage({'https': 1, 'urlLength:<=50': 1, 'urlLength:<=100': 1, 'urlLength:>100': 1, 'Special_char': 1, 'Title tag': 1, 'Description tag': 1, 'Keywords tag': 1, 'SEO tag name=title': 1, 'SEO tag name=description': 1, 'SEO tag name=keywords': 1, 'SEO tag property=og:title': 1, 'SEO tag property=og:description': 1, 'SEO tag property=og:keywords': 1, 'SEO tag property=og:site': 1, 'Corp_Rate_All:20': 1, 'Corp_Rate_All:40': 1, 'Corp_Rate_All:60': 1, 'Corp_Rate_All:80': 1, 'Corp_Rate_All:100': 1, 'Corp_Rate_Link:20': 1, 'Corp_Rate_Link:40': 1, 'Corp_Rate_Link:60': 1, 'Corp_Rate_Link:80': 1, 'Corp_Rate_Link:100': 1, 'Corp_Rate_Script:20': 1, 'Corp_Rate_Script:40': 1, 'Corp_Rate_Script:60': 1, 'Corp_Rate_Script:80': 1, 'Corp_Rate_Script:100': 1, 'Corp_Rate_Img:20': 1, 'Corp_Rate_Img:40': 1, 'Corp_Rate_Img:60': 1, 'Corp_Rate_Img:80': 1, 'Corp_Rate_Img:100': 1, 'Is_gverify': 1, 'Is_msverify': 1, 'Is_twitter': 1, 'facebook': 1, 'line': 1, 'gTLD': 1, 'HTML_Length<10000': 1}).save("test.png")

def genlimg():
    features=pd.read_csv('./csvfiles/phishtable.csv')
    features=pd.concat([features,pd.read_csv('./csvfiles/top10mtable.csv')])
    for i in range(len(features)):
        feature=features.iloc[i,:].to_dict()
        if(feature['Phish']==1):
            genimage(feature).save('./image/phish/'+str(i)+'.png')
        else:
            genimage(feature).save('./image/notphish/'+str(i)+'.png')

genlimg()