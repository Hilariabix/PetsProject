from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from pets import db
from pets.models.employee import Employee
from pets.models.manager import Manager
from pets.models.person import Role

employees = Blueprint("employees", __name__)


@employees.route("/employees")
@login_required
def get_all_employees():
    try:
        is_employed = request.args.get('is_employed')
        if is_employed is not None:
            results = Employee.query.filter_by(is_employed=is_employed.lower() == "true")
        else:
            results = Employee.query.all()
        if not results:
            raise ValueError("No Employees")
    except Exception as ex:
        results = None
        flash("Error: {}".format(ex), "error")
    return render_template("employees/employees.html", employees_list=results)


@employees.route("/employees/<employee_id>", methods=["GET"])
@login_required
def get_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)
        if not employee:
            raise ValueError("Employee ID {} was not found".format(employee_id))
    except Exception as ex:
        flash("Error: {}".format(ex), "error")
        return redirect(url_for("employees.get_all_employees"))

    return render_template("employees/view.html", method="POST", action="/employees/{}".format(employee_id), employee=employee)


@employees.route("/employees/<employee_id>", methods=["POST"])
@login_required
def update_employee(employee_id):
    try:
        exist_employee = Employee.query.get(employee_id)
        if not exist_employee:
            raise ValueError("Employee ID {} was not found".format(employee_id))

        updated_role = Role(request.form["role"])
        if exist_employee.role != updated_role:
            db.session.delete(exist_employee)
            db.session.commit()
            if updated_role == Role.Manager:
                employee = Manager(request.form)
            else:
                employee = Employee(request.form)
            db.session.add(employee)
        else:
            exist_employee.update(request.form)

        db.session.commit()
        flash("{} was updated successfully".format(exist_employee.name), "info")
    except Exception as ex:
        flash("Error: {}".format(ex), "error")
        return redirect(url_for("employees.get_all_employees"))

    return redirect(url_for("employees.get_all_employees"))


@employees.route("/employees/add", methods=["GET"])
@login_required
def add_employee_view():
    return render_template("employees/view.html", method="POST", action="/employees/add", employee=None)


@employees.route("/employees/add", methods=["POST"])
@login_required
def add_employee():
    # try:
    role = Role(request.form["role"])
    if role == Role.Manager:
        employee = Manager(request.form)
    else:
        employee = Employee(request.form)

    db.session.add(employee)
    db.session.commit()
    flash("{} was added successfully".format(employee.name), "info")
    # except Exception as ex:
    #     flash("Error: Failed to add an employee, {}".format(ex), "error")

    return redirect(url_for("employees.get_all_employees"))


@employees.route("/employees/delete/<employee_id>", methods=["GET"])
@login_required
def delete_employee(employee_id):
    try:
        exist_employee = Employee.query.get(employee_id)
        if not exist_employee:
            raise ValueError("Employee ID {} was not found".format(employee_id))

        db.session.delete(exist_employee)
        db.session.commit()
        flash("{} was deleted successfully".format(exist_employee.name), "info")
    except Exception as ex:
        flash("Error: {}".format(ex), "error")

    return redirect(url_for("employees.get_all_employees"))
