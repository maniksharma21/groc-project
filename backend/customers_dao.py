from http.client import responses
from sql_connection import get_sql_connection

def get_customers(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM groc.customers"

    cursor.execute(query)


    response = []
    print(cursor)
    for (CustomerID,Name,Contact,Address) in cursor:
        response.append([CustomerID,Name,Contact,Address])


    return response


def insert_customer(connection, customer):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO customers (CustomerID, Name, Contact, Address) VALUES (%s, %s, %s, %s)"
        data = (customer['CustomerID'], customer['Name'], customer['Contact'], customer['Address'])

        cursor.execute(query, data)
        connection.commit()

        return {"message": "Customer inserted successfully", "CustomerID": customer['CustomerID']}  # Consistent JSON response

    except Exception as e:
        connection.rollback()  # Rollback if an error occurs
        print(f"Error inserting customer: {e}")
        return {"error": str(e)}  # Return error message

    finally:
        cursor.close()  # Ensure cursor is closed no matter what


def delete_customer(connection, customer):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM customers WHERE CustomerID = %s"
        cursor.execute(query, (customer['CustomerID'],))  # Parameterized query prevents SQL injection
        connection.commit()

        return {"message": "Customer deleted successfully"}

    except Exception as e:
        connection.rollback()  # Rollback if an error occurs
        print(f"Error deleting customer: {e}")
        return {"error": str(e)}  # Return error message

    finally:
        cursor.close()  # Ensure cursor is closed no matter what



if __name__ == '__main__':
    connection = get_sql_connection()
    print(connection)


