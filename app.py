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
            
            # account for null height_restriction and null lightning_lane
            elif height_restriction == "" and lightning_lane == "":
                query = "INSERT INTO Rides (ride_name, park_id, ride_length) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, ride_length))
                mysql.connection.commit()

            # account for null height_restriction and null ride_length
            elif height_restriction == "" and ride_length == "":
                query = "INSERT INTO Rides (ride_name, park_id, lightning_lane) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane))
                mysql.connection.commit()

            # account for null lightning_lane and null ride_length
            elif lightning_lane == "" and ride_length == "":
                query = "INSERT INTO Rides (ride_name, park_id, height_restriction) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction))
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

            # redirect back to rides page
            return redirect("/rides")

    # Grab Rides data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the rides in Rides
        query = "SELECT Rides.id, ride_name, height_restriction, lightning_lane, ride_length, Parks.park_name AS park FROM Rides LEFT JOIN Parks ON park_id = Parks.park_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT park_id, park_name FROM Parks;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_rides template
        return render_template("rides.j2", data=data, parks=parks_data)

# route for delete functionality, deleting a ride from Rides,
# we want to pass the 'id' value of that ride on button click (see HTML) via the route
@app.route("/delete_ride/<int:id>")
def delete_ride(id):
    # mySQL query to delete the ride with our passed id
    query = "DELETE FROM Rides WHERE id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/rides")


# route for edit functionality, updating the attributes of a ride in Rides
# similar to our delete route, we want to the pass the 'id' value of that ride on button click (see HTML) via the route
@app.route("/edit_ride/<int:id>", methods=["POST", "GET"])
def edit_ride(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT * FROM Rides WHERE id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT park_id, park_name FROM Parks"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_ride template
        return render_template("edit_rides.j2", data=data, parks=parks_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Ride' button
        if request.form.get("Edit_Ride"):
            # grab user form inputs
            ride_id = request.form["ride_id"]
            ride_name = request.form["ride_name"]
            height_restriction = request.form["height_restriction"]
            lightning_lane = request.form["lightning_lane"]
            park_id = request.form["park_id"]
            ride_length = request.form["ride_length"]

            # account for null height_restriction AND lightning_lane AND ride_length
            if height_restriction == "" and lightning_lane == "" and ride_length == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.height_restriction = NULL, Rides.lightning_lane = NULL, Rides.ride_length = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, ride_id))
                mysql.connection.commit()

            # account for null height_restriction AND lightning_lane
            elif height_restriction == "" and lightning_lane == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.ride_length = %s, Rides.height_restriction = NULL, Rides.lightning_lane = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, ride_length, ride_id))
                mysql.connection.commit()

            # account for null height_restriction AND ride_length
            elif height_restriction == "" and ride_length == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.lightning_lane = %s, Rides.height_restriction = NULL, Rides.ride_length = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane, ride_id))
                mysql.connection.commit()

            # account for null ride_length AND lightning_lane
            elif lightning_lane == "" and ride_length == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.height_restriction = %s, Rides.lightning_lane = NULL, Rides.ride_length = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction, ride_id))
                mysql.connection.commit()
            
            # account for null lightning_lane
            elif lightning_lane == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.height_restriction = %s, Rides.ride_length = %s, Rides.lightning_lane = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, height_restriction, ride_length, ride_id))
                mysql.connection.commit()

            # account for null height_restriction
            elif height_restriction == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.lightning_lane = %s, Rides.ride_length = %s, Rides.height_restriction = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane, ride_length, ride_id))
                mysql.connection.commit()

            # account for null ride_length
            elif ride_length == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.ride_name = %s, Rides.park_id = %s, Rides.lightning_lane = %s, Rides.height_restriction = %s, Rides.ride_length = NULL WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane, height_restriction, ride_id))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Rides SET Rides.ride_name= %s, Rides.park_id = %s, Rides.lightning_lane = %s, Rides.height_restriction = %s Rides.ride_length = %s WHERE Rides.ride_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (ride_name, park_id, lightning_lane, height_restriction, ride_length, ride_id))
                mysql.connection.commit()

            # redirect back to rides page after we execute the update query
            return redirect("/rides")



# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=8675, debug=True)
