from application.extensions import ma
from application.models import Service_tickets

class Service_ticketsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service_tickets
        include_fk = True

Service_ticket_schema =Service_ticketsSchema()
Service_tickets_schema = Service_ticketsSchema(many=True)