from .Schemas import Service_ticket_schema, Service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Service_tickets, Mechanics, db
from . import service_tickets_bp

@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = Service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = Service_tickets(
            service_date=service_ticket_data['service_date'], 
            VIN=service_ticket_data['VIN'], 
            service_desc=service_ticket_data['service_desc'],
            customers_id=service_ticket_data['customers_id'])
    
    db.session.add(new_service_ticket)
    db.session.commit()

    return Service_ticket_schema.jsonify(new_service_ticket), 201     

@service_tickets_bp.route("/<ticket_id>/assign-mechanic/<mechanic_id>", methods=['PUT'])
def update_mechanic(ticket_id, mechanic_id):
    service_ticket_data = db.session.get(Service_tickets, ticket_id)
    mechanic_data = db.session.get(Mechanics, mechanic_id)
    if not service_ticket_data:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic_data:
        return jsonify({"error": "Mechanic not found"}), 404
    if mechanic_data in service_ticket_data.mechanics:
        return jsonify({"message": "Mechanic already in list"}), 200
    service_ticket_data.mechanics.append(mechanic_data)
    db.session.commit()
    return Service_ticket_schema.jsonify(service_ticket_data), 200
    
@service_tickets_bp.route("/<ticket_id>/remove-mechanic/<mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket_data = db.session.get(Service_tickets, ticket_id)
    mechanic_data = db.session.get(Mechanics, mechanic_id)
    if not service_ticket_data:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic_data:
        return jsonify({"error": "Mechanic not found"}), 404
    if mechanic_data not in service_ticket_data.mechanics:
        return jsonify({"message": "Mechanic not in list"}), 404
    service_ticket_data.mechanics.remove(mechanic_data)
    db.session.commit()
    return Service_ticket_schema.jsonify(service_ticket_data), 200    
    
#GET '/': Retrieves all service tickets.
@service_tickets_bp.route("/", methods=['GET'])
def get_service_tickets():
    query = select(Service_tickets)
    service_tickets = db.session.execute(query).scalars().all()

    return Service_tickets_schema.jsonify(service_tickets)    
    


