import math
import pandas
import sys

columns=['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm', 'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
'Temp3pm', 'RainToday', 'RainTomorrow']

categorical = ['Location','WindGustDir', 'WindDir9am', 'WindDir3pm', 'RainToday']
categoricalIndexes = [0, 6, 8, 9, 20]

numerical = ['MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine', 'WindGustSpeed', 'WindSpeed9am','WindSpeed3pm', 'Humidity9am', 'Humidity3pm', 'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
'Temp3pm']
numericalIndexes = [1,2,3,4,5,7,10,11,12,13,14,15,16,17,18,19]

def makeDatasets(train,test):
    train_dataset = pandas.read_csv(train, sep=",", header=None)
    test_dataset = pandas.read_csv(test, sep=",", header=None)
    train_dataset = train_dataset.set_axis(labels=columns, axis=1)
    test_dataset = test_dataset.set_axis(labels=columns, axis=1)
    train_dataset_yes = train_dataset[train_dataset['RainTomorrow'] == ' Yes'] 
    train_dataset_no = train_dataset[train_dataset['RainTomorrow'] == ' No'] 
    return (train_dataset_yes, train_dataset_no, test_dataset)

def calculateProbability(x, mean, std):
    result = 1.0/(std * math.sqrt(2 * math.pi))
    e_term = -0.5 * math.pow((x - mean)/std, 2)
    result = result * math.pow(math.e, e_term)

    if(result < math.pow(math.e, -10)):
        result = math.pow(math.e,-10)

    return result

def classifier(train_dataset1, train_dataset2, testRow):
    train_dataset_yes = train_dataset1
    train_dataset_no = train_dataset2

    means_yes = train_dataset_yes.mean(axis=0, numeric_only=True)
    stds_yes = train_dataset_yes.std(axis=0, numeric_only=True)

    means_no = train_dataset_no.mean(axis=0, numeric_only=True)
    stds_no = train_dataset_no.std(axis=0, numeric_only=True)

    c_yes = math.log(1./2, 10)
    c_no = math.log(1./2, 10)

    for category in categorical:
        if(category == 'Location'):
            yes = train_dataset_yes[category].value_counts()
            c_yes += math.log(yes[testRow[0]]/9911,10)
            
            no = train_dataset_no[category].value_counts()
            c_no += math.log(no[testRow[0]]/9911,10)
        if(category == 'WindGustDir'):
            yes = train_dataset_yes[category].value_counts()
            c_yes += math.log(yes[testRow[6]]/9911,10)
            
            no = train_dataset_no[category].value_counts()
            c_no += math.log(no[testRow[6]]/9911,10)
        if(category == 'WindDir9am'):
            yes = train_dataset_yes[category].value_counts()
            c_yes += math.log(yes[testRow[8]]/9911,10)
            
            no = train_dataset_no[category].value_counts()
            c_no += math.log(no[testRow[8]]/9911,10)
        if(category == 'WindDir3pm'):
            yes = train_dataset_yes[category].value_counts()
            c_yes += math.log(yes[testRow[9]]/9911,10)
            
            no = train_dataset_no[category].value_counts()
            c_no += math.log(no[testRow[9]]/9911,10)
        if(category == 'RainToday'):
            yes = train_dataset_yes[category].value_counts()
            c_yes += math.log(yes[testRow[20]]/9911,10)
            
            no = train_dataset_no[category].value_counts()
            c_no += math.log(no[testRow[20]]/9911,10)

    i=0
    for category in numerical:
        prob_yes = calculateProbability(testRow[numericalIndexes[i]], means_yes[category], stds_yes[category])
        c_yes += math.log(prob_yes,10)
        prob_no = calculateProbability(testRow[numericalIndexes[i]], means_no[category], stds_no[category])
        c_no += math.log(prob_no, 10)
        i += 1

    if(c_yes > c_no):
        return 1
    else:
        return 0

def train_and_test():
    datasets = makeDatasets(sys.argv[1],sys.argv[2])
    train_dataset_yes = datasets[0]
    train_dataset_no = datasets[1]
    test_dataset = datasets[2]

    test_dataset=test_dataset.drop(['RainTomorrow'],axis=1)

    for row in test_dataset.values.tolist():
        print(classifier(train_dataset_yes, train_dataset_no, row))
    

train_and_test()