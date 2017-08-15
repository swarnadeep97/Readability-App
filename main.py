#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function

import os
import sys
import nltk
import re

from nltk import pos_tag, word_tokenize
from itertools import dropwhile
import postagger

global TAGGER
TAGGER = postagger.get_tagger()

# The code for the detection of passive voice has been done with help from https://github.com/j-c-h-e-n-g/nltk-passive-voice

def tag_sentence(sent):
	"""Take a sentence as a string and return a list of (word, tag) tuples."""
	assert isinstance(sent, basestring)

	tokens = word_tokenize(sent)
	return TAGGER.tag(tokens)

def passivep(tags):
	postToBe = list(dropwhile(lambda(tag): not tag.startswith("BE"), tags))
	nongerund = lambda(tag): tag.startswith("V") and not tag.startswith("VBG")

	filtered = filter(nongerund, postToBe)
	out = any(filtered)

	return out

def oneline(sent):
	return sent.replace("\n", " ").replace("\r", " ")

def print_if_passive(sent):
	tagged = tag_sentence(sent)
	tags = map( lambda(tup): tup[1], tagged)

	if passivep(tags):
		print ("(passive)", end='')

punkt = nltk.tokenize.punkt.PunktSentenceTokenizer()
def findpassives(lines):
	sentences = punkt.tokenize(lines)

	for sent in sentences:
		print_if_passive(sent)


# findpassives("./input.txt")

totalwords=0
totalsentences=0
totalparagraphs=0
totalsyllables=0

# This function is made by taking help from http://eayd.in/?p=232
def sylco(word) :
 
	word = word.lower()
 
	# exception_add are words that need extra syllables
	# exception_del are words that need less syllables
 
	exception_add = ['serious','crucial','sentences','trying','blue','meandering']
	exception_del = ['fortunately','unfortunately','facebook','something','writes']
 
	co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
	co_two = ['coapt','coed','coinci']
 
	pre_one = ['preach']
 
	ans = 0 
	discard = 0
 
	if len(word) <= 3 :
		ans = 1
		return ans
  
	if word[-2:] == "es" or word[-2:] == "ed" :
		doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]',word))
		if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]',word)) > 1 :
			if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
				pass
			else :
				discard+=1

	le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
 
	if word[-1:] == "e" :
		if word[-2:] == "le" and word not in le_except :
			pass
 
		else :
			discard+=1
 
	doubleAndtripple = len(re.findall(r'[eaoui][eaoui]',word))
	tripple = len(re.findall(r'[eaoui][eaoui][eaoui]',word))
	discard+=doubleAndtripple + tripple
 
	numVowels = len(re.findall(r'[eaoui]',word))
 
	if word[:2] == "mc" :
		ans+=1
 
	if word[-1:] == "y" and word[-2] not in "aeoui" :
		ans +=1
 
	for i,j in enumerate(word) :
		if j == "y" :
			if (i != 0) and (i != len(word)-1) :
				if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
					ans+=1
 
	if word[:3] == "tri" and word[3] in "aeoui" :
		ans+=1
 
	if word[:2] == "bi" and word[2] in "aeoui" :
		ans+=1
 
	if word[-3:] == "ian" : 
		if word[-4:] == "cian" or word[-4:] == "tian" :
			pass
		else :
			ans+=1
 
	if word[:2] == "co" and word[2] in 'eaoui' :
 
		if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
			ans+=1
		elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
			pass
		else :
			ans+=1
 
	if word[:3] == "pre" and word[3] in 'eaoui' :
		if word[:6] in pre_one :
			pass
		else :
			ans+=1
 
	negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
 
	if word[-3:] == "n't" :
		if word in negative :
			ans+=1
		else :
			pass  
 
	if word in exception_del :
		discard+=1
 
	if word in exception_add :
		ans+=1    
 
	return numVowels - discard + ans


f=open("./input.txt")


for line in f:
	check=0
	for word in line.split():
		check=1

		# removing punctuations
		temp = word.strip('.')

		# new sentence after a .
		if temp!=word:
			totalsentences=totalsentences+1
		word = word.strip('.,?!;:—')
		

		# removing the special case of hyphenation
		newword=""
		for i in word:
			if i!="-":
				newword+=i
			else:
				totalwords=totalwords-1
				newword+=' '

		for IndividualWord in newword.split():
			totalwords+=1
			totalsyllables=totalsyllables+sylco(IndividualWord)
	
	if check==1:
		totalparagraphs=totalparagraphs+1

# print(totalparagraphs)
# print(totalsentences)
# print(totalwords)
# print(totalsyllables)


f=open("./input.txt")

orig_stdout = sys.stdout
out = open('output.txt', 'w')
sys.stdout = out
print("Readability = ", end='')
print("%.2f" % (0.39*totalwords/totalsentences+11.8*totalsyllables/totalwords-15.59))
print("-------------------")
check=0
for newline in f:
	for lines in newline.split("."):
		findpassives(lines)
		text = word_tokenize(lines)
		tagged_text=nltk.pos_tag(text)
		check=0
		for tagged_words in tagged_text:
			if tagged_words[0]==',':
				print(",", end='')
				continue
			if tagged_words[0]==';':
				print(";", end='')
				continue
			if tagged_words[0][0]=='\'':
				if tagged_words[1]=="RB":
					print("(adverb)"+tagged_words[0], end='')
				else:
					print(tagged_words[0], end='')
				continue
			if check==1:
				print(" ", end='')
			if tagged_words[1]=="RB":
				print("(adverb)"+tagged_words[0], end='')
			else:
				print(tagged_words[0], end='')

			check=1

		if lines!="\n" and lines!="":
			print(". ", end='')
	print("\n", end='')

# f=open("./input.txt")
# for newline in f:
# 	print(" ")
# 	text = word_tokenize(newline)
# 	tagged_text=nltk.pos_tag(text)
# 	print(tagged_text)












