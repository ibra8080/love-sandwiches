import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input frome the user
    """
    while True:
        print('Please enter sales data frome the last market.')
        print('Data should be six numbers, separated by commas.')
        print('Example: 30,23,43,54,33,12\n')

        data_str = input('Enter your data here: ')

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid')
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValuError if strings cannot be convertet into int,
    or they are not exactly 6 values. 
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, You provided {len(values)}"
            )
    except ValueError as e:
            print(f"Invalid data: {e}, please try again.\n")
            return False
    
    return True

"""
def update_sales_worksheet(data):
    
    Update sales worksheet, add new row with the list data provided.
    
    print("update sales sheet.. \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully. \n")


def update_surplus_worksheet(data):
    
    Updat surplus worksheet, add new row with the list data calculated.
    
    print("update surplus worksheet.. \n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully. \n")
"""

def update_worksheet(data, worksheet):
    """
    Receive a list of integers to be inserted into worksheet
    Updata the relevant worksheet with the data provided.
    """
    print(f"update {worksheet} worksheet.. \n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully. \n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus data for each item type.
    The surplus is defined as the sales figure suptracted frome the stock:
    - Positive surplus indicate waste.
    - Nigative surplus indicate extra made when stock was sold out.
    """
    print("calculate surplus data run \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row = [int(i) for i in stock_row]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Colect collumns of dat frome sales sheet. collecting
    the last 5 intries for each sandawich and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    collumns = []
    for ind in range(1, 7):
        collumn = sales.col_values(ind)
        collumns.append(collumn[-5:])
    
    return(collumns)

def main():
    """
    Run all programm functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love sandwiches data automation")
#main()
sales_collumns = get_last_5_entries_sales()