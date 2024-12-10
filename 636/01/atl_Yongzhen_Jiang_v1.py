# ============== AOTEAROA TOURISM MANAGEMENT SYSTEM ==============
# Student Name: Yongzhen Jiang
# Student ID :  1162376
# ================================================================
 
from datetime import datetime, date, timedelta     # datetime module is required for working with dates
import re                                          # used to check against email format

# Make the variables and function in atl_data.py available in this code (without needing 'atl_data.' prefix)
from atl_data import customers, tours, unique_id, display_formatted_row   


# red = '\033[91m'
# green = '\033[92m'
# blue = '\033[94m'
# yellow = '\033[93m'
# magenta = '\033[95m'
# cyan = '\033[96m'
# reset = '\033[0m'

def red(format_str):
    return format_str.replace("{", "\033[91m{").replace("}", "}\033[0m")

def green(format_str):
    return format_str.replace("{", "\033[92m{").replace("}", "}\033[0m")

def blue(format_str):
    return format_str.replace("{", "\033[94m{").replace("}", "}\033[0m")

def yellow(format_str):
    return format_str.replace("{", "\033[93m{").replace("}", "}\033[0m")

def magenta(format_str):
    return format_str.replace("{", "\033[95m{").replace("}", "}\033[0m")

def cyan(format_str):
    return format_str.replace("{", "\033[96m{").replace("}", "}\033[0m")

# ----------------------- Start of Internal functions -----------------------
def display_customer_list(customers):
    """
    Display all customer"""

    print('-'*96)
    format_str = "| {: <5} | {: <15} | {: <15} | {: <15} | {: <30} |"            # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","First Name","Family Name","Birth Date","E-Mail"], green(format_str))     # Use the display_formatted_row() function to display the column headers with consistent spacing
    print('-'*96)

    if len(customers) == 0:
        display_formatted_row(['No Customer'], "| {: <92} |")

    else:
        for customer in customers:
            id = customer[0]
            fname = customer[1]
            famname = customer[2]
            birthdate = customer[3].strftime("%d %b %Y")
            email = customer[4]

            display_formatted_row([id,fname,famname,birthdate,email],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing

    print('-'*96)


def display_tour_groups(tour_groups):
    """
    Display tour groups"""

    print()
    print("-"*96)
    format_str = "| {: <5} | {: <33} | {: <48} |"
    display_formatted_row(['No', 'Tour Group', 'Tour Date'], green(format_str))
    print("-"*96)

    for index, tg in enumerate(tour_groups):
        display_formatted_row([index + 1, tg[0][0], get_datetime(tg[0][1]).strftime("%d %b %Y")], format_str)
    
    print("-"*96)


def is_email(email):
    """
    Check email address format using regex"""

    email_patter = r'^\S+@\S+\.\S+$'
    return re.match(email_patter, email)


def is_valid_date(birth_date):
    """
    Check whether the birth date is a valid date"""

    try:
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y')

        if birth_date.date() > date.today():
            return 'Later than today'
        elif birth_date.date() < yearsago(110, date.today()):
            return 'Earlier than 110 years ago'
        else:
            return birth_date.date()
    except ValueError:
        return 'Incorrect date format'


def yearsago(years, current_date=None):
    """
    Calcuate the date which is N years ago"""

    if current_date is None:
        current_date = datetime.today().date()

    try:
        return current_date.replace(year=current_date.year - years)
    except ValueError:
        # Leap year and is 29 Feb
        return current_date.replace(year=current_date.year - 100, month=2, day=28)


def is_customer_id_existed(id):
    """
    Check whether the customer id is already existed"""

    ids = [c[0] for c in customers]
    return id in ids


def is_tour_group_existed(tour_group_no, tour_groups):
    """
    Check whether the tour group which user selects is within the available groups"""

    return tour_group_no > 0 and tour_group_no <= len(tour_groups)


def is_customer_already_in_tour_group(customer_id, tour_group_no, tour_groups):
    """
    Check whether the customer id is already existed in the tour group"""

    return customer_id in tour_groups[tour_group_no - 1][1][1]


def is_customer_age_valid(customer_id, tour_group_no, tour_groups):
    """
    Check whether the age of the customer is equal or larger than the restricted age"""

    date_of_birth = [c[3] for c in customers if c[0] == customer_id][0]
    age_restricted = tour_groups[tour_group_no - 1][1][0]

    return get_customer_age(date_of_birth) >= age_restricted


def get_customer_age(birthday):
    """
    Get the customer's age"""

    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def _add_customer_to_tourgroup(customer_id, tour_group_no, tour_groups):
    """
    Add the customer into the tour group selected"""

    group_date = tour_groups[tour_group_no - 1][0][1]
    new_group_member = tour_groups[tour_group_no - 1][1][1] + [customer_id]

    groups = tours[tour_groups[tour_group_no - 1][0][0]]["groups"]

    groups.update({
        group_date: new_group_member
    })


def get_tour_groups():
    """
    Re-structure tours data, grouped by pair of (tour_name, tour_date), and sorted by tour_name ascending, tour_date ascending.
    Because pair of (tour_name, tour_date) is unique."""

    # Transform tours data into a dictionary with (tour_name, tour_date) as key, and (age_restriction, customer_member_list) as value
    # Data structure would be like: {('WestEurope', date(2023,8,15)): (0, [810,801])}
    tour_groups = {}
    for tour in tours.items():
        for group in tour[1]['groups'].items():
            tour_groups.update({(tour[0], group[0]): (tour[1]["age_restriction"], group[1])})

    # sort by group data ascending (use reverse=True to sort descending)
    tour_groups = sorted(tour_groups.items(), key=lambda x: get_datetime(x[0][1]), reverse=False)

    # sort by tour name ascending
    tour_groups = sorted(tour_groups, key=lambda x: x[0][0], reverse=False)

    return tour_groups


def display_customer_by_tour_group(tour_groups):
    """
    Display customers grouped by tour group"""

    customers_dict = get_customers_dict(customers)

    for tg in tour_groups:
        print()

        print('-'*96)
        print('| Tour  |', end="")
        display_tour_group_header(tg[0][0], tg[0][1])

        if len(tg[1][1]) == 0:
            display_customer_list([])
        else:
            customer_list = []
            for c in tg[1][1]:
                customer_list.append(customers_dict[c])
            display_customer_list(customer_list)


def display_tour_group_header(tour_name, tour_date):
    """
    Display tour group header"""

    format_str = "{: <34} | {: <15} | {: <30} |"
    display_formatted_row([tour_name, tour_date.strftime('%b %Y'), tour_date.strftime('%d %b %Y')], cyan(format_str))


def display_tour_details(tours):
    """
    Display tour details"""
    
    for tour in tours:
        # print(tour[0])
        print()
        print('-'*109)
        print('| Tour         |', end='')
        display_formatted_row([tour[0]], cyan(" {: <90} |"))
        print('-'*109)
        print('| Destinations |', end='')
        display_formatted_row([', '.join(tour[1]['itinerary'])], green(" {: <90} |"))
        print('-'*109)
        # print(', '.join(tour[1]['itinerary']))


def get_all_destinations_with_tour():
    """
    Get all destinations, each with a tour list whose itinerary contains this destination
    """

    destinations = set()

    # Add all destinations into a set (so there's no duplicate destination)
    for tour in tours.items():
        destinations |= set(tour[1]['itinerary'])

    # Sort destinations by name ascending
    destinations = sorted(destinations)

    # Create a list of touple, each tuple is a pair of (destination, tour_list)
    destinations_tour = []
    for d in destinations:
        tour_list = []
        for tour in tours.items():
            if d in tour[1]['itinerary']:
                tour_list.append(tour[0])
        tour_list = sorted(tour_list)
        destinations_tour.append((d, tour_list))
    
    return destinations_tour


def display_destinations_with_tour(destintions):
    """
    Display destinations"""

    print()

    format_str = "| {: <23} | {: <66} |"

    print('-'*96)
    display_formatted_row(["Destination", "Tour"], green(format_str))
    print('-'*96)

    for d, t in destintions:
        display_formatted_row((d, ",".join(t)), format_str)
    print('-'*96)


def get_datetime(dt):
    """
    Convert date to datetime since tour date in the source data might be date or datetime
    Use datetime to compare tour date"""

    if type(dt) == date:
        return datetime(dt.year, dt.month, dt.day)
    else:
        return dt


def get_customers_dict(customers):
    """
    Convert customer list to dictionary, using customer id as the key.
    The purpose is to find customer by customer id quickly"""

    return {c[0]: [c[0], c[1], c[2], c[3], c[4]] for c in customers}


def print_red(s):
    print('\033[91m{}\033[0m'.format(s))


def print_green(s):
    print('\033[92m{}\033[0m'.format(s))


def print_blue(s):
    print('\033[94m{}\033[0m'.format(s))


def print_yellow(s):
    print('\033[93m{}\033[0m'.format(s))


def print_magenta(s):
    print('\033[95m{}\033[0m'.format(s))


def print_cyan(s):
    print('\033[96m{}\033[0m'.format(s))



# ----------------------- End of Internal functions -----------------------


def list_all_customers():
    """
    Lists customer details.
    This is an example of how to produce basic output."""

    print()
    # Move display code into a function so that it could be reused by other functions
    display_customer_list(customers)

    input("\nPress Enter to continue.")


def list_customers_by_tourgroup():
    """
    Lists Customer details (including birth date), grouped by tour then tour group."""

    # Get tour groups
    tour_groups = get_tour_groups()
    
    # print(tour_groups)
    
    # Display tour groups
    display_customer_by_tour_group(tour_groups)

    input("\nPress Enter to continue.")


def list_tour_details():
    """
    List the tours and all locations visited."""
    
    # Sort tours
    tours_sorted = sorted(tours.items(), key=lambda x: x[0])
    
    # Display sorted tours
    display_tour_details(tours_sorted)
    
    input("\nPress Enter to continue.")


def add_customer_to_tourgroup():
    """
    Choose a customer, then a tour & group, add customers to tour groups only if they meet the minimum age requirement """

    # display customer list
    display_customer_list(customers)
    
    # Input and validate customer id
    while True:
        customer_id = input("Please input a customer id (input c to cancel): ")

        if customer_id.lower() == 'c':
            input("\nPress Enter to continue.")
            return
        
        try:
            customer_id = int(customer_id)
            if not is_customer_id_existed(customer_id):
                print("Customer ID not existing, please try again (input c to quit).\n")
            else:
                break
        except ValueError:
            print("Please input an integer.\n")
    
    # Get tour groups
    tour_groups = get_tour_groups()

    # Display tour groups
    display_tour_groups(tour_groups)

    # Input and validate tour group
    while True:
        tour_group_no = input("Plese input the tour group number (input c to cancel): ")

        if tour_group_no.lower() == "c":
            input("\nPress Enter to continue.")
            return

        try:
            tour_group_no = int(tour_group_no)
            if not is_tour_group_existed(tour_group_no, tour_groups):
                print("Tour group number is not correct. Please try again (input c to cancel).\n")

            elif is_customer_already_in_tour_group(customer_id, tour_group_no, tour_groups):
                print("Customer already in this tour group. Please try again (input c to cancel).\n")

            elif not is_customer_age_valid(customer_id, tour_group_no, tour_groups):
                print("Customer is younger than the age restricted. Please try again (input c to cancel).\n")

            else:
                break

        except ValueError:
            print("Please input an integer.\n")

    # Internal function to add cutomer into tour group
    _add_customer_to_tourgroup(customer_id, tour_group_no, tour_groups)

    print('The customer has been added to the tour group successfully.\n')

    input("\nPress Enter to continue.")


def add_new_customer():
    """
    Add a new customer to the customer list."""

    # User can add new customer repeatedly
    while True:
        first_name = get_input("Please input first name (input :q to quit):\n")
        if first_name == ":q":
            return
        
        last_name = get_input("Please input last name (input :q to quit):\n")
        if last_name == ":q":
            return

        birth_date = get_input("Please input birth date with format 'dd/MM/YYYY' (input :q to quit):\n", validation='date')
        if birth_date == ":q":
            return

        email = get_input("Please input email address (input :q to quit):\n", validation='email')
        if email == ":q":
            return

        _add_new_customer([first_name, last_name, birth_date, email])

        print("Cutomer has successfully added. Continue to add another customer.\n")


def get_input(prompt, validation=None):
    """
    Receiver user input and validate date or email.
    This function is used for add new customer (First Name, Last Name, Birth Date, Email)."""

    while True:
        input_string = input(prompt).strip()

        if input_string.lower() == ":q":
            return ":q"

        if input_string == "":
            print("Can not be empty.")
            continue

        elif validation == 'date':
            validation_result = is_valid_date(input_string)
            if type(validation_result) != date:
                print(validation_result)
                continue

            input_string = validation_result

        elif validation == 'email':
            if not is_email(input_string):
                print("Incorrect email format")
                continue
        break
    return input_string


def _add_new_customer(new_customer):
    """
    Add new customer into customers"""

    customers.append([unique_id(), *new_customer])


def list_all_destinations():
    """
    List all destinations that ATL Visit and the tours that visit them"""

    destinations = get_all_destinations_with_tour()
    display_destinations_with_tour(destinations)

    input("\nPress Enter to continue.")


def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("\033[94m==== WELCOME TO AOTEAROA TOURS MANAGEMENT SYSTEM ====\033[00m")
    print(" 1 - List Customers")
    print(" 2 - List Customers By Tour Groups")
    print(" 3 - List Tours and their details")
    print(" 4 - List all Tours that visit Destinations")
    print(" 5 - Add Existing Customer to Tour Group")
    print(" 6 - Add New Customer")
    print(" X - eXit (stops the program)")



# ------------ This is the main program ------------------------

# Don't change the menu numbering or function names in this menu.
# Although you can add arguments to the function calls, if you wish.
# Repeat this loop until the user enters an "X" or "x"
response = ""
while response != "X":
    # Display menu for the first time, and ask for response
    disp_menu()
    # Convert input to upper case to accept both 'x' and 'X'
    response = input("Please enter menu choice: ").upper()
    if response == "1":
        list_all_customers()
    elif response == "2":
        list_customers_by_tourgroup()
    elif response == "3":
        list_tour_details()
    elif response == "4":
        list_all_destinations()
    elif response == "5":
        add_customer_to_tourgroup()
    elif response == "6":
        add_new_customer()
    elif response != "X":
        print("\n*** Invalid response, please try again (enter 1-6 or X)")

    print("")

print("\n=== Thank you for using the AOTEAROA TOURS MANAGEMENT SYSTEM! ===\n")




