from http.client import responses
from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = "SELECT * FROM groc.inventory"

    cursor.execute(query)


    response = []
    print(cursor)
    for (ProductID,ProductName,SupplierID,Quantity,Price) in cursor:
        response.append([ProductID,ProductName,SupplierID,Quantity,Price])


    return response

def insert_product(connection,product):
    cursor = connection.cursor()
    query=("INSERT INTO inventory"
           "(ProductName,SupplierID,Quantity,Price)"
           "VALUES (%s,%s,%s,%s)")

    data =(product['ProductName'],product['SupplierID'],product['Quantity'],product['Price'])
    cursor.execute(query,data)
    connection.commit()
    return cursor.lastrowid


def delete_product(connection,product):
    cursor = connection.cursor()
    query=("DELETE FROM inventory where ProductID=" + str(product))
    cursor.execute(query)
    connection.commit()






if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_products(connection))






# print(insert_product(connection,{
#        'ProductName':'carrot',
#        'SupplierID':'2',
#        'Quantity':'50',
#        'Price':'50'
#
#
#     }))

