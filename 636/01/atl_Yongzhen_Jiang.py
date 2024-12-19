# ============== AOTEAROA TOURISM MANAGEMENT SYSTEM ==============
# Student Name: Yongzhen Jiang
# Student ID :  1162376
# ================================================================
 
from datetime import datetime, date, timedelta     # datetime module is required for working with dates
import re                                          # used to check against email format

# use namedtuple to receive data which is easy to access value with field name, rather than with integer index.
# but we could also use normal tuples here
from collections import namedtuple

# Make the variables and function in atl_data.py available in this code (without needing 'atl_data.' prefix)
from atl_data import customers, tours, unique_id, display_formatted_row   

# color code for in command line
# red = "\033[91m"
# green = "\033[92m"
# blue = "\033[94m"
# yellow = "\033[93m"
# magenta = "\033[95m"
# cyan = "\033[96m"
# reset = "\033[0m"

# some helper functions for printing with color
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

def print_warning(s):
    print("\033[91m{}\033[0m".format(s))

def print_success(s):
    print("\033[92m{}\033[0m".format(s))


# ----------------------- Start of Internal functions -----------------------
def display_customer_list(customers):
    """
    Display all customer"""

    print("-"*106)
    format_str = "| {: <5} | {: <15} | {: <15} | {: <15} | {: <40} |"            # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","First Name","Family Name","Birth Date","E-Mail"], green(format_str))     # Use the display_formatted_row() function to display the column headers with consistent spacing
    print("-"*106)

    if len(customers) == 0:
        # Display None Customer if no customer is within this group
        display_formatted_row(["None Customer"], "| {: <102} |")

    else:
        # sort customers by family name first and then by first name
        customers = sorted(customers, key=lambda c: c[1])
        customers = sorted(customers, key=lambda c: c[2])
        
        # display customer record
        for customer in customers:
            id = customer[0]
            first_name = customer[1]
            family_name = customer[2]
            birthdate = customer[3].strftime("%d %b %Y")
            email = customer[4]

            display_formatted_row([id,first_name,family_name,birthdate,email],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing

    print("-"*106)


def display_tour_groups(tour_group_list):
    """
    Display tour groups"""

    print()
    print("-"*96)
    format_str = "| {: <5} | {: <33} | {: <48} |"
    display_formatted_row(["No", "Tour Group", "Tour Date"], green(format_str))
    print("-"*96)

    for index, tg in enumerate(tour_group_list):
        display_formatted_row([index + 1, tg.title.name, tg.title.date.strftime("%d %b %Y")], format_str)
    
    print("-"*96)


def is_email(email):
    """
    Check email address format using regex"""

    email_patter = r"^\S+@\S+\.\S+$"
    return re.match(email_patter, email)


def is_valid_date(birth_date):
    """
    Check whether the birth date is a valid date"""

    try:
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y")

        if birth_date.date() > date.today():
            return "The date input is later than today"
        elif birth_date.date() < yearsago(110, date.today()):
            return "The date input is earlier than 110 years ago"
        else:
            return birth_date.date()
    except ValueError:
        return "Incorrect date format"


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


def is_tour_group_existed(index, tour_groups):
    """
    Check whether the tour group which user selects is within the available groups"""

    return index >= 0 and index < len(tour_groups)


def is_customer_already_in_tour_group(customer_id, index, tour_group_list):
    """
    Check whether the customer id is already existed in the tour group"""

    return customer_id in tour_group_list[index].member_list


def is_customer_age_valid(customer_id, index, tour_group_list):
    """
    Check whether the age of the customer is equal or larger than the restricted age"""

    date_of_birth = [c[3] for c in customers if c[0] == customer_id][0]
    age_restricted = tour_group_list[index].age_restriction

    return get_customer_age(date_of_birth) >= age_restricted


def get_customer_age(birthday):
    """
    Get the customer's age"""

    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def _add_customer_to_tourgroup(customer_id, index, tour_group_list):
    """
    Add the customer into the tour group selected"""

    group_date = tour_group_list[index].title.date
    new_member_list = tour_group_list[index].member_list + [customer_id]

    current_groups = tours[tour_group_list[index].title.name]["groups"]

    current_groups.update({
        group_date: new_member_list
    })


def get_tour_groups(name_descending=False, date_descending=False):
    """
    Re-structure tours data, grouped by a namedtuple named title = (tour_name, tour_date), and sorted by tour_name ascending, tour_date ascending.
    Because pair of (tour_name, tour_date) is unique.
    
    Finally the data structure will be list of following namedtuple:
    (title, age_restriction, member_list) -> (("name" "date"), age_restriction, member_list) -> (("UK", date(2023,7,10)), 0, [816,923,343])
    
    name_descending & date_descending controls order by direction (ascending or descending)"""

    tour_group_list = []
    tour_group = namedtuple("TourGroup", "title age_restriction member_list")
    tour_group_title = namedtuple("TourGroupTitle", "name date")


    # Transform tours data into a list of namedtuple ("title age_restriction memeber_list"), where title is another namedtuple ("name date")
    # Finally: ("("name date") age_restriction member_list") -> (("WestEurope", date(2023,8,15)), 0, [810,801])
    for tour in tours.items():
        for group in tour[1]["groups"].items():
            title = tour_group_title(tour[0], group[0])
            tour_group_list.append(tour_group(title, tour[1]["age_restriction"], group[1]))
    
    # sort by group date ascending (use reverse=True for descending)
    tour_group_list = sorted(tour_group_list, key=lambda x: x.title.date, reverse=date_descending)

    # sort by group name ascending (use reversed=True for descending)
    tour_group_list = sorted(tour_group_list, key=lambda x: x.title.name, reverse=name_descending)

    return tour_group_list


def display_customer_by_tour_group(tour_group_list):
    """
    Display customers grouped by tour group"""

    customers_dict = get_customers_dict(customers)

    # Calculate max length of tour name
    max_length = max([len(tour_group.title.name) for tour_group in tour_group_list])

    for tg in tour_group_list:
        print()

        # print("-"*106)
        print(" Tour  ", end="")
        display_tour_group_header(tg.title.name, tg.title.date, max_length)

        if len(tg.member_list) == 0:
            display_customer_list([])
        else:
            customer_list = []
            for c in tg.member_list:
                customer_list.append(customers_dict[c])
            display_customer_list(customer_list)


def display_tour_group_header(tour_name, tour_date, max_length):
    """
    Display tour group header"""

    format_str = "\033[94m{: <" + str(max_length) + "}\033[0m        Date  \033[96m{: <15}\033[0m  Month  \033[95m{: <40}\033[0m "
    display_formatted_row([tour_name, tour_date.strftime("%d %b %Y"), tour_date.strftime("%b %Y"), ], format_str)


def display_tour_details(tours):
    """
    Display tour details"""
    
    for tour in tours:
        # print(tour[0])
        print()
        print("-"*52)
        print("| Tour         |", end="")
        display_formatted_row([tour[0]], cyan(" {: <33} |"))
        print("-"*52)
        print("| Destinations |", end="")
        first_line_mark = True
        for itinerary in sorted(tour[1]["itinerary"]):
            if not first_line_mark:
                print("|              |", end="")
            display_formatted_row([itinerary], green(" {: <33} |"))
            first_line_mark = False
        print("-"*52)


def get_all_destinations_with_tour():
    """
    Get all destinations, each with a tour list whose itinerary contains this destination
    """

    destinations = set()

    # Add all destinations into a set (so there"s no duplicate destination)
    for tour in tours.items():
        destinations |= set(tour[1]["itinerary"])

    # Sort destinations by name ascending
    destinations = sorted(destinations)

    # Create a list of touple, each tuple is a pair of (destination, tour_list)
    destinations_tour = []
    for d in destinations:
        tour_list = []
        for tour in tours.items():
            if d in tour[1]["itinerary"]:
                tour_list.append(tour[0])
        tour_list = sorted(tour_list)
        destinations_tour.append((d, tour_list))
    
    return destinations_tour


def display_destinations_with_tour(destintions):
    """
    Display destinations"""

    print()

    format_str_header = "| {: <20} | {: <35} |"
    format_str = "| \033[96m{: <20}\033[0m | \033[92m{: <35}\033[0m |"

    print("-"*62)
    display_formatted_row(["Destination", "Tour"], format_str_header)
    print("-"*62)

    for destination, tour_list in destintions:
        first_line_mark = True
        for tour in tour_list:
            if first_line_mark:
                display_formatted_row([destination, tour], format_str)
                first_line_mark = False
            else:
                display_formatted_row(["", tour], format_str)
    
    print("-"*62)


def get_customers_dict(customers):
    """
    Convert customer list to dictionary, using customer id as the key.
    The purpose is to find customer by customer id quickly"""

    return {c[0]: [c[0], c[1], c[2], c[3], c[4]] for c in customers}


def get_user_input(prompt, validation=None):
    """
    Receive user input and validate date or email.
    This function is used for add new customer (First Name, Last Name, Birth Date, Email)."""

    while True:
        input_string = input(prompt).strip()

        if input_string.lower() == ":q":
            return ":q"

        if input_string == "":
            print_warning("Input can not be empty.")
            continue

        elif validation == "date":
            validation_result = is_valid_date(input_string)
            if type(validation_result) != date:
                print_warning(validation_result)
                continue

            input_string = validation_result

        elif validation == "email":
            if not is_email(input_string):
                print_warning("Incorrect email format")
                continue
        break
    return input_string


def _add_new_customer(new_customer):
    """
    Add new customer into customers"""

    customers.append([unique_id(), *new_customer])


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
    tour_group_list = get_tour_groups()
    
    # print(tour_group_list)
    
    # Display tour groups
    display_customer_by_tour_group(tour_group_list)

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
        customer_id = input("Please input a customer id (input :q to quit): ")

        if customer_id.lower() == ":q":
            input("\nPress Enter to continue.")
            return
        
        try:
            customer_id = int(customer_id)
            if not is_customer_id_existed(customer_id):
                print_warning("Customer ID not existing, please try again (input :q to quit).\n")
            else:
                break
        except ValueError:
            print_warning("Please input an integer.\n")
    
    # Get tour groups
    tour_group_list = get_tour_groups()

    # Display tour groups
    display_tour_groups(tour_group_list)

    # Input and validate tour group
    while True:
        index = input("Plese input the tour group number (input :q to quit): ")

        if index.lower() == ":q":
            input("\nPress Enter to continue.")
            return

        try:
            index = int(index) - 1
            if not is_tour_group_existed(index, tour_group_list):
                print_warning("Tour group number is not correct. Please try again (input :q to quit).\n")

            elif is_customer_already_in_tour_group(customer_id, index, tour_group_list):
                print_warning("Customer already in this tour group. Please try again (input :q to quit).\n")

            elif not is_customer_age_valid(customer_id, index, tour_group_list):
                print_warning("Customer is younger than the age restricted. Please try again (input :q to quit).\n")

            else:
                break

        except ValueError:
            print_warning("Please input an integer.\n")

    # Internal function to add cutomer into tour group
    _add_customer_to_tourgroup(customer_id, index, tour_group_list)
    
    print_success("The customer has been added to the tour group successfully.\n")

    input("\nPress Enter to continue.")


def add_new_customer():
    """
    Add a new customer to the customer list."""

    # User can add new customer repeatedly
    while True:
        first_name = get_user_input("Please input first name (input :q to quit):\n")
        if first_name == ":q":
            return
        
        last_name = get_user_input("Please input last name (input :q to quit):\n")
        if last_name == ":q":
            return

        birth_date = get_user_input("Please input birth date with format 'dd/MM/YYYY' (input :q to quit):\n", validation="date")
        if birth_date == ":q":
            return

        email = get_user_input("Please input email address (input :q to quit):\n", validation="email")
        if email == ":q":
            return

        _add_new_customer([first_name, last_name, birth_date, email])

        print_success("Cutomer has successfully added. Continue to add another customer.\n")


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

print("\n\033[94m=== Thank you for using the AOTEAROA TOURS MANAGEMENT SYSTEM! ===\033[0m\n")
