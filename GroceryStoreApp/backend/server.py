from flask import Flask, request, jsonify, render_template,redirect
import products_dao


app = Flask(__name__)


@app.route('/')
def home():
    uoms = products_dao.get_all_uoms()
    products = products_dao.get_all_products()
    return render_template('index.html',uoms=uoms, products=products)




@app.route('/getProducts', methods=['GET'])
def getProducts():
    products = products_dao.get_all_products()

    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getOrders', methods=['GET'])
def getOrders():
    orders = products_dao.get_all_orders()

    response = jsonify(orders)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/deleteOrder/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        products_dao.delete_order(order_id)
        return jsonify({'message': f'Product {order_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        products_dao.delete_product(product_id)
        return jsonify({'message': f'Product {product_id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/addProduct', methods=['POST'])
def add_product():
    # Dohvati podatke iz forme
    name = request.form.get('name')
    uom_id = request.form.get('uom_id')
    price = request.form.get('price_per_unit')
    # print(f"Name={name}, UOM={uom_id}, Price={price}")

    products_dao.insert_product(name, uom_id, price)


    return redirect('/')


@app.route('/addOrder', methods=['POST'])
def add_order():
    # Dohvati podatke iz forme
    Cname = request.form.get('Cname')
    total = 0
    date = request.form.get('date')
    # print(f"Name={Cname}, UOM={total}, Price={date}")

    products_dao.insert_order(Cname, total, date)


    return redirect('/')

@app.route('/addOrderDetail', methods=['POST'])
def add_orderDetail():
    # Dohvati podatke iz forme
    order_id = request.form.get('order_id')
    prodID = request.form.get('prodID')
    quantity = request.form.get('quantity')
    totalPrice = request.form.get('totalPrice')
    # print(f"Name={prodID}, UOM={quantity}, Price={totalPrice}")

    products_dao.insert_orderDetail(order_id,prodID, quantity, totalPrice)

    products_dao.changeOrderTotal(order_id)
    return redirect('/')

# @app.route('/changeOrderTotal/<int:order_id>', methods=['POST'])
# def changeOrderTotal(order_id):
#     try:
#         products_dao.changeOrderTotal(order_id)
#         return jsonify({'message': f'Product {order_id} updated'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


@app.route('/openOrderDetails/<int:order_id>', methods=['POST'])
def openOrderDetail(order_id):
    orderDetails=products_dao.openOrderDetail(order_id)
    response = jsonify(orderDetails)
    return response


if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store")
    app.run(port=5000)