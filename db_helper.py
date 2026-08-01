import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "127.0.0.1", # As mysql is in parallels we provide IPv4 address of parallels as-host
        # host = "localhost", # this works if mysql workbench is installed in mac
        user = "root",
        passwd = "root@123",
        database = "expense_manager"
    )

    if connection.is_connected():
        print("Connection successful")
    else:
        print("Failed in connecting to a database")

    cursor = connection.cursor(dictionary = True)
    yield cursor

    if commit == True:
        connection.commit()

    cursor.close()
    connection.close()





def fetch_expense_for_date(expense_date):
    logger.info(f'Fetch_expenses_for_date called with {expense_date}')

    with get_db_cursor() as cursor:
        cursor.execute("select * from expenses where expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()

        return expenses


def insert_expense(expense_date, amount, category, notes):
    logger.info(f'insert_expenses called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}')

    with get_db_cursor(commit = True) as cursor:
        cursor.execute("insert into expenses (expense_date, amount, category, notes) values (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes))


def delete_expenses_for_date(expense_date):
    logger.info(f'delete_expenses_for_date called with {expense_date}')

    with get_db_cursor(commit = True) as cursor:
        cursor.execute("delete from expenses where expense_date = %s", (expense_date,))
        print(f'Deleted {expense_date}')


def fetch_expense_summary(start_date, end_date):
    logger.info(f'Fetch_expenses_summary called with start_date: {start_date} and end_date: {end_date}')

    with get_db_cursor() as cursor:
        cursor.execute('''Select category,sum(amount) as total 
                       from expenses 
                       where expense_date between %s and %s
                       group by category''',
                       (start_date, end_date))
        data = cursor.fetchall()
        return data


def fetch_all_records_by_month():
    with get_db_cursor() as cursor:
        cursor.execute("select DATE_FORMAT(expense_date,'%M') as expense_month, "
                       "DATE_FORMAT(expense_date,'%Y') as expense_year, sum(amount) as total "
                       "from expenses "
                       "group by DATE_FORMAT(expense_date,'%Y'),DATE_FORMAT(expense_date,'%M') "
                       "order by expense_month")
        expenses = cursor.fetchall()

        return expenses





if __name__ == "__main__":

    #delete_expenses_for_date("2020-08-20")
    #fetch_expense_for_date("2020-08-20")
    summary = fetch_all_records_by_month()
    for records in summary:
        print(records)