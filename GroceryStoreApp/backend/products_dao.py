# data access object
import mysql.connector
def get_all_products():
    cnx = mysql.connector.connect(user='root',password='root',
                                host='127.0.0.1',
                                database='grocery')
    cursor = cnx.cursor()
    query = ('SELECT p.product_id,u.uom_name,p.name,p.price_per_unit FROM products p left join uom u on p.uom_id=u.uom_id')
    cursor.execute(query)

    response = []

    for(product_id,uom_id,name,price_per_unit) in cursor:
        response.append({'product_id': product_id,
                        'name': name,
                        'uom': uom_id,
                        'price_per_unit': price_per_unit})
    cnx.close()
    return response
# ---------------------------------------------------
def get_all_orders():
    cnx = mysql.connector.connect(user='root',password='root',
                                host='127.0.0.1',
                                database='grocery')
    cursor = cnx.cursor()
    query = ('SELECT * FROM grocery.orders')
    cursor.execute(query)

    response = []

    for(order_id,customer_name,total,date) in cursor:
        response.append({'order_id': order_id,
                        'customer_name': customer_name,
                        'total': total,
                        'date': date})
    cnx.close()
    return response

def delete_order(order_id):
    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='grocery'
    )
    cursor = cnx.cursor()
    
    cursor.execute("DELETE FROM order_details WHERE order_id = %s", (order_id,))


    cursor.execute("DELETE FROM orders WHERE order_id =" + str(order_id))
    

    
    cnx.commit()
    cnx.close()


def insert_order(Cname, total,date):
    
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='grocery'
        )
        cursor = cnx.cursor()

        query = "INSERT INTO `grocery`.`orders` (`customer_name`, `total`, `date`) VALUES (%s, %s,%s)"
        val = (Cname, total,date)
        cursor.execute(query, val)

        cnx.commit()

        print(cursor.rowcount, "record inserted.")
    except Exception as e:
        print("Error: ",e)
    finally:
        cursor.close()
        cnx.close()

# ------------------------------------------------------


def openOrderDetail(order_id):
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='grocery'
        )
        cursor = cnx.cursor()
        query = """SELECT o.customer_name, p.name, od.quantity, od.total_price
            FROM grocery.orders o
            JOIN grocery.order_details od ON o.order_id = od.order_id
            JOIN products p ON p.product_id = od.product_id
            WHERE o.order_id = %s"""
        val = (order_id,)
        cursor.execute(query, val)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print("Error: ",e)
    finally:
        cursor.close()
        cnx.close()






def insert_product(name, uom_id,price_per_unit):
    
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='grocery'
        )
        cursor = cnx.cursor()

        query = "INSERT INTO products (name, uom_id,price_per_unit) VALUES (%s, %s,%s)"
        val = (name, uom_id,price_per_unit)
        cursor.execute(query, val)

        cnx.commit()

        
    except Exception as e:
        print("Error: ",e)
    finally:
        cursor.close()
        cnx.close()




def get_all_uoms():
    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='grocery'
    )
    cursor = cnx.cursor()
    cursor.execute("SELECT uom_id, uom_name FROM uom")
    uoms = cursor.fetchall()
    cursor.close()
    cnx.close()
    return uoms




def insert_orderDetail(order_id,prodID, quantity, totalPrice):
    
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='grocery'
        )
        cursor = cnx.cursor()

        query = "INSERT INTO `grocery`.`order_details` (`order_id`, `product_id`, `quantity`, `total_price`) VALUES (%s, %s,%s,%s)"
        val = (order_id,prodID, quantity, totalPrice)
        cursor.execute(query, val)

        cnx.commit()

        
    except Exception as e:
        print("Error: ",e)
    finally:
        cursor.close()
        cnx.close()

def changeOrderTotal(order_id):
    try:
        cnx = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='grocery'
        )
        cursor = cnx.cursor()
        queryForTotal="SELECT SUM(total_price) FROM order_details WHERE order_id = (%s)"
        queryToChangeTotal = "UPDATE `grocery`.`orders` SET `total` = %s WHERE `order_id` = (%s)"
        
        cursor.execute(queryForTotal,(order_id,))
        orderTotal = cursor.fetchone()[0] or 0
        cursor.execute(queryToChangeTotal,(orderTotal,order_id))

        cnx.commit()

        
    except Exception as e:
        cnx.rollback()
        print("Error: ",e)
    finally:
        cursor.close()
        cnx.close()


# def changeOrderTotalOnProdDel(product_id):
#     cnx = mysql.connector.connect(
#             user='root',
#             password='root',
#             host='127.0.0.1',
#             database='grocery'
#         )
#     cursor = cnx.cursor()
#     query="SELECT order_id FROM grocery.order_details JOIN grocery.products ON order_details.product_id=products.product_id WHERE products.product_id=(%s)"
#     cursor.execute(query,product_id)
#     affected_orders = [row[0] for row in cursor.fetchall()]


def delete_product(product_id):
    cnx = mysql.connector.connect(
        user='root',
        password='root',
        host='127.0.0.1',
        database='grocery'
    )
    cursor = cnx.cursor()
    cursor.execute("SELECT DISTINCT order_id FROM order_details WHERE product_id = %s", (product_id,))
    affected_orders = [row[0] for row in cursor.fetchall()]
    cursor.execute("DELETE FROM order_details WHERE product_id=" + str(product_id))
    
    cursor.execute("DELETE FROM products WHERE product_id=" + str(product_id))
    
    cnx.commit()
    cnx.close()

    for order_id in affected_orders:
        changeOrderTotal(order_id)

if __name__=='__main__':
    # print(insert_new_product({
    #     'product_name': 'mrkva',
    #     'uom_id':'1',
    #     'price_per_unit':'10'


    # }))
    print(delete_product(15))

