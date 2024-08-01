from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_gottk'
app.config['MYSQL_PASSWORD'] = 'xxxx' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_gottk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes 

@app.route("/")
def home():
    return render_template("main.j2")


# route for people page
@app.route("/rides", methods=["POST", "GET"])
def rides():
    # Separate out the request methods, in this case this is for a POST
    # insert a person into the bsg_people entity
    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Ride"):
            # grab user form inputs
            ride_name = request.form["ride_name"]
            park_id = request.form["park_id"]
            height_restriction = request.form["height_restriction"]
            lightning_lane = request.form["lightning_lane"]
            ride_length = request.form["ride_length"]

            # account for null height_restriction AND lightning_lane AND ride_length
            if height_restriction == "" and lightning_lane == "" and ride_length == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Rides (ride_name, park_id) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id))
                mysql.connection.commit()

            # account for null height_restriction
            elif height_restriction == "":
                query = "INSERT INTO Rides (ride_name, park_id, lightning_lane, ride_length) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane, ride_length))
                mysql.connection.commit()

            # account for null lightning_lane
            elif lightning_lane == "":
                query = "INSERT INTO Rides (ride_name, park_id, height_restriction, ride_length) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction, ride_length))
                mysql.connection.commit()

            # account for null ride_length
            elif ride_length == "":
                query = "INSERT INTO Rides (ride_name, park_id, height_restriction, lightning_lane) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction, lightning_lane))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Rides (ride_name, park_id, height_restriction, lightning_lane, ride_length) VALUES (%s, %s,%s,%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction, lightning_lane, ride_length))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/rides")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Rides.id, ride_name, height_restriction, lightning_lane, ride_length, Parks.park_name AS park FROM Rides LEFT JOIN Parks ON park_id = Parks.park_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT park_id, park_name FROM Parks"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("people.j2", data=data, homeworlds=homeworld_data)

# route for delete functionality, deleting a person from bsg_people,
# we want to pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/delete_people/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM bsg_people WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/people")


# route for edit functionality, updating the attributes of a person in bsg_people
# similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
@app.route("/edit_people/<int:id>", methods=["POST", "GET"])
def edit_people(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM bsg_people WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab planet id/name data for our dropdown
        query2 = "SELECT id, name FROM bsg_planets"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        homeworld_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("edit_people.j2", data=data, homeworlds=homeworld_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("Edit_Person"):
            # grab user form inputs
            id = request.form["personID"]
            fname = request.form["fname"]
            lname = request.form["lname"]
            homeworld = request.form["homeworld"]
            age = request.form["age"]

            # account for null age AND homeworld
            if (age == "" or age == "None") and homeworld == "0":
                # mySQL query to update the attributes of person with our passed id value
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, id))
                mysql.connection.commit()

            # account for null homeworld
            elif homeworld == "0":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = NULL, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, age, id))
                mysql.connection.commit()

            # account for null age
            elif age == "" or age == "None":
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = NULL WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE bsg_people SET bsg_people.fname = %s, bsg_people.lname = %s, bsg_people.homeworld = %s, bsg_people.age = %s WHERE bsg_people.id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, homeworld, age, id))
                mysql.connection.commit()

            # redirect back to people page after we execute the update query
            return redirect("/people")



# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8675, debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 9112))
#     app.run(port=port, debug=True)