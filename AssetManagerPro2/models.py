from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)
    equipment = db.relationship('Equipment', backref='employee', lazy=True)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    oil_change_date = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(500), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)

    maintenance_records = db.relationship('Maintenance', backref='vehicle', lazy=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.String(50), nullable=True)

class JobMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(100), nullable=False)
    quantity_received = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.String(500), nullable=True)



class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    home = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    last_updated = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.String(500), nullable=True)


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)  # Tie maintenance to a specific vehicle
    service_date = db.Column(db.String(50), nullable=False)  # Date of service
    service_type = db.Column(db.String(100), nullable=False)  # Type of service (e.g., oil change, tire rotation)
    notes = db.Column(db.String(500), nullable=True)  # Additional notes about the service

    def __repr__(self):
        return f"<Maintenance {self.service_type} on {self.service_date}>"