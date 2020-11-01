import csv
import sys
import copy
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    print(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")

    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def conv_month_num():
    month = dict()
    month["Jan"] = 0
    month["Feb"] = 1
    month["Mar"] = 2
    month["Apr"] = 3
    month["May"] = 4
    month["June"] = 5
    month["Jul"] = 6
    month["Aug"] = 7
    month["Sep"] = 8
    month["Oct"] = 9
    month["Nov"] = 10
    month["Dec"] = 11
    return month
def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    month = conv_month_num()

    with open(f"{filename}") as f:
        reader = csv.reader(f)
        next(reader)

        evidence = []
        labels = []
        for row in reader:
            L=[]
            L.append(int(row[0]))
            L.append(float(row[1]))
            L.append(int(row[2]))
            L.append(float(row[3]))
            L.append(int(row[4]))
            L.append(float(row[5]))
            for i in range(4):
                L.append(float(row[6+i]))
            L.append(int(month[f"{row[10]}"]))
            for i in range(4):
                L.append(int(row[11+i]))
            if row[15]== "Returning_Visitor":
                L.append(1)
            else:
                L.append(0)
            if row[16]=="TRUE":
                L.append(1)
            else:
                L.append(0)
            M = copy.deepcopy(L)
            evidence.append(M)
            if row[17]=="TRUE":
                labels.append(1)
            else:
                labels.append(0)
            L.clear()
    return (evidence,labels)




    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(evidence,labels)
    return model
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    i=0
    j=0
    total_true = 0
    total_wrong = 0
    for label,prediction in zip(labels,predictions):
        if label==1:
            total_true = total_true + 1
            if prediction == 1:
                i = i + 1
        else:
            total_wrong = total_wrong + 1
            if prediction == 0:
                j = j + 1
    sensitivity = float(i/total_true)
    specificity = float(j/total_wrong)
    return(sensitivity, specificity)




    raise NotImplementedError


if __name__ == "__main__":
    main()
