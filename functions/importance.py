from sklearn import ensemble,preprocessing,metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score,f1_score
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np

'''
features=pd.read_csv("featuretable.csv")
f1=pd.read_csv("4060.csv")
f2=pd.read_csv("5050.csv")
f3=pd.read_csv("6040.csv")
'''

def rf(features):

    features=features.dropna()
    features=features.drop("url",axis=1)
    features=features.drop('response url',axis=1)

    phish_x=features.drop("Phish",axis=1)
    phish_y=features["Phish"]

    train_x,test_x,train_y,test_y=train_test_split(phish_x,phish_y,test_size=0.3)

    forest=ensemble.RandomForestClassifier(n_estimators=100)
    forest_fit=forest.fit(train_x,train_y)

    predicted=forest.predict(test_x)

    accuracy=metrics.accuracy_score(test_y,predicted)

    feature_importance=forest.feature_importances_
    feature_df=pd.DataFrame({'Features':phish_x.columns,'Importance':feature_importance})
    feature_df.sort_values('Importance',inplace=True,ascending=False)

    recall=recall_score(test_y,predicted)
    f1=f1_score(test_y,predicted)

    '''
    print("調和平均數:"+str(f1))
    print("召回率:"+str(recall))
    print("準確度:"+str(accuracy))
    
    print(feature_df)
    '''
    result=feature_df

    result['Importance']=result['Importance'].map(lambda x:x*accuracy)


    return result


def rfgroupresult(data):
    table=rf(data)
    for i in range(19):
        temp=rf(data).rename(columns={'Importance':'Importance'+str(i+2)})
        table=pd.merge(table,temp,on='Features')

    list=table.values.tolist()

    mean=[]
    l75=[]
    l50=[]
    l25=[]

    for i in range(len(table)):
        row = list[i][1:]
        mean.append(float(np.mean(row)))
        l75.append(float(np.percentile(row,75)))
        l50.append(float(np.percentile(row,50)))
        l25.append(float(np.percentile(row,25)))


    result=pd.DataFrame({'Features':table.Features,'rf_mean':mean,'rf_75%':l75,'rf_50%':l50,'rf_25%':l25}).sort_values("rf_mean", ascending=False).reset_index(drop=True)

    return result

def dt(features):


    features = features.dropna()
    features = features.drop("url", axis=1)
    features = features.drop('response url',axis=1)

    phish_x = features.drop("Phish", axis=1)  # 所有的特徵
    phish_y = features["Phish"]  # 預測標籤

    train_x, test_x, train_y, test_y = train_test_split(phish_x, phish_y, test_size=0.3, stratify=phish_y)

    model = DecisionTreeClassifier(max_depth=5)
    model.fit(train_x, train_y)

    importances = model.feature_importances_
    feature_df = pd.DataFrame({'Features': phish_x.columns, 'Importance': importances})
    feature_df.sort_values('Importance', ascending=False, inplace=True)

    predicted=model.predict(test_x)

    accuracy=metrics.accuracy_score(test_y,predicted)

    result=feature_df
    result["Importance"]=result['Importance'].map(lambda x:x*accuracy)

    return feature_df

def dtgroupresult(data):
    table = dt(data).copy()

    for i in range(19):  # 再跑 19 次總共 20 次
        temp = dt(data).rename(columns={'Importance': 'Importance' + str(i + 2)})
        table = pd.merge(table, temp, on='Features')  # 合併進 table

    values = table.values.tolist()

    mean = []
    l75 = []
    l50 = []
    l25 = []

    for i in range(len(table)):
        row = values[i][1:]  
        mean.append(float(np.mean(row)))
        l75.append(float(np.percentile(row, 75)))
        l50.append(float(np.percentile(row, 50)))
        l25.append(float(np.percentile(row, 25)))

    result = pd.DataFrame({
        'Features': table['Features'],
        'dts_mean': mean,
        'dts_75%': l75,
        'dts_50%': l50,
        'dts_25%': l25
    }).sort_values("dts_mean", ascending=False).reset_index(drop=True)

    return result

def finalresult():
    phish=pd.read_csv('./csvfiles/phishtable.csv')
    top10m=pd.read_csv('./csvfiles/top10mtable.csv')
    total=phish.shape[0]
    t46=pd.concat([phish[:int(total*0.4)],top10m[:int(total*0.6)]])
    t55=pd.concat([phish[:int(total*0.5)],top10m[:int(total*0.5)]])
    t64=pd.concat([phish[:int(total*0.6)],top10m[:int(total*0.4)]])
    table=rfgroupresult(t46)
    table2=rfgroupresult(t55)
    table3=rfgroupresult(t64)

    table4=dtgroupresult(t46)
    table5=dtgroupresult(t55)
    table6=dtgroupresult(t64)

    result=pd.merge(table,table2,on='Features')
    result=pd.merge(result,table3,on='Features')
    result=pd.merge(result,table4,on='Features')
    result=pd.merge(result,table5,on='Features')
    result=pd.merge(result,table6,on='Features')

    print(result)
    result.to_csv('./csvfiles/importance.csv',encoding='utf-8',index=False)
    return result

finalresult()

'''
print('40:60')
print(rf_groupresult('4060.csv'))
print('50:50')
print(rf_groupresult('5050.csv'))
print('60:40')
print(rf_groupresult('6040.csv'))
'''

