# Wells Fargo Machine Learning Competition
## Summary
Led a team of University students to Design a machine learning algorithim for a Wells Fargo ML Challenge
There are ten different categories we must sort the Wells fargo transactions into; Finance, Travel, Retail trade, etc...
This program centers around a Wikipedia web scraper that takes in the coalesced_brand name and searches it in the WikiAPI 
It takes the summary from the WIKI page and then uses a TFID Vectorizer and stemmer on the summary page
Then uses that binary representation as another input to the XGBoost Categorizer model along with the merchant_cat_codes, amt, and is_international flag

## Challenge
#### Web Scraper
At first I tried to write my own web scraper that could take in a company name and then find that companies about us page on their respective website
However I discoverd the hard way that google puts a limit on the amount of web requests you can do in a certain amount of time before it flags your ip as potentially malicious and blocks you from making more requests (HTTP ERROR 429)
So I then tried to use a tor browser and IP switcher to fool Googles limitations, but unfortunately after many hours of trying I couldnt get the IP switching to  work properly and my time was limited so I decided to look into other solutions
I tried to find databases that contained company names and a associated description and eventually found the Wikipedia API tool and wrote a much simpler webscraper in runner.py
You can search directly on Wikipedia for a name and then grab whatever information Wikipedia has on that name, in my case I just pulled their summary page

Worked on project starting on June 20th through July 13th
Given transactions are in TrainData.xlsx and TestData.xlsx

#### To run:
First run runner.py on TrainData.xlsx
Then run runner.py on TestData.xlsx
Finally run main.py with filenames entered correctly
OutPut is written to TestDataOut.xlsx
