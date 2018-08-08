#!/usr/bin/env python

import numpy as np
import string
import re

class Objective:

    def __init__(self,sentence,com):
        self.sentence = sentence
        self.command = []
        self.person = []
        self.object = []
        self.location = []
        self.fromLocation = []
        self.toLocation = []
        self.furniture = []
        self.reference = []
        self.locationModifier = []
        self.command.append(com)

    def parse(self):
        #reads sentence and stores key words
        splitList = self.sentence.split()
        for word in splitList:
            test = ' ' + word + ' '
            if test in locations:
                self.location.append(word)
            elif test in furnitures:
                self.furniture.append(word)
            elif test in objects:
                self.object.append(word)
            elif test in people:
                self.person.append(word)
            elif test in references:
                self.reference.append(word)
            elif test in locModifiers:
                self.locationModifier.append(word)

        #uses modifier words 'to' and 'from' to fill in 'to' and 'from' locations - important in "take thing from x to y" tasks
        count = 0
        while len(self.locationModifier) > 0:
            word = self.locationModifier[0]
            #print "word: " + word
            if word == "from":
                try:
                    self.fromLocation.append(self.location[count])
                    del self.locationModifier[0]
                except IndexError:
                    #print "No location matching 'from' modifier"
                    del self.locationModifier[0]
            elif word == "to":
                try:
                    self.toLocation.append(self.location[count])
                    del self.locationModifier[0]
                except IndexError:
                    #print "No location matching 'to' modifier"
                    del self.locationModifier[0]
            count = count + 1




    def printme(self):
        #prints all fields in the objective that have values in them
        print ' '
        #print "task: "
        #print self.sentence
        print "command: "
        print self.command
        if len(self.person) > 0:
            print "people: "
            print self.person
        if len(self.object) > 0:
            print "objects: "
            print self.object
        if len(self.fromLocation) > 0:
            print "from location: "
            print self.fromLocation
        if len(self.toLocation) > 0:
            print "to location: "
            print self.toLocation
        if len(self.location) > 0:
            print "locations: "
            print self.location
        if len(self.furniture) > 0:
            print "furniture: "
            print self.furniture
        if len(self.reference) > 0:
            print "references: "
            print self.reference
        if len(self.locationModifier) > 0:
            print "modifiers: "
            print self.locationModifier

def process(task):
    #process the task, removing punctuation, the word 'and', converting to lower case and adding leading and trailing spaces
    print task
    taskP = task.translate(None, string.punctuation)
    nd = re.compile('(\s*)and(\s*)')
    taskP = nd.sub(' ', taskP)
    me = re.compile('(\s*)me(\s*)')
    taskP = me.sub(' user ', taskP)
    taskP = taskP.lower()
    taskP = ' ' + taskP + ' '
    return taskP

def objectify(taskP):
    #take processed task text and generate a list of Objective classes
    coms = []
    taskflags = []
    objectives = []
    #iterate through task looking for any commands, store them and their indexes in relevant list
    for word in taskP.split():
        test = ' ' + word + ' '
        index = commands.find(test)
        if index >-1:
            coms.append(word)
            index = taskP.find(test)
            if index >-1:
                taskflags.append(index)

    #use the indices of commands to split task into objectives
    objective1 = Objective(taskP[taskflags[0]+1:taskflags[1]],coms[0])
    objective2 = Objective(taskP[taskflags[1]+1:taskflags[2]],coms[1])
    objective3 = Objective(taskP[taskflags[2]+1:len(taskP)],coms[2])

    return [objective1,objective2,objective3]

def resolveReferences(objectives):
    #if an objective references an object or person mentioned earlier, look at the previous objective and copy object or person data into current objective
    for i in range(1,len(objectives)):
        while len(objectives[i].reference) > 0:
            ref = objectives[i].reference[0]
            if ref == "him" or ref == "her" or ref == "them":
                try:
                    objectives[i].person = objectives[i-1].person
                    del objectives[i].reference[0]
                except IndexError:
                    print "Failed to resolve reference for '" + ref + "'"
                    del objectives[i].reference[0]
            elif ref == "it":
                try:
                    objectives[i].object = objectives[i-1].object
                    del objectives[i].reference[0]
                except IndexError:
                    print "Failed to resolve reference for '" + ref + "'"
                    del objectives[i].reference[0]
            else:
                print "Unknown reference, how did this happen?"
                del objectives[i].reference[0]


# space separated strings to use when processing and parsing tasks
commands = " find locate look search pinpoint spot guide take lead accompany follow escort put place leave set get grasp retrieve pickup bring deliver give hand "

locations = " kitchen bedroom exit "

furnitures = " table cabinet bin "

objects = " apple bottle glasses pear cup "

people = " tracy john user "

references = " him her it them "

locModifiers = " from to "

#hard coded example commands - first four from ERL documentation
task1 = "Locate Tracy, lead her to the bedroom, and bring me an apple from the kitchen cabinet."

task2 = "Find the bottle, place it in the trash bin, and take John from the bedroom to the exit."

task3 = "Guide me to the bedroom, find my glasses, and bring me a pear from the kitchen table."

task4 = "Give me the cup on the coffee table, find John, and follow him."

task5 = "Hi Tiago, please will you go and find john, I need you to take him to the exit and then get me a bottle of water from the kitchen cabinet, thanks!"

#simplify text ease of use
taskP = process(task5)

#create objectives from task text
objectives = objectify(taskP)

#use task text to fill relevant variables in each objective
objectives[0].parse()
objectives[1].parse()
objectives[2].parse()

#attempt to change reference words (him, her etc) into the names of the objects/people they are referencing
resolveReferences(objectives)

#print objectives for user to read
objectives[0].printme()
objectives[1].printme()
objectives[2].printme()
