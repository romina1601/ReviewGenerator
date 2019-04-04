#
#PLEASE CHANGE THE FOLDER CONTAINING THE TXT FILE CONTAINING THE ORIGINAL REVIEWS
#BASED ON WHERE YOU DOWNLOAD THIS PROJECT
#SEE LINE 21
#

from related import related as r
from antonyms import antonyms as a
from synonyms import synonyms as s
from sentimentAnalyzer import sentimentAnalyzer as sa
import requests
import os

#####################some variables ###################################
originalReviewsSet = []
fakeReviewSet = []


#change the working t=directory so we can read from text file inside the project's directory
#CHANGE HERE WITH THE CORRESPONDING FOLDER
folder = "E:/Romina/Facultate/An III/Sem I/IAI/FakeReviewsGenerator"
os.chdir(folder)

#build the original reviews dataset from the .txt file
#every review is on a single line; after every review there is a \n characterx
with open("originalPosRevs.txt", "r") as originalReviewsFile:
    originalReviewsSet = originalReviewsFile.read().splitlines()

#some introduction to the program
print("Welcome! This is the Fake Review Generator (FKG) v1.0.")
print("You can choose to chage the words from a review with their SYNONYMS, ANTONYMS or RELATED WORDS.")
print("For SYNONYMS, type s; for ANTONYMS type a; for RELATED WORDS type r")

#get the user input
typeOfRev = input("Please enter your choice: ")

#match the user input with one of the 3 cases
#if SYNONYMS is selected
if typeOfRev == "s":
    print("Now, you can choose to substitute only the ADJECTIVES, NOUNS, ADVERBS or ALL of them.")
    print("For ADJECTIVES type 'adj'; for NOUNS type 'noun'; for ADVERBS type 'adv'; for ALL of them type 'all'")
    choice = input("Please enter your choice: ")
    fakeReviewSet = s.validateReview(originalReviewsSet, choice)
    #print(fakeReviewSet)
    print("Finish")

#if ANTONYMS is selected
elif typeOfRev == "a":
    print("Now, you can choose to substitute only the ADJECTIVES or VERBS.")
    print("For ADJECTIVES type 'adj'; for VERBS type 'vb'")
    choice = input("Please enter your choice: ")
    fakeReviewSet = a.validateReview(originalReviewsSet, choice)
    #print(fakeReviewSet)
    print("Finish")

#if RELATED WORDS is selected
elif typeOfRev == "r":
    print("Now, you can choose to substitute only the ADJECTIVES, NOUNS or ALL of them.")
    print("For ADJECTIVES type 'adj'; for NOUNS type 'noun'; for ALL of them type 'all'")
    choice = input("Please enter your choice: ")
    fakeReviewSet = r.validateReview(originalReviewsSet, choice)
    #print(fakeReviewSet)
    print("Finish")

#any other input is invalid; exit the program
else:
    print("Your choice is invalid")
    exit

with open("E:/Romina/Facultate/An III/Sem I/IAI/FakeReviewsGenerator/fakeSynAdjFromPos.txt", "w") as fakeRevsFile:
    for review in fakeReviewSet:
        fakeRevsFile.write("%s\n" % review)

print("Lengtth of original file is: ", len(originalReviewsSet))
print("Length of fake reviews file is: ", len(fakeReviewSet))