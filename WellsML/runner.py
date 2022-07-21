#Creates excel file BrandDescriptors.xlsx that contains a summary of each brand in Train_data.xlsx
#Gets summary from wikipediaapi
import time
import pandas as pd
import xlsxwriter
import wikipediaapi
import string
import time
import wikipedia

#Start stopwatch
start_time = time.time()


#Load the xlsx file and turn each column into it own list
#Load coalesced_brands from training data
excel_data = pd.read_excel("Test_data.xlsx", usecols = [12], na_values = "Missing")
coalesced_brands = [x for x in excel_data['coalesced_brand']]



#Open excel doc
workbook = xlsxwriter.Workbook('BrandDescriptorsTest.xlsx')
worksheet = workbook.add_worksheet()
row = 0
column = 0


#Function to get summary from wikipedia using wikipediapi
wiki_wiki = wikipediaapi.Wikipedia('en')
def scrape(name):
    #Account for names that arent of type string
    if not isinstance(name, str):
        return name
    #Handle name with only digits
    if name.isnumeric():
        return name
   
    #Search wikipedia for title of wikipage associated with the company
    company_name = name.rstrip(string.digits)
    wikistring = "{brand} company".format(brand=company_name)
    wikistring = company_name
    searchresults = wikipedia.search(wikistring)    
    
   
    #Make sure we got a search result
    if len(searchresults) > 0:
        title = searchresults[0]
        #Pulls up wikipedia page from the title
        page_py = wiki_wiki.page(title)
        return page_py.summary
    #Handle no wikipedia page
    else:
        return company_name


#Convert brand names into a short description of what the company does and store descriptions in list(main)
for brand in coalesced_brands:
    scraped_brand = scrape(brand)
    worksheet.write(row, column, scraped_brand)
    print("Writing to row: " + str(row))
    row += 1
    
#Close workbook and report run time
workbook.close()
print("--- %s seconds ---" % (time.time() - start_time))

  


