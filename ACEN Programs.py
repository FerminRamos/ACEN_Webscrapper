# TODO: Pulls All ACEN Accredited Colleges of Nursing, located in United States.
#  ACEN website (https://www.acenursing.org/search-programs/). Has the ability to exclude
#  certain Program Types, if needed.

import csv

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def getTable(soup):
    return soup.find('table')


def getTableItems(soup):
    return soup.find_all('td')


def extractData(tableItems):
    data = []
    for item in tableItems:
        data.append(item.text.strip())
    return data


def groupByRow(items):
    groupSize = 4
    subList = [items[n:n+groupSize] for n in range(0, len(items), groupSize)]
    return subList


# Looks through dataset and removes any that have degree type "Practical". Use as needed.
def filterByProgramType(data):
    excludedDegreeType = ["Practical", "Associate", ""]

    filteredDataset = []
    for d in data:
        if d[1] not in excludedDegreeType:
            filteredDataset.append(d)
    return filteredDataset

    # filteredDataset = []
    # for d in data:
    #     if d[1] != "Practical":
    #         filteredDataset.append(d)
    # return filteredDataset


def mergeDatasets(d1, d2):
    return d1 + d2


# TODO: This is main.
dataset = []
statesList = ["Alabama", "Alaska", "American Samoa", "Arizona", "Arkansas", "California", "Colorado",
              "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii",
              "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
              "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana",
              "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
              "North Carolina", "North Dakota", "Northern Mariana Islands", "Ohio", "Oklahoma", "Oregon",
              "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
              "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
              "Wisconsin", "Wyoming", "Washington, DC", "Virgin Islands", "Guam"]
pgNum = 1

for state in statesList:
    websiteHasNextPage = True

    while websiteHasNextPage:

        # Send an HTTP GET request to the website
        if state != "Washington, DC":
            url = f"https://www.acenursing.org/search-programs/?GovOrg&Program&State={state.capitalize()}&Status=Accredited&frm-page-168018={str(pgNum)}"  # Replace with the URL of the website you want to scrape
        else:
            url = f"https://www.acenursing.org/search-programs/?GovOrg=&Program=&State=Washington%2C+DC&Status=Accredited&frm-page-168018={str(pgNum)}"
        website = requests.get(url)

        # Check if the request was successful (status code 200)
        if website.status_code == 200:

            # 1. Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(website.content, "html.parser")

            # 2. Check if website has Table
            table = getTable(soup=soup)
            if table is not None:  # Yes, has table...

                # 3. Extract the desired data from Table
                tableItems = extractData(getTableItems(table))

                # 3. Extraction leaves individual strands of data, group them by rows
                tableItems = groupByRow(tableItems)

                # 4. Display dataset to user
                print(tabulate(tableItems, headers=[f"Colleges in {state}, pg. {pgNum}", "Program Type", "State/Country", "Status"]), end='\n\n')

                # 5. Add new data to existing
                dataset = mergeDatasets(dataset, tableItems)

                pgNum += 1

            else:  # No, does NOT have table...
                print("\n##########################")
                print(f"# FINISHED STATE IN LIST #  {state.upper()}")
                print("##########################\n")
                websiteHasNextPage = False  # Go to next state
                pgNum = 1

        else:
            print("Failed to retrieve data from the website.\n")
            exit(1)


# Filter Datasets, uncomment if needed.
dataset = filterByProgramType(data=dataset)


# Write to CSV
print("\t\t\t\t##########################")
print("\t\t\t\t# FINAL COMPILED DATASET #")
print("\t\t\t\t##########################")
print(tabulate(dataset))
with open("Webscrapper Output/ACEN Colleges of Nursing.csv", mode='w', encoding='utf-8', newline='') as csvFile:
    csvWriter = csv.writer(csvFile)
    dataset.insert(0, ["ACEN Colleges of Nursing", "Program Type", "State/Country", "Status"])
    csvWriter.writerows(dataset)
