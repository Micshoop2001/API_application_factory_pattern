from .Schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Customers, db
from . import customers_bp
    

#POST '/' : Creates a new Customer
@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customers(name=customer['name'], 
                    phone=customer['phone'], 
                    email=customer['email'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201    
 
 
#GET '/': Retrieves all Customers
@customers_bp.route("/", methods=['GET'])
def get_customers():
    query = select(Customers)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers)


#PUT '/<int:id>': Updates a specific Customer based on the id passed in through the url.
@customers_bp.route('/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customers, id)

    if not customer:
        return jsonify({"message": "Invalid customer id"}), 400
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer.name = customer_data['name']
    customer.phone = customer_data['phone']
    customer.email = customer_data['email']

    db.session.commit()
    return customer_schema.jsonify(customer), 200

#DELETE '/<int:id': Deletes a specific customer based on the id passed in through the url.
@customers_bp.route('/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customers, id)
    if not customer:
        return jsonify({"message": "Invalid customer id"}), 400 
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"successfully deleted customer {id}"}), 200