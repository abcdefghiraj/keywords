""" Testing the setup"""
from __future__ import print_function
import os
from operator import itemgetter
from keywords import core


# Welcome message
print("\nkeywords v1.0")
print("-----------------------------------")
print("pwd: " + os.path.realpath(__file__))

MESSAGE = "Enter the text file path you want to read:"
CONFIRMATIONMESSAGE = "Try again?(Y/N):"
RAKE = core.Rake("assets/stopwords.txt")
# Event loop
FLAG = True
while FLAG:
    print("-----------------------------------")
    print(MESSAGE)
    FILEPATH = input()
    FILECONTENT = ""
    if not ".txt" in FILEPATH:
        print("\nThis utility only parses .txt files.")
        continue
    try:
        FILECONTENT = open(FILEPATH, mode='r').read()
        SCORES = RAKE.run(FILECONTENT)
        print("----Top 10 keywords----")
        COUNT = 1
        SORTEDSCORES = sorted(SCORES.items(), key=itemgetter(1))
        for candidate in SORTEDSCORES:
            print(candidate, SCORES[candidate])
            COUNT += 1
            if COUNT > 10:
                break
    except (OSError, IOError) as fileerror:
        print("Unable to load file.Please check the filepath.")
    print(CONFIRMATIONMESSAGE)
    FLAG = input().lower() == "y"

print("-----------------------------------")
print("Thank you!!")
#End
