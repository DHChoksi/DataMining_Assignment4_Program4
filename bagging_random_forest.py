#-------------------------------------------------------------------------
# AUTHOR: Dhruvi Choksi
# FILENAME: bagging_random_forest.py
# SPECIFICATION: implement base classifier, ensemble classifier, and Random Forest classifier to recognize handwritten digits.
# FOR: CS 5990- Assignment #4
# TIME SPENT: 3-4 hours
#-----------------------------------------------------------*/

#importing some Python libraries
from sklearn import tree
from sklearn.utils import resample
from sklearn.ensemble import RandomForestClassifier
import numpy as np

dbTraining = []
dbTest = []
X_training = []
y_training = []
classVotes = [] #this array will be used to count the votes of each classifier

#reading the training data from a csv file and populate dbTraining
#--> add your Python code here
with open('optdigits.tra', 'r') as file:
    for line in file:
        instance = [int(x) for x in line.strip().split(",")]
        dbTraining.append(instance)

#reading the test data from a csv file and populate dbTest
#--> add your Python code here
with open('optdigits.tes', 'r') as file:
    for line in file:
        instance = [int(x) for x in line.strip().split(",")]
        dbTest.append(instance)

#inititalizing the class votes for each test sample. Example: classVotes.append([0,0,0,0,0,0,0,0,0,0])
#--> add your Python code here
for _ in range(len(dbTest)):
    classVotes.append([0]*10)

accuracy = 0

print("Started my base and ensemble classifier ...")

for k in range(20): #we will create 20 bootstrap samples here (k = 20). One classifier will be created for each bootstrap sample

    bootstrapSample = resample(dbTraining, n_samples=len(dbTraining), replace=True)

    #populate the values of X_training and y_training by using the bootstrapSample
    #--> add your Python code here
    X_training = [instance[:-1] for instance in bootstrapSample]
    y_training = [instance[-1] for instance in bootstrapSample]

    #fitting the decision tree to the data
    clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=None) #we will use a single decision tree without pruning it
    clf = clf.fit(X_training, y_training)

    for i, testSample in enumerate(dbTest):
        #make the classifier prediction for each test sample and update the corresponding index value in classVotes
        prediction = clf.predict([testSample[:-1]])[0]
        classVotes[i][prediction] += 1

        if k == 0: #for only the first base classifier, compare the prediction with the true label of the test sample here to start calculating its accuracy
            if prediction == testSample[-1]:
                accuracy += 1

if k == 0: #for only the first base classifier, print its accuracy here
    accuracy /= len(dbTest)
    print("Finished my base classifier (fast but relatively low accuracy) ...")
    print("My base classifier accuracy: " + str(accuracy))
    print("")

#initialize accuracy for ensemble classifier
accuracy = 0

#now, compare the final ensemble prediction (majority vote in classVotes) for each test sample with the ground truth label to calculate the accuracy of the ensemble classifier (all base classifiers together)
#--> add your Python code here
for i, testSample in enumerate(dbTest):
    prediction = np.argmax(classVotes[i])
    if prediction == testSample[-1]:
        accuracy += 1

accuracy /= len(dbTest)

#printing the ensemble accuracy here
print("Finished my ensemble classifier (slow but higher accuracy) ...")
print("My ensemble accuracy: " + str(accuracy))
print("")

print("Started Random Forest algorithm ...")

#Create a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=20) #this is the number of decision trees that will be generated by Random Forest. The sample of the ensemble method used before

#Fit Random Forest to the training data
clf.fit(X_training, y_training)

#make the Random Forest prediction for each test sample.
#--> add your Python code here
rf_predictions = clf.predict([instance[:-1] for instance in dbTest])

#compare the Random Forest prediction for each test sample with the ground truth label to calculate its accuracy
#--> add your Python code here
accuracy = sum(1 for predicted, actual in zip(rf_predictions, [instance[-1] for instance in dbTest]) if predicted == actual) / len(dbTest)

#printing Random Forest accuracy here
print("Random Forest accuracy: " + str(accuracy))

print("Finished Random Forest algorithm (much faster and higher accuracy!) ...")
