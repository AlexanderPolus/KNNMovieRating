#Alexander Polus
#CS460G
#For: Dr. Brent Harrison
#2.15.18
#-------------------libraries----------------------------------
import sys
import math
#from tqdm import tqdm
#download pycharm
#-------------------indexing functions for simplicity----------
def movie(val):
    return int(val - 1)
def user(val):
    return int(val - 1)
#-------------------error function-----------------------------
def error(predicted, actual):
    return ((actual-predicted)**2)
#---------------Cosine Similarity Function---------------------------------
def CosineSimilarity(vec1, vec2): #
    #magnitude A
    presqrtA = 0
    for i in vec1:
        if i != 0:
            presqrtA += i**2
    magA = math.sqrt(presqrtA)

    #magnitude B
    presqrtB = 0
    for i in vec2:
        if i != 0:
            presqrtB += i**2
    magB = math.sqrt(presqrtB)
    #dot product
    dotproduct = 0
    for i in range(0,1682):
        if (vec1[i] != 0) and (vec2[i] != 0):
            dotproduct += (vec1[i] * vec2[i])
    #final value
    similarity = dotproduct / (magA * magB)
    return similarity

#---------------Validate Usage---------------------------------------------
if (len(sys.argv) != 1):
    print("Usage: Python3 KNN3.py")
    sys.exit(0)

base_file = open('u1-base.base')
whole_base_file = base_file.read()
base_rows = whole_base_file.split("\n")

base2d = []
for row in base_rows:
    base2d.append(row.split("\t"))
del base2d[-1] 
for row in base2d:
    for i in range(0,len(row)):
        row[i] = float(row[i])
#My data at this point is just the excel file in a 2d array
#--------------Make 5 folds in my data-------------------------------------
print("rows in file: ", len(base2d))
#we have 80,000 rows of data, and will split into 5 folds
fold1 = []
fold2 = []
fold3 = []
fold4 = []
fold5 = []
for i in range(0, len(base2d), 5):
    fold1.append(base2d[i])
    fold2.append(base2d[i+1])
    fold3.append(base2d[i+2])
    fold4.append(base2d[i+3])
    fold5.append(base2d[i+4])

#Get the compliment of each fold:
fold1comp = []
fold2comp = []
fold3comp = []
fold4comp = []
fold5comp = []
for i in range(0,16000):    #changed to 16,000 from 20,000 for correct range
    fold1comp.append(fold2[i])
    fold1comp.append(fold3[i])
    fold1comp.append(fold4[i])
    fold1comp.append(fold5[i])

    fold2comp.append(fold1[i])
    fold2comp.append(fold3[i])
    fold2comp.append(fold4[i])
    fold2comp.append(fold5[i])

    fold3comp.append(fold1[i])
    fold3comp.append(fold2[i])
    fold3comp.append(fold4[i])
    fold3comp.append(fold5[i])

    fold4comp.append(fold1[i])
    fold4comp.append(fold2[i])
    fold4comp.append(fold3[i])
    fold4comp.append(fold5[i])

    fold5comp.append(fold1[i])
    fold5comp.append(fold2[i])
    fold5comp.append(fold3[i])
    fold5comp.append(fold4[i])

#turn each compliment into a list of users:
movie_vector = []
for i in range(0,1682):
    movie_vector.append(0)

fold1training = []
fold2training = []
fold3training = []
fold4training = []
fold5training = []

#make each training set a full set of user movie vectors
for i in range(0,943):
    fold1training.append(movie_vector[:])
    fold2training.append(movie_vector[:])
    fold3training.append(movie_vector[:])
    fold4training.append(movie_vector[:])
    fold5training.append(movie_vector[:])


trainingsets = [fold1training, fold2training, fold3training, fold4training, fold5training]
foldcomps = [fold1comp, fold2comp, fold3comp, fold4comp, fold5comp]


for i in range(0,5):
    for row in foldcomps[i]:
        print(row)
        trainingsets[i][user(row[0])][movie(row[1])] = row[2]

#at this point I have 5 training and testing folds
def PredictAndFindError(user_profiles, testrow, k_value):
    #copy_user_profiles = user_profiles[:]
    #organize test row into pieces
    username = int(testrow[0] - 1)
    movie = int(testrow[1] - 1)
    actual_rating = int(testrow[2])
    
    #key/value pair of [most similar index, similarity value]
    top3mostsimilar = [[0,0]] * k_value
    #find all similarities excluding similarity to themselves, record index of top 3
    for i in range(0,len(user_profiles)):
        #exclude the test user
        if (i != username) and (user_profiles[i][movie] != 0):
            similarity = CosineSimilarity(user_profiles[username], user_profiles[i])
            set_flag = 0
            for similar_user in top3mostsimilar:
                if (set_flag == 0) and (similarity > similar_user[1]):
                    similar_user[0] = i
                    similar_user[1] = similarity      #update these properly
                    set_flag = 1
    #weighted average their 3 ratings for the movie (sim1*rat1+sim2*rat2+sim3*rat3) / (sim1+sim2+sim3)

    denominator = 0
    numerator = 0
    for similar_user in top3mostsimilar:
        denominator += similar_user[1]
        numerator += (similar_user[1] * user_profiles[similar_user[0]][movie])
    if denominator == 0: predicted_rating = 2.5
    else: predicted_rating = numerator / denominator
    
    #calculate error for that one instance
    error = ( (predicted_rating - actual_rating) ** 2 )
    return error


#Now I need to find the error for each K value 1,3,5,7,9:
#Error values for each k value:

#trainingsets = [fold1training, fold2training, fold3training, fold4training, fold5training]
print("Reaching computation... ")
testingsets = [fold1, fold2, fold3, fold4, fold5]
kvalues = [1, 3, 5, 7, 9]
finalerrors = []
#for each k value...
for j in range(0,5):
    folderrors = []
    #for each fold and corresponding training set....
    for i in range(0,5):
        folderror = []
        for row in testingsets[i]:
            error = PredictAndFindError(trainingsets[i], row, kvalues[j])
            folderror.append(error)
        avgfolderror = sum(folderror) / len(folderror)
        folderrors.append(avgfolderror)
        print("fold error: ", avgfolderror)
    kvalerror = sum(folderrors) / len(folderrors)
    print("kvalerror: ", kvalerror)
    finalerrors.append(kvalerror)

print("K = 1 error: ", finalerrors[0])
print("K = 3 error: ", finalerrors[1])
print("K = 5 error: ", finalerrors[2])
print("K = 7 error: ", finalerrors[3])
print("K = 9 error: ", finalerrors[4])







