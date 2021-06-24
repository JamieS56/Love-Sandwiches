import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Gete sales figures input from the user.
    """
    while True:
        print('Please enter sales data from the last market.')
        print('Data should be six numbers, seperated by commas')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here: ')
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('Data is valid!')
            break
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if stringd cannot be converted into int,
    or if there arent exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )

    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet_name):
    """
    Updates worsheet, add new row with the list data provided
    """
    print(f'Updating {worksheet_name} worksheet...\n')
    worksheet = SHEET.worksheet(worksheet_name)
    worksheet.append_row(data)
    print(f'{worksheet_name} worksheet updated succesfully.\n')


def calculate_surplas_data(sales_row):
    """
    Compare sales with stock and calculate the surplas for each item type.

    The surplas is defined as sales figures subtracted for the stock:
    - Positive surplas indicates waste
    - Negative surpla indicates extra stock made once we ran out.
    """
    print('Calculating surplas data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    collects collumns of data from sales worksheet, collecting 
    the last 5 entries for each sandwich and returns the data as a list of lists.
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        colums.append(column[-5:])
    pprint(columns)

    return columns

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplas_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    print(new_surplus_data)


print('Welcome to Love Sandwiches Data Automation')
#main()

get_last_5_entries_sales()