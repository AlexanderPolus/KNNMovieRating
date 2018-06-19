#Alexander Polus
#CS460G
#For: Dr. Brent Harrison
#2.15.18
#-------------------libraries----------------------------------
import sys
import math
#from tqdm import tqdm
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
train_file = open('u1-test.test')
whole_base_file = base_file.read()
whole_train_file = train_file.read()
#get each row
base_rows = whole_base_file.split("\n")
train_rows = whole_train_file.split("\n")

#split on spaces/tab for 2D array
base2d = []
train2d = []
for row in base_rows:
    base2d.append(row.split("\t"))
for row in train_rows:
    train2d.append(row.split("\t"))

del base2d[-1] #the last line of the file was a blank line, so I'm deleting that
del train2d[-1] #same as above


#trim off the last column cause we don't need it
for row in base2d:
    del row[-1]
for row in train2d:
    del row[-1]

#turn everything into a float:
for row in base2d:
    for i in range(0,len(row)):
        row[i] = float(row[i])
for row in train2d:
    for i in range(0,len(row)):
        row[i] = float(row[i])
#at this point my test table is done



for row in base2d:
    print(row)
pause = input("^ training data as floats")
for row in train2d:
    print(row)
pause = input("^ test data as floats")


#figure out the number of users:
raw_users = []
for row in base2d:
    raw_users.append(row[0])
num_users = max(raw_users)
print("There are ", num_users, " users")

#figure out number of movies:
raw_movies = []
for row in base2d:
    raw_movies.append(row[1])
num_movies = max(raw_movies)
print("there are ", num_movies, " movies")
pause = input("waiting...")
#---------------Organize the data into 2D array----------------------------
#here will be a "scatterplot" of values that looks like so:
#       movie1  movie2  movie3  ... movieX
#user1  1   2   3   0   5
#user2  3   4   5   2   1
#...
#userX                      etc....


#the 2d array will be first indexed by user, then by movie. The movie() and user() functions subtract 1 so the values match up since indexes start at zero
user_profiles = []
generic_user = []
for i in range(0,1682):
    generic_user.append(0)
for i in range(0,943):
    user_profiles.append(generic_user[:])  #[:] makes deep copy


#now I will update the array, so that each user's ratings are correctly valued:
for row in base2d:
    print(row)
    user_profiles[user(row[0])][movie(row[1])] = row[2]
print("number of user profiles: ", len(user_profiles))
print("number of movies being analyzed: ", len(user_profiles[0]))
pause = input("Click Enter to begin execution... ")


#print(user_profiles[0])

#training is done!


#USERS ARE THE SAME ACROSS TRAINING AND TEST SET~~~~~~~~~~~~~~~~~~~~~~~~~

#excluding the user at hand in each testing row, find 3 largest val similarities of other users who have seen the movie of concern - make subset
def PredictAndFindError(testrow):
    #pass as global instead of argument
    global user_profiles
    #copy_user_profiles = user_profiles[:]
    #organize test row into pieces
    username = int(testrow[0] - 1)
    movie = int(testrow[1] - 1)
    actual_rating = int(testrow[2])

    #key/value pair of [most similar index, similarity value]
    top3mostsimilar = [[0,0], [0,0], [0,0]]
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

#make vector to record all errors and run that function on every row in test data
error_values = []
for testrow in train2d:
    error = PredictAndFindError(testrow)
    error_values.append(error)
    print("Error: ", error)
#find average error
average_error_on_data = sum(error_values) / len(error_values)
print("Average error across test for K=3 approach: ", average_error_on_data)







