from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Employee, Vehicle, Inventory, JobMaterial, Equipment, Maintenance

app = Flask(__name__)

# Configuration for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()
    vehicles = Vehicle.query.order_by(Vehicle.id.desc()).limit(5).all()
    equipment = Equipment.query.order_by(Equipment.id.desc()).limit(5).all()
    inventory = Inventory.query.order_by(Inventory.id.desc()).limit(5).all()
    job_materials = JobMaterial.query.order_by(JobMaterial.id.desc()).limit(5).all()
    maintenance = Maintenance.query.order_by(Maintenance.id.desc()).limit(5).all()

    return render_template('index.html', employees=employees, vehicles=vehicles, equipment=equipment,
                           inventory=inventory, job_materials=job_materials, maintenance=maintenance)


@app.route('/employees', methods=['GET'])
def employees():
    employees = Employee.query.all()

    return render_template('employees.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    # Handle adding a new employee
    if request.method == 'POST':
        name = request.form['name']
        new_employee = Employee(name=name)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('employees'))
    return render_template('employees.html', employees=employees)

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    employees = Employee.query.all()

    # Handle editing an existing employee
    if request.method == 'POST':
        employee.name = request.form['name']
        db.session.commit()
        return redirect(url_for('employees'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    # Handle deleting an employee

    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employees'))



@app.route('/maintenance', methods=['GET'])
def maintenance():
    maintenance_items = Maintenance.query.all()
    vehicles = Vehicle.query.all()
    for item in maintenance_items:
        print(f"ID: {item.id}")
    return render_template('maintenance.html', maintenance_items=maintenance_items, vehicles=vehicles)

@app.route('/maintenance/add', methods=['GET', 'POST'])
def add_maintenance():
    vehicles = Vehicle.query.all()

    if request.method == 'POST':
        vehicle_id = request.form.get('vehicleID')
        service_date = request.form['service_date']
        service_type = request.form['service_type']
        notes = request.form['notes']
        new_maintenance = Maintenance(vehicle_id=vehicle_id, service_date=service_date, service_type=service_type,
                                      notes=notes)
        db.session.add(new_maintenance)
        db.session.commit()
        return redirect(url_for('maintenance'))

    return render_template('add_maintenance.html', vehicles=vehicles)

@app.route('/maintenance/edit_maintenance', methods=['GET','POST'])
def edit_maintenance(id):
    return redirect(url_for('maintenance'))


@app.route('/vehicles', methods=['GET'])
def vehicles():
    vehicles = Vehicle.query.all()
    employees = Employee.query.all()

    return render_template('vehicles.html', vehicles=vehicles, employees=employees)


@app.route('/vehicles/add', methods=['GET', 'POST'])
def add_vehicle():
    employees = Employee.query.all()  # Get all employees for vehicle assignment
    print(f"Employees: {employees}")
    if request.method == 'POST':
        number = request.form['number']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        oil_change_date = request.form['oil_change_date']
        notes = request.form['notes']
        driver_id = request.form.get('driver')  # This is the employee assigned to the vehicle
        new_vehicle = Vehicle(number=number, make=make, model=model, year=year, oil_change_date=oil_change_date,
                              notes=notes, driver_id=driver_id)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))

    return render_template('add_vehicle.html', employees=employees)


@app.route('/edit_vehicle/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    employees = Employee.query.all()  # Get all employees for vehicle assignment

    # Handle the form submission for editing a vehicle
    if request.method == 'POST':
        vehicle.number = request.form['number']
        vehicle.make = request.form['make']
        vehicle.model = request.form['model']
        vehicle.year = request.form['year']
        vehicle.oil_change_date = request.form['oil_change_date']
        vehicle.notes = request.form['notes']
        vehicle.driver_id = request.form.get('driver')  # Employee assigned to the vehicle

        db.session.commit()
        return redirect(url_for('vehicles'))  # Redirect back to the vehicle list page

    return render_template('edit_vehicle.html', vehicle=vehicle, employees=employees)

@app.route('/delete_vehicle/<int:id>', methods=['POST'])
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('vehicles'))





# Routes for Equipment
@app.route('/equipment', methods=['GET'])
def equipment():
    equipment = Equipment.query.all()
    employees = Employee.query.all()
    for equip in equipment:
        print(f"ID: {equip.id}, Description: {equip.description}, Brand: {equip.brand}, Model: {equip.model}")
    return render_template('equipment.html', equipment=equipment, employees=employees)

@app.route('/equipment/add', methods=['GET', 'POST'])
def add_equipment():
    employees = Employee.query.all()  # Get all employees for equipment assignment
    if request.method == 'POST':
        description = request.form['description']
        brand = request.form['brand']
        model = request.form['model']
        location = request.form['location']
        home = request.form['home']
        employee_id = request.form.get('employee')  # Employee assigned to equipment
        new_equipment = Equipment(description=description, brand=brand, model=model, location=location, home=home, employee_id=employee_id)
        db.session.add(new_equipment)
        db.session.commit()
        return redirect(url_for('equipment'))
    return render_template('equipment_form.html', employees=employees)

@app.route('/edit_equipment/<int:id>', methods=['GET', 'POST'])
def edit_equipment(id):
    equipment = Equipment.query.get(id)
    employees = Employee.query.all()
    if request.method == 'POST':
        equipment.description = request.form['description']
        equipment.brand = request.form['brand']
        equipment.model = request.form['model']
        equipment.location = request.form['location']
        equipment.home = request.form['home']
        equipment.employee_id = request.form.get('employee')
        db.session.commit()
        return redirect(url_for('equipment'))
    return render_template('edit_equipment.html', equipment=equipment, employees=employees)

@app.route('/delete_equipment/<int:id>', methods=['POST'])
def delete_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    db.session.delete(equipment)
    db.session.commit()
    return redirect(url_for('equipment'))


@app.route('/inventory', methods=['GET'])
def inventory():
    inventory = Inventory.query.all()
    inventory_item = None
    for inv in inventory:
        print(f"ID: {inv.id}, Description: {inv.description}, Brand: {inv.brand}, Part: {inv.part_number}")
    return render_template('inventory.html', inventory=inventory )

@app.route('/inventory/add', methods=['GET', 'POST'])
def add_inventory():
#     Handle adding a new inventory item
    if request.method == 'POST':
        description = request.form['description']
        brand = request.form['brand']
        part_number = request.form['part_number']
        quantity = request.form['quantity']
        last_updated = request.form['last_updated']
        new_inventory = Inventory(description=description, brand=brand, part_number=part_number, quantity=quantity,
                                  last_updated=last_updated)
        db.session.add(new_inventory)
        db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('add_inventory.html', inventory=inventory)

@app.route('/edit_inventory/<int:id>', methods=['GET', 'POST'])
def edit_inventory(id):
    inventory = Inventory.query.get(id)
    if request.method == 'POST':
        inventory.description = request.form['description']
        inventory.brand = request.form['brand']
        inventory.part_number = request.form['part_number']
        inventory.quantity = request.form['quantity']
        inventory.last_updated = request.form['last_updated']

        db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('edit_inventory.html', inventory=inventory)


@app.route('/delete_inventory/<int:id>', methods=['POST'])
def delete_inventory(id):
    inventory = Inventory.query.get(id)
    db.session.delete(inventory)
    db.session.commit()
    return redirect(url_for('inventory'))










@app.route('/job_materials', methods=['GET'])
def job_materials():
    materials = JobMaterial.query.all()
    material_item = None
    for material in materials:
        print(f"ID: {material.id}, Description: {material.description}")
    return render_template('job_materials.html', materials=materials)

@app.route('/job_materials/add', methods=['GET', 'POST'])
def add_job_materials():
#     Handle adding a new inventory item
    materials = JobMaterial.query.all()

    if request.method == 'POST':
        job_number = request.form['job_number']
        description = request.form['description']
        brand = request.form['brand']
        part_number = request.form['part_number']
        quantity_received = request.form['quantity_received']
        notes = request.form['notes']
        new_material = JobMaterial(job_number=job_number, description=description, brand=brand, part_number=part_number,
                                   quantity_received=quantity_received, notes=notes)
        db.session.add(new_material)
        db.session.commit()
        return redirect(url_for('job_materials'))
    return render_template('add_job_materials.html', materials=materials)

@app.route('/edit_job_materials/<int:id>', methods=['GET', 'POST'])
def edit_job_materials(id):
    materials = JobMaterial.query.get(id)

    if request.method == 'POST':
        materials.job_number = request.form['job_number']
        materials.description = request.form['description']
        materials.brand = request.form['brand']
        materials.part_number = request.form['part_number']
        materials.quantity_received = request.form['quantity_received']
        materials.notes = request.form['notes']

        db.session.commit()
        return redirect(url_for('job_materials'))
    return render_template('edit_job_materials.html', materials=materials)


@app.route('/delete_job_materials/<int:id>', methods=['POST'])
def delete_job_materials(id):
    materials = JobMaterial.query.get(id)
    db.session.delete(materials)
    db.session.commit()
    return redirect(url_for('job_materials'))


if __name__ == "__main__":
    app.run(port=5001, debug=True)
