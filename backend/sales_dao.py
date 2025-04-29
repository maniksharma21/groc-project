from http.client import responses
from sql_connection import get_sql_connection

def show_sales(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM groc.sales"
    cursor.execute(query)

    response = []
    print(cursor)
    for (SaleID,OrderID,SaleDate,Total) in cursor:
        response.append([SaleID,OrderID,Total])
    return response

def show_salesdetails(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM groc.salesdetails"
    cursor.execute(query)

    response = []
    print(cursor)
    for (SaleDetailID,SaleID,ProductID,Quantity,UnitPrice,TotalPrice) in cursor:
        response.append([SaleDetailID,SaleID,ProductID,Quantity,UnitPrice,TotalPrice])
    return response

def show_orders(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM groc.orders"
    cursor.execute(query)

    response = []
    print(cursor)
    for (OrderID,CustomerID,OrderDate,TotalAmount,Status) in cursor:
        response.append([OrderID,CustomerID,OrderDate,TotalAmount,Status])
    return response



#from claude
from http.client import responses
def process_sale(connection, sale_data):
    """
    Process a sale by calling the ProcessSale stored procedure

    Args:
        connection: MySQL database connection
        sale_data: Dictionary containing sale information with keys:
            - customer_id: ID of the customer
            - product_id: ID of the product being sold
            - quantity: Quantity of the product
            - payment_method: Method of payment (Cash, Credit Card, Debit Card, UPI, Other)

    Returns:
        Dictionary with success status and message
    """
    try:
        cursor = connection.cursor()

        # Call the stored procedure
        cursor.callproc('ProcessSale', [
            sale_data['customer_id'],
            sale_data['product_id'],
            sale_data['quantity'],
            sale_data['payment_method']
        ])

        # Commit the transaction
        connection.commit()

        return {
            "success": True,
            "message": "Sale processed successfully"
        }

    except Exception as e:
        # Rollback in case of error
        connection.rollback()
        return {
            "success": False,
            "message": str(e)
        }


# Example usage of the function
if __name__ == '__main__':
    connection = get_sql_connection()
    print(connection)
    # Example sale data

    #sale = {
    #    'customer_id': 1,
    #    'product_id': 5,
    #    'quantity': 2,
     #   'payment_method': 'Credit Card'
    #}

    #result = process_sale(connection, sale)
    #print(result)




