import math
import pandas as pd
import sys

def NaiveBayes(test_i,X_train):
    c_yes=0
    c_no=0
    Total=len(X_train)
    count_yes=0
    count_no=0
    for i in X_train:
        if i[-1]==' Yes':
            count_yes+=1
    count_no=Total-count_yes
#     print(count_yes,' ',count_no)
    c_yes=math.log(count_yes/Total)
    c_no=math.log(count_no/Total)
    print(c_yes)
    print(c_no)
    count_xi_yes=[0]*len(test_i)
    count_xi_no=[0]*len(test_i)
    
    
    for i in range(len(X_train[0])-1):
        for j in X_train:
            if(test_i[i]==j[i]) and (j[-1]==" Yes"):
                count_xi_yes[i]+=1
            if(test_i[i]==j[i]) and (j[-1]==" No"):
                count_xi_no[i]+=1
    
#     for i in count_xi_yes:
#         print(i)
#     print()
#     for i in count_xi_no:
#         print(i)
    
    likelihood_yes=[]
    likelihood_no=[]
    
    for i in count_xi_yes:
        likelihood_yes.append(math.log((i+1)/(count_yes+2)))
        
    for i in count_xi_no:
        likelihood_no.append(math.log((i+1)/(count_no+2)))
        
        
#     for i in likelihood_yes:
#         print(i)
#     print()
#     for i in likelihood_no:
#         print(i)
        
    c_yes += sum(likelihood_yes)
    c_no += sum(likelihood_no)
    
    if(c_yes>c_no):
        return 1
    else:
        return 0

def main():
    train = pd.read_csv(sys.argv[1], sep=",",header = None)
    test = pd.read_csv(sys.argv[2], sep=",",header = None)

    colnames=['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
'Temp3pm', 'RainToday', 'RainTomorrow']
    
    train =train.set_axis(colnames, axis=1, inplace=False)
    test =test.set_axis(colnames, axis=1, inplace=False)

    labels4 = ['Q1','Q2','Q3','Q4']
    for i in train.columns:
        if all(isinstance(x,float) for x in train[i]) and i != "Rainfall":
            train[i] =  pd.qcut(x = train[i], q=4, labels = labels4)
    train['Rainfall']= pd.qcut(x = train['Rainfall'], q=3,labels = ['Q1','Q2'],duplicates='drop')
    y_train=train['RainTomorrow'].values.tolist()
    X_train=train.drop(['Location'],axis=1).values.tolist()
    print(X_train)
    

    # for i in test.columns:
    #     if all(isinstance(x,float) for x in test[i]) and i != "Rainfall":
    #         test[i] =  pd.qcut(x = test[i], q=4, labels = labels4)
    # test['Rainfall']= pd.qcut(x = test['Rainfall'], q=3,labels = ['Q1','Q2'],duplicates='drop')
    # y_test=test['RainTomorrow'].values.tolist()
    # X_test=test.drop(['Location','RainTomorrow'],axis=1).values.tolist()

    # test_labels=[]
    # for i in y_test:
    #     if i == ' Yes':
    #         test_labels.append(1)
    #     if i== ' No':
    #         test_labels.append(0)

    # predictions=[]
    # for i in X_test:
    #     predictions.append(NaiveBayes(i,X_train))

    # for i in predictions:
    #     print(i)

main()