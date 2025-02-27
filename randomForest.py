#notes: 

#- for running on windows, I installed full Anaconda and it contains all the prereqs. Besides that, also have to do python nltk.download() and get the stopwords corpus. After that saw it working on windows with python BagOfWord.py

#- used material from:
#!/usr/bin/env python

#  Author: Angela Chapman
#  Date: 8/6/2014
#
#  This file contains code to accompany the Kaggle tutorial
#  "Deep learning goes to the movies".  The code in this file
#  is for Part 1 of the tutorial on Natural Language Processing.
#
# *************************************** #

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
#from KaggleWord2VecUtility import KaggleWord2VecUtility
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import cross_val_score


def review_to_words( raw_review ):
    # Function to convert a raw review to a string of words
    # The input is a single string (a raw movie review), and 
    # the output is a single string (a preprocessed movie review)
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(raw_review).get_text() 
    #
    # 2. Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    #
    # 3. Convert to lower case, split into individual words
    words = letters_only.lower().split()                             
    #
    # 4. In Python, searching a set is much faster than searching
    #   a list, so convert the stop words to a set
    stops = set(stopwords.words("english"))                  
    # 
    # 5. Remove stop words
    meaningful_words = [w for w in words if not w in stops]   
    #
    # 6. Join the words back into one string separated by space, 
    # and return the result.
    return( " ".join( meaningful_words ))   



if __name__ == '__main__':
    train = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'labeledTrainData.tsv'), header=0, \
                    delimiter="\t", quoting=3)
    test = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'testData.tsv'), header=0, delimiter="\t", \
                   quoting=3 )

    print('The first review is:')
    print(train["review"][0])

    #raw_input("Press Enter to continue...")


    #print 'Download text data sets. If you already have NLTK datasets downloaded, just close the Python download window...'
    #nltk.download()  # Download text data sets, including stop words

    # Initialize an empty list to hold the clean reviews
    clean_train_reviews = []

    # Loop over each review; create an index i that goes from 0 to the length
    # of the movie review list

    #print "Cleaning and parsing the training set movie reviews...\n"
    for i in range( 0, len(train["review"])):
        #clean_train_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(train["review"][i], True)))
        clean_train_reviews.append(review_to_words(train["review"][i])) #done by soheil, grabbed review_to_words from here : https://www.kaggle.com/c/word2vec-nlp-tutorial#part-1-for-beginners-bag-of-words
        


    # ****** Create a bag of words from the training set
    #
    #print "Creating the bag of words...\n"


    # Initialize the "CountVectorizer" object, which is scikit-learn's
    # bag of words tool.
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

    # fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
    train_data_features = vectorizer.fit_transform(clean_train_reviews)

    # Numpy arrays are easy to work with, so convert the result to an
    # array
    np.asarray(train_data_features)

    # ******* Train a random forest using the bag of words
    #
    #print "Training the random forest (this may take a while)..."


    # Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = 100)


    #BOOKMARK: working on corss validation
    crossValResults = cross_val_score(forest, train_data_features, train["sentiment"], scoring='accuracy', cv=5)
    print("crossValResults = "+str(crossValResults))

    if False:

        # Fit the forest to the training set, using the bag of words as
        # features and the sentiment labels as the response variable
        #
        # This may take a few minutes to run
        forest = forest.fit( train_data_features, train["sentiment"] )



        # Create an empty list and append the clean reviews one by one
        clean_test_reviews = []

        #print "Cleaning and parsing the test set movie reviews...\n"
        for i in range(0,len(test["review"])):
            #clean_test_reviews.append(" ".join(KaggleWord2VecUtility.review_to_wordlist(test["review"][i], True)))
            clean_test_reviews.append(review_to_words(test["review"][i])) #done by soheil, grabbed review_to_words from here : https://www.kaggle.com/c/word2vec-nlp-tutorial#part-1-for-beginners-bag-of-words

        # Get a bag of words for the test set, and convert to a numpy array
        test_data_features = vectorizer.transform(clean_test_reviews)
        np.asarray(test_data_features)

        # Use the random forest to make sentiment label predictions
        #print "Predicting test labels...\n"
        result = forest.predict(test_data_features)

        # Copy the results to a pandas dataframe with an "id" column and
        # a "sentiment" column
        output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )

        # Use pandas to write the comma-separated output file
        output.to_csv(os.path.join(os.path.dirname(__file__), 'data', 'Bag_of_Words_model_randomForest.csv'), index=False, quoting=3)
        #print "Wrote results to Bag_of_Words_model.csv"


