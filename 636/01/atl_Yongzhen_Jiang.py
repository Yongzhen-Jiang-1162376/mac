# ============== AOTEAROA TOURISM MANAGEMENT SYSTEM ==============
# Student Name: Yongzhen Jiang
# Student ID :  1162376
# ================================================================
 
from datetime import datetime, date, timedelta     # datetime module is required for working with dates
import re                                          # used to check against email format

# Make the variables and function in atl_data.py available in this code (without needing 'atl_data.' prefix)
from atl_data import customers, tours, unique_id, display_formatted_row   


def list_all_customers():
    """
    Lists customer details.
    This is an example of how to produce basic output."""
    
    display_all_customer()

    input("\nPress Enter to continue.")


def list_customers_by_tourgroup():
    """
    Lists Customer details (including birth date), grouped by tour then tour group."""

    tour_groups = get_tour_groups()
    print_customer_by_tour_group(tour_groups)

    input("\nPress Enter to continue.")

def list_tour_details():
    """
    List the tours and all locations visited."""
    
    tours_sorted = sorted(tours.items(), key=lambda x: x[0])
    print_tour_details(tours_sorted)
    
    input("\nPress Enter to continue.")

def add_customer_to_tourgroup():
    """
    Choose a customer, then a tour & group, add customers to tour groups only if they meet the minimum age requirement """

    # display customer list
    display_all_customer()
    
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
    
    tour_groups = get_tour_groups()

    # display tour group list
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
    
    _add_customer_to_tourgroup(customer_id, tour_group_no, tour_groups)

    print('The customer has been added to the tour group successfully.\n')

    input("\nPress Enter to continue.")


def add_new_customer():
    """
    Add a new customer to the customer list."""

    print('Add new customers now................')

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

        print(first_name, last_name, birth_date, email)

        _add_new_customer([first_name, last_name, birth_date, email])

        print("Cutomer has successfully added. Continue to add another customer.\n")
        # break


def get_input(prompt, validation=None):
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
                continue
        break
    return input_string


def _add_new_customer(new_customer):
    customers.append([unique_id(), *new_customer])

def list_all_destinations():
    """
    List all destinations that ATL Visit and the tours that visit them
    """
    destinations = get_all_destinations()
    print_destinations(destinations)

    input("\nPress Enter to continue.")

def disp_menu():
    """
    Displays the menu and current date.  No parameters required.
    """
    print("==== WELCOME TO AOTEAROA TOURS MANAGEMENT SYSTEM ===")
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





# ------------ Internal functions below ------------------------

def display_all_customer():
    print('-'*96)
    format_str = "| {: <5} | {: <15} | {: <15} | {: <15} | {: <30} |"            # Use the same format_str for column headers and rows to ensure consistent spacing. 
    display_formatted_row(["ID","First Name","Family Name","Birth Date","E-Mail"],format_str)     # Use the display_formatted_row() function to display the column headers with consistent spacing
    print('-'*96)
    for customer in customers:
        id = customer[0]
        fname = customer[1]
        famname = customer[2]
        birthdate = customer[3].strftime("%d %b %Y")
        email = customer[4]

        display_formatted_row([id,fname,famname,birthdate,email],format_str)     # Use the display_formatted_row() function to display each row with consistent spacing


def display_tour_groups(tour_groups):

    print()
    print("-"*63)
    format_str = "| {: <5} | {: <33} | {: <15} |"
    display_formatted_row(['No', 'Tour Group', 'Tour Date'], format_str)
    print("-"*63)

    for index, tg in enumerate(tour_groups):
        display_formatted_row([index + 1, tg[0][0], get_date(tg[0][1]).strftime("%d %b %Y")], format_str)
    
    # print(tour_groups[4])


def is_email(email):
    email_patter = r'^\S+@\S+\.\S+$'
    return re.match(email_patter, email)


def is_valid_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y')

        if birth_date.date() > date.today():
            return 'Later than today'
        elif birth_date.date() < yearsago(110, date.today()):
            return 'Earlier than 110 years ago'
        else:
            return birth_date.date()
    except ValueError:
        return 'ValueError'


def yearsago(years, current_date=None):
    if current_date is None:
        current_date = datetime.today().date()
    
    try:
        return current_date.replace(year=current_date.year - years)
    except ValueError:
        # Leap year and is 29 Feb
        return current_date.replace(year=current_date.year - 100, month=2, day=28)


def is_customer_id_existed(id):
    ids = [c[0] for c in customers]
    return id in ids


def is_tour_group_existed(tour_group_no, tour_groups):
    return tour_group_no > 0 and tour_group_no <= len(tour_groups)


def is_customer_already_in_tour_group(customer_id, tour_group_no, tour_groups):
    return customer_id in tour_groups[tour_group_no - 1][1][1]


def is_customer_age_valid(customer_id, tour_group_no, tour_groups):
    date_of_birth = [c[3] for c in customers if c[0] == customer_id][0]

    print("DOB: ", date_of_birth)

    age_restricted = tour_groups[tour_group_no - 1][1][0]

    return get_customer_age(date_of_birth) >= age_restricted


def get_customer_age(birthday):
    today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def _add_customer_to_tourgroup(customer_id, tour_group_no, tour_groups):
    group_date = tour_groups[tour_group_no - 1][0][1]
    new_group_member = tour_groups[tour_group_no - 1][1][1] + [customer_id]

    groups = tours[tour_groups[tour_group_no - 1][0][0]]["groups"]

    groups.update({
        group_date: new_group_member
    })

def get_tour_groups():
    tour_groups = {}
    for tour in tours.items():
        for group in tour[1]['groups'].items():
            tour_groups.update({(tour[0], group[0]): (tour[1]["age_restriction"], group[1])})
    
    tour_groups = sorted(tour_groups.items(), key=lambda x: get_date(x[0][1]))

    tour_groups = sorted(tour_groups, key=lambda x: x[0][0])
    
    return tour_groups


def print_customer_by_tour_group(tour_groups):
    customers_dict = get_customers_dict(customers)

    for tg in tour_groups:
        print(tg[0][0], tg[0][1])
        if len(tg[1]) == 0:
            print('None customer.')
        else:
            for c in tg[1]:
                print(customers_dict[c])
        print()


def print_tour_details(tours):
    for tour in tours:
        print(tour[0])
        print(', '.join(tour[1]['itinerary']))

def get_all_destinations():
    destinations = set()

    for tour in tours.items():
        destinations |= set(tour[1]['itinerary'])

    destinations = sorted(destinations)
    # print(destinations)

    destinations_tour = []
    for d in destinations:
        tour_list = []
        for tour in tours.items():
            if d in tour[1]['itinerary']:
                tour_list.append(tour[0])
        tour_list = sorted(tour_list)
        destinations_tour.append((d, tour_list))
    
    return destinations_tour


def print_destinations(destintions):
    for d, t in destintions:
        print(d, t)


def get_date(dt):
    if type(dt) == datetime:
        return dt.date()
    else:
        return dt

def get_customers_dict(customers):
    """
    Convert customer list to dictionary, customer id as the key
    This is to quick find customer by customer id
    """
    return {c[0]: (c[1], c[2], c[3], c[4]) for c in customers}