# Wells Fargo Machine Learning Competition
## Summary
We are given basic information about a transaction and must use that information to deterimine which category the transaction belongs to
There are ten different categories we must sort the transactions into; Finance, Travel, Retail trade, etc...
This program centers around a Wikipedia web scpraer that takes in the coalesced_brand name and searches it in the WikiAPI 
It takes the summary from the WIKI page and then uses a TFID Vectorizer and stemmer on the summary page
Then uses that binary representation as another input to the XGBoost Catogrizer model along with the merchant_cat_codes, amt, and is_international flag

## Challenges
#### Web Scraper
At first I tried to write my own web scraper that could take in a name and then find that companies about us page on their respective website
However I discoverd the hard way that google puts a limit on the amount of web requests you can do in a certain amount of time before it flags your ip as potentially malicious and blocks you from making more requests (HTTP ERROR 429)
So I then tried to use a tor browser and IP switcher to fool Googles limitations, but unfortunately after many hours of trying I couldnt get the IP switching to  work properly and my time was limited so I decided to look into other solutions
I tried to find databases that contained company names and a associated description and eventually found the Wikipedia API tool and wrote a much simpler webscraper in runner.py
You can search directly on Wikipedia for a name and then grab whatever information Wikipedia has on that name, in my case I just pulled the summary page

#### Blank merchant cat codes
Approximately 40% of the merchant_cat_codes in the training data are left blank
The merchant_cat_codes were key for transaction categorizing
I looked for awhile but couldnt find out how WellsFargo specifically determined the cat codes. At the same time I found out that XGBoost supposedly could hand NaN values well so I put the idea of filling the cat codes on the backburner
However on the last day as I was trying to get the accuracy score up I decided to give it one last try and ended up figuring out that Visa actually assigned the cat codes and WellFargo just uses what Visa gives them
I was able to find a key with each of the ~900 cat codes and a description of what businesses they correspond to on visas website
I stayed up the whole night before the project was due and trained another XGBoost model that used NLP on the merchant cat code key descriptions appended with the 25,000 transanactions that we were given in TrainData that had a merchant_cat_code and brand summary
The inputs to this new model were the TFIDF vectorized brand summaries and key decriptions. The target was the merchant cat code keys
I got the model working and then used this model to predict the merchant cat codes of the 15,000 transactions that didnt have one
It semmed to work well but when I filled in the cat codes and ran my main XGBoost model the accuracy score actually went down
Unfortunately at this point I had to submit the project soon and didnt have time for another solution
I think I needed to use a different approach to handling the Visa key that dosent involve using the training data
The training data most likely overshadowed the Visa key in the models mind but I couldnt just use the Visa key because it only had one instance of each cat code and that wouldnt be enough data to train an effective model on and would most likely cause underfitting
If I had more time I would have used a synonym generator that could create 9 additional descriptions for each of the 900 merchant cat code business descriptions to increase the amount of data we had and then run a model just on that key data. This would have been more precise data to feed a model and wouldnt rely on the Training data.


Worked on project starting on June 20th through July 13th
Given transactions are in TrainData.xlsx and TestData.xlsx

To run:
First run runner.py on TrainData.xlsx
Then run runner.py on TestData.xlsx
Finally run main.py with filenames entered correctly
OutPut is written to TestDataOut.xlsx
