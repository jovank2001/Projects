import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import enchant
from spacy.lang.en import English
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import Stemmer
import numpy as np
from sklearn.metrics import f1_score
import math

#Globals
max_sum_length = 10
min_summaries_word_appears_in = 30

#Ignore pandas warnings
pd.options.mode.chained_assignment = None  # default='warn'

#Read in and organize relevant training data
df = pd.read_excel("Train_data.xlsx", na_values = 'Missing')
df.drop(['sor', 'cdf_seq_no', 'trans_desc', 'db_cr_cd', 'payment_reporting_category', 'payment_category', 'default_brand', 'default_location', 'qrated_brand'], axis='columns', inplace=True)
target = df.copy()
target.drop(['merchant_cat_code', 'amt', 'coalesced_brand', 'is_international'], axis='columns', inplace=True)
df.drop('Category', axis='columns', inplace=True)
inputs = df

#Convert is_international flag to binary values
inputs = pd.get_dummies(inputs, columns=['is_international'], drop_first=True)

#Convert merchant cat codes to binary representation
#inputs = pd.get_dummies(inputs, columns=['merchant_cat_code'], drop_first=True, prefix = 'merchant_cat_code')#<-- Comment

#Open up BrandDescriptors.xlsx and fill in coalesced_brand column with the brand summaries
excel_data = pd.read_excel("BrandDescriptors.xlsx", usecols = [0])
brand_summaries = [x for x in excel_data['brand_summary']]


# Create our list of punctuation marks
punctuations = string.punctuation

# Create our list of stopwords
stop_words = spacy.lang.en.stop_words.STOP_WORDS

#English dictionary
d = enchant.Dict("en_US")

#Removes punctuation and stop words, and lemmatize
def cleaner(summary):

    #Split each summary into array of words
    mytokens = summary.split() 

    #Convert all words int lowercase
    mytokens = [word.lower() for word in mytokens]
    
    #Removing stop words and non english words
    mytokens = [word for word in mytokens if word not in stop_words and word not in punctuations and d.check(word)] 
    
    #Remove all numbers
    mytokens = [''.join([i for i in word if not i.isdigit()]) for word in mytokens]

    #Shorten each summary to be less than max_sum_length
    if len(mytokens) < max_sum_length:
        return mytokens
    else:
        return mytokens[:max_sum_length]
   
#Clean each summary
brand_summaries = [" ".join(cleaner(str(summary))) for summary in brand_summaries]


#Tfid Vectorizer
english_stemmer = Stemmer.Stemmer('en')
class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: english_stemmer.stemWords(analyzer(doc))

#Convert list of summaries into dataframe and turn into numeric representation with tfidf
df = pd.DataFrame(brand_summaries, columns = ['summaries'])
tfidf = StemmedTfidfVectorizer(min_df=min_summaries_word_appears_in, stop_words='english', analyzer='word', ngram_range=(1,1))
X = tfidf.fit_transform(df['summaries'])
df_summaries = pd.DataFrame(X.toarray(),columns=tfidf.get_feature_names_out())

#Append brand summary dataframe to dataframe containing merchant_cat_codes and other variables
inputs = pd.concat([inputs.iloc[:15000], df_summaries.iloc[:15000]], axis = 'columns')
inputs.drop('coalesced_brand', axis='columns', inplace=True)


#Convert target categories into numeric represenatation
target = pd.get_dummies(target.Category)

#Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(inputs, target.iloc[:15000], test_size=0.2, random_state=0)

##Train XGB model
#Initialize classifier
xgb_cl = xgb.XGBClassifier(learning_rate=0.3,
    n_estimators = 300,
    nthread=3,
    tree_method="hist")

# Fit
xgb_cl.fit(X_train, y_train)

# Predict
preds = xgb_cl.predict(X_test)

# Score
print(accuracy_score(y_test, preds))
print(f1_score(y_test, preds, average = 'weighted'))


##Fill in Test_data with predicted categories
#Open up Test Data
test_data_out = pd.read_excel("Test_data.xlsx", na_values = 'Missing')
test_data_o = pd.read_excel("Test_data.xlsx", na_values = 'Missing')
test_description = pd.read_excel("BrandDescriptorsTest.xlsx", usecols = [0])
brand_summaries_test = [x for x in test_description['brand_summary']]
test_data_o.drop(['coalesced_brand', 'sor', 'cdf_seq_no', 'trans_desc', 'db_cr_cd', 'payment_reporting_category', 'payment_category', 'default_brand', 'default_location', 'qrated_brand'], axis='columns', inplace=True)

#Convert is_international flag to binary values
test_data_o = pd.get_dummies(test_data_o, columns=['is_international'], drop_first=True)

#Clean Test Data
brand_summaries_test = [" ".join(cleaner(str(summary))) for summary in brand_summaries_test]

#Convert list of summaries into dataframe and turn into numeric representation with tfidf
df = pd.DataFrame(brand_summaries_test, columns = ['summaries'])
tfidf = StemmedTfidfVectorizer(min_df=min_summaries_word_appears_in, stop_words='english', analyzer='word', ngram_range=(1,1))
X = tfidf.fit_transform(df['summaries'])
X = pd.DataFrame(X.toarray(),columns=tfidf.get_feature_names_out())

#Adjust size of X to fit size of X_train (What the model learned to read from)
columns_train = X_train.columns
columns_nan = X.columns

for column in columns_train:
    for column_na in columns_nan:
        if column == column_na:
            X_train.loc[:,column] = X[column_na]
            break
            
X_predict = X_train.iloc[:X.shape[0]]
X_predict = X_predict.fillna(0)
#Predict and save
preds_na = xgb_cl.predict(X_predict)
preds_na = preds_na.tolist()


#Convert binary prediction to classification
preds_out_list = []
categories = ['Communication Services', 'Education', 'Entertainment', 'Finance',
       'Health and Community Services', 'Property and Business Services',
       'Retail Trade', 'Services to Transport',
       'Trade, Professional and Personal Services', 'Travel']

for pred in preds_na:
    if pred == [float(x) for x in [1,0,0,0,0,0,0,0,0,0]]:
        preds_out_list.append(categories[0])
    elif pred == [float(x) for x in [0,1,0,0,0,0,0,0,0,0]]:
        preds_out_list.append(categories[1])
    elif pred == [float(x) for x in [0,0,1,0,0,0,0,0,0,0]]:
        preds_out_list.append(categories[2])
    elif pred == [float(x) for x in [0,0,0,1,0,0,0,0,0,0]]:
        preds_out_list.append(categories[3])
    elif pred == [float(x) for x in [0,0,0,0,1,0,0,0,0,0]]:
        preds_out_list.append(categories[4])
    elif pred == [float(x) for x in [0,0,0,0,0,1,0,0,0,0]]:
        preds_out_list.append(categories[5])
    elif pred == [float(x) for x in [0,0,0,0,0,0,1,0,0,0]]:
        preds_out_list.append(categories[6])
    elif pred == [float(x) for x in [0,0,0,0,0,0,0,1,0,0]]:
        preds_out_list.append(categories[7])
    elif pred == [float(x) for x in [0,0,0,0,0,0,0,0,1,0]]:
        preds_out_list.append(categories[8])
    elif pred == [float(x) for x in [0,0,0,0,0,0,0,0,0,1]]:
        preds_out_list.append(categories[9])  
    else:
        preds_out_list.append(categories[6])
  
preds_out = pd.DataFrame(preds_out_list, columns = ['category'])
output = pd.concat((test_data_out, preds_out), axis = 'columns')
output.to_excel("Test_data_out.xlsx")






