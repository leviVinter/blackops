#!/usr/bin/env python3
"""
Black-Ops app
"""
import sys
sys.path.insert(0, "classes")

from flask import Flask, render_template, request, redirect, url_for
from flask import abort, session, flash
from controller import Controller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///db/blackops.sqlite")
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

controller = Controller(Session)

app = Flask(__name__)
app.secret_key = "BlackOpsSecretKey"

# Make it easier to debug
# app.debug = True
# app.config.update(PROPAGATE_EXCEPTIONS=True)

@app.route("/")
def main():
    """ Main route """
    return render_template("index.html",
                           controller=controller,
                           session=session)

@app.route("/staff", methods=["GET", "POST"])
def staff():
    """ Staff route """
    error = False
    if request.method == "POST":
        if not 'LoggedIn' in session:
            error = True
            flash('You must be logged in to add a new soldier')
        else:
            fname = request.form.get("inputFirstName")
            lname = request.form.get("inputLastName")
            soldier_type = request.form.get("select")
            if fname and lname and soldier_type:
                controller.add_soldier(fname, lname, soldier_type)
                flash('You added ' + fname + ' ' + lname + ' to the staff')
    return render_template("staff.html",
                           error=error,
                           controller=controller)

@app.route("/staff_member/<staff_id>", methods=["GET"])
def staff_member(staff_id):
    """ Staff member route """
    error = False
    soldier = controller.get_soldier(soldier_id=staff_id)
    if request.method == "GET":
        material_id = request.args.get("material")
        soldier_id = request.args.get("soldier")
        action = request.args.get("action")
        soldier_type = request.args.get("soldier_type")
        # Book or unbook material
        if material_id and soldier_id:
            if action == "book":
                controller.hand_out_material([material_id], soldier_id)
            elif action == "unbook":
                controller.hand_in_material([material_id], soldier_id)
        # Change soldier classification
        elif soldier_type and soldier_id:
            controller.change_soldier_type(soldier_id, soldier_type)
            flash(soldier.get_name() + ' was updated to ' \
                  + soldier_type.capitalize() + ' class')
            return redirect(url_for('staff'))
        # Remove soldier
        elif soldier_id and action == "remove":
            name = soldier.get_name()
            if 'LoggedIn' in session \
               and controller.remove_soldier(soldier_id):
                flash(name+ " was removed.")
                return redirect(url_for('staff'))
            else:
                error = True
                flash('You have to be logged in to remove a soldier.')
    return render_template("staff-member.html",
                           error=error,
                           controller=controller,
                           soldier=soldier)

@app.route("/material", methods=["GET", "POST"])
def material():
    """ Material route """
    error = False
    if request.method == "POST" and request.form["material"]:
        if not 'LoggedIn' in session:
            flash('You must be logged in to add new material')
            error = True
        else:
            name = request.form["inputName"]
            if not controller.material_name_exists(name):
                material_type = request.form["material"]
                code = request.form["inputCode"]
                attr = {}
                if request.form["material"] == "weapon":
                    attr["weapon_type"] = request.form["inputWeaponType"]
                    attr["ammo_type"] = request.form["inputAmmo"]
                elif request.form["material"] == "equipment":
                    attr["description"] = request.form["textarea"]
                controller.add_material(name, code, attr, material_type)
                flash('You added ' + name + ' to the storage')

    return render_template("material.html",
                           error=error,
                           controller=controller)

@app.route("/view_material/<material_id>/<quantity>", methods=["GET"])
def view_material(material_id, quantity):
    """ View material route """
    error = False
    a_material = controller.get_material_by_id(material_id)
    if request.method == "GET" and request.args.get("action") \
       and request.args.get("number"):
        if not 'LoggedIn' in session:
            error = True
            flash('You must be logged in to add or remove material')
        else:
            action = request.args.get("action")
            number = request.args.get("number")
            try:
                number = int(number)
            except ValueError:
                abort(404)
            counter = 0
            if not action or not number or not material:
                abort(404)
            if action == "add":
                name = a_material.get_name()
                code = a_material.get_code()
                material_type = a_material.get_type()
                attr_dict = {}
                if material_type == "weapon":
                    attr_dict["weapon_type"] = a_material.get_weapon_type()
                    attr_dict["ammo_type"] = a_material.get_ammo_type()
                elif material_type == "equipment":
                    attr_dict["description"] = a_material.get_description()

                while counter < number:
                    controller.add_material(name, code, attr_dict,
                                            material_type)
                    counter += 1
                return redirect(url_for('material'))
            elif action == "remove":
                name = a_material.get_name()
                controller.remove_material_by_name(name, number)
                return redirect(url_for('material'))
    return render_template("view-material.html",
                           error=error,
                           controller=controller,
                           material=a_material,
                           quantity=quantity)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login route """
    error = False
    if request.method == 'POST':
        wrong_username = request.form['inputUsername'] != 'admin'
        wrong_password = request.form['inputPassword'] != 'admin'
        if wrong_username or wrong_password:
            error = True
            flash('Wrong username or password')
        else:
            session['LoggedIn'] = True
            flash('You were successfully logged in')
            return redirect(url_for('main'))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    """ Logout route """
    session.pop('LoggedIn', None)
    return redirect(url_for('main'))

@app.teardown_request
def remove_session(exception=None):
    """ Remove session """
    Session.remove()
    if exception:
        print("An exception was found in remove_session")

if __name__ == "__main__":
    app.run()
