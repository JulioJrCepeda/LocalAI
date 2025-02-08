from LLM import LLM
from Embedding import Embedding
from HelperFunctions import *
import streamlit as st


class AI:
    ai = LLM()
    textToVector = Embedding()
    shortTermList = []
    relativeContext = ""
    shortTermContext = ""
    longTermDict = {}
    saves = 0
        
    def __init__(self):
        self.shortTermContext = ""
        self.longTermDict = load_dict("Memory.json")

    def save_to_dictionary(self, stringText):
        sentences = get_sentences(stringText)
        sentencesGroup = combine_lines(sentences, 8)
        vectorList = self.textToVector.run(sentencesGroup)
        for index, item in enumerate(vectorList):
            key = tuple(item)
            self.longTermDict[key] = sentencesGroup[index]

    def save(self):
        #longTermDict = clean_up_memory(longTermDict, textToVector) #currently Experimental!
        self.shortTermContext = list_to_string(self.shortTermList)
        self.save_to_dictionary(self.shortTermContext)
        self.longTermDict = simple_clean(self.longTermDict)
        save_dict(self.longTermDict, "Memory.json")


    def getAnswer(self, input):

        if self.longTermDict: # get the 3 most relevant infromation from memory
            questionVector = self.textToVector.run(list_to_string(self.shortTermList) + " " + input)
            self.relativeContext = find_top_three(questionVector, self.longTermDict)

        self.shortTermContext = list_to_string(self.shortTermList) # get short-term context from list.

        result = self.ai.Run(self.relativeContext + self.shortTermContext, input)

        self.shortTermList.append("You: " + input)
        self.shortTermList.append("Bot: " + result)
        self.saves += 2

        
        if self.saves == 6: # save every loop
            self.shortTermContext = list_to_string(self.shortTermList)
            self.save_to_dictionary(self.shortTermContext)
            self.saves = 0


        while len(self.shortTermList) > 6: # remove the oldest message from the list.
            self.shortTermList.pop(0)

        return result


