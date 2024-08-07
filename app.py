from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_username'
app.config['MYSQL_PASSWORD'] = 'password' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_username'
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
        if request.form.get("insertRide"):
            # grab user form inputs
            rideName = request.form["rideName"]
            parkID = request.form["parkID"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            rideLength = request.form["rideLength"]

            # account for null heightRestriction AND lightningLane AND rideLength
            if heightRestriction == "" and lightningLane == "" and rideLength == "":
                # mySQL query to insert a new person into bsg_people with our form inputs
                query = "INSERT INTO Rides (rideName, parkID) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID))
                mysql.connection.commit()
            
            # account for null heightRestriction and null lightningLane
            elif heightRestriction == "" and lightningLane == "":
                query = "INSERT INTO Rides (rideName, parkID, rideLength) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideLength))
                mysql.connection.commit()

            # account for null heightRestriction and null rideLength
            elif heightRestriction == "" and rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, lightningLane) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane))
                mysql.connection.commit()

            # account for null lightningLane and null rideLength
            elif lightningLane == "" and rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction))
                mysql.connection.commit()

            # account for null heightRestriction
            elif heightRestriction == "":
                query = "INSERT INTO Rides (rideName, parkID, lightningLane, rideLength) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideLength))
                mysql.connection.commit()

            # account for null lightningLane
            elif lightningLane == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, rideLength) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideLength))
                mysql.connection.commit()

            # account for null rideLength
            elif rideLength == "":
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, lightningLane) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, lightningLane))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Rides (rideName, parkID, heightRestriction, lightningLane, rideLength) VALUES (%s, %s,%s,%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, lightningLane, rideLength))
                mysql.connection.commit()

            # redirect back to rides page
            return redirect("/rides")

    # Grab Rides data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the rides in Rides
        query = "SELECT Rides.rideID, rideName, heightRestriction, lightningLane, rideLength, Parks.parkName AS park FROM Rides LEFT JOIN Parks ON Rides.parkID = Parks.parkID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks;"
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
    query = "DELETE FROM Rides WHERE rideID = '%s';"
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
        query = "SELECT * FROM Rides WHERE rideID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab park id/name data for our dropdown
        query2 = "SELECT parkID, parkName FROM Parks"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        parks_data = cur.fetchall()

        # render edit_rides page passing our query data and parks data to the edit_ride template
        return render_template("edit_rides.j2", data=data, parks=parks_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Ride' button
        if request.form.get("edit_ride"):
            # grab user form inputs
            rideID = request.form["rideID"]
            rideName = request.form["rideName"]
            heightRestriction = request.form["heightRestriction"]
            lightningLane = request.form["lightningLane"]
            parkID = request.form["parkID"]
            rideLength = request.form["rideLength"]

            # account for null heightRestriction AND lightningLane AND rideLength
            if heightRestriction == "" and lightningLane == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = NULL, Rides.lightningLane = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideID))
                mysql.connection.commit()

            # account for null heightRestriction AND lightningLane
            elif heightRestriction == "" and lightningLane == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.rideLength = %s, Rides.heightRestriction = NULL, Rides.lightningLane = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, rideLength, rideID))
                mysql.connection.commit()

            # account for null heightRestriction AND rideLength
            elif heightRestriction == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideID))
                mysql.connection.commit()

            # account for null rideLength AND lightningLane
            elif lightningLane == "" and rideLength == "":
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = %s, Rides.lightningLane = NULL, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideID))
                mysql.connection.commit()
            
            # account for null lightningLane
            elif lightningLane == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.heightRestriction = %s, Rides.rideLength = %s, Rides.lightningLane = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, heightRestriction, rideLength, rideID))
                mysql.connection.commit()

            # account for null heightRestriction
            elif heightRestriction == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.rideLength = %s, Rides.heightRestriction = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, rideLength, rideID))
                mysql.connection.commit()

            # account for null rideLength
            elif rideLength == "" :
                # mySQL query to update the attributes of ride with our passed id value
                query = "UPDATE Rides SET Rides.rideName = %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = %s, Rides.rideLength = NULL WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, heightRestriction, rideID))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "UPDATE Rides SET Rides.rideName= %s, Rides.parkID = %s, Rides.lightningLane = %s, Rides.heightRestriction = %s Rides.rideLength = %s WHERE Rides.rideID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (rideName, parkID, lightningLane, heightRestriction, rideLength, rideID))
                mysql.connection.commit()

            # redirect back to rides page after we execute the update query
            return redirect("/rides")



# Listener

if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=9001, debug=True)
