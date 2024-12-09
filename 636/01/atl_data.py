# ============== AOTEAROA TOUR MANAGEMENT SYSTEM ==============
# Student Name: Yongzhen Jiang
# Student ID :  1162376
# =============================================================


# * * * * * * * * * ======= WARNING ======= * * * * * * * * * * * 
# * * * Do not add any functions or variables to this file. * * *  
# * * *    It will be deleted and replaced for marking.     * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

from datetime import date,datetime,timedelta



tours = {
    # itinerary is the list of destinations visited on the tour
    "UK": {"itinerary":["London","Stoke-On-Trent","Cotswolds","Ambleside","Glasgow","Edinburgh","Inverness","Loch Ness"],
           # age restriction is the integer age limit for taking the tour, tour participants must be at least this old
           "age_restriction":0,
           # tour groups - the tour date is the key, a list of tour participants (customers) is the value
           "groups":{date(2023,7,10):[816,923,343]}},
    "WestEurope": {"itinerary":["London","Paris","Madrid","Berlin"],
           "age_restriction":0,
           "groups":{date(2023,8,15):[810,801]}},
    "EastEurope": {"itinerary":["Berlin","Bucharest","Budapest","Minsk"],
           "age_restriction":18,
           "groups":{date(2025,6,24):[786],datetime(2025,2,21):[121],datetime(2024,2,20):[]}},
}


# [id, first_name, family_name, birthdate ,email address]
customers = [ 
	[816, 'Simon', 'Charles', date(1952,7,15), 'simon@charles.nz'],
	[923, 'Simone', 'Charles', date(1987,9,1), 'simone.charles@kiwi.nz'],
	[343, 'Charlie', 'Charles', date(1954,1,25), 'charlie@charles.nz'],
	[810, 'Kate', 'McArthur', date(1972,9,30), 'K_McArthur94@gmail.com'],
	[786, 'Jack', 'Hopere', date(1980,2,10), 'Jack643@gmail.com'],
	[801, 'Chloe', 'Mathewson', date(1980,3,15), 'Chloe572@gmail.com'],
	[121, 'Kate', 'McLeod', date(1952,7,15), 'KMcLeod112@gmail.com'],
    [924, 'Samantha', 'Charles', date(2013,7,24), 'simone.charles@kiwi.nz']
]


def unique_id():
    """
    This will return the next available ID as a new integer value
    that is one higher than the current maximum ID number in the list."""
    
    return max(list(zip(*customers))[0]) + 1


def display_formatted_row(row, format_str):
    """
    row is a list or tuple containing the items in a single row.
    format_str uses the following format, with one set of curly braces {} for each column:
       eg, "{: <10}" determines the width of each column, padded with spaces (10 spaces in this example)
       <, ^ and > determine the alignment of the text: < (left aligned), ^ (centre aligned), > (right aligned)
    The following example is for 3 columns of output: left-aligned 5 characters wide; centred 10 characters; right-aligned 15 characters:
        format_str = "{: <5}  {: ^10}  {: >15}"
    Make sure the column is wider than the heading text and the widest entry in that column,
        otherwise the columns won't align correctly.
    You can also pad with something other than a space and put characters between the columns, 
        eg, this pads with full stops '.' and separates the columns with the pipe character '|' :
           format_str = "{:.<5} | {:.^10} | {:.>15}"
    """
    # Convert a tuple to a list, to allow updating of values
    if type(row) == tuple: 
        row = list(row)
    # Loop through each item in the row, changing to "" (empty string) if value is None and converting all other values to string
    #   (Extra info:  enumerate() places a loop counter value in index to allow updating of the correct item in row)
    for index,item in enumerate(row):
        if item is None:      # Removes any None values from the row_list, which would cause the print(*row_list) to fail
            row[index] = ""       
        else:    
            row[index] = str(item)
    # Apply the formatting in format_str to all items in row
    print(format_str.format(*row))

