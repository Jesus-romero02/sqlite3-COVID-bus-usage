#Jesus Romero
# jromer61@uic.edu
#I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s
#Academic Integrity standards. Signed: Jesus Romero




import pandas
import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def convert():
  #Added a connection and a cursor as well as an execution line that checks to see if the table already exists. If the table exists, it just replaces the existing table. Doing this is just more efficient because otherwise you would need to delete the database everytime you run the code because you would get an error. 
  data = pandas.read_csv("bus_data.csv")
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  cur.execute("DROP table IF EXISTS bus_rides")
  cur.execute("CREATE TABLE bus_rides (route TEXT,date TEXT,daytype TEXT, rides INT)")
  #Created a table with the same column names from the CSV file
  for i in range(len(data)):
    a = data["route"][i]
    b = data["date"][i]
    c = data["daytype"][i]
    d = int(data["rides"][i])
    cur.execute("INSERT INTO bus_rides VALUES(?,?,?,?);",(a,b,c,d,))
  #Looped over the data from the CSV file in order to insert the values into the data base and their respective columns. As opposed to the % or .format ways to format, I used the ? formatting which seems easier to work with in SQL.
  conn.commit()
  conn.close()
  #At the end, the CSV file took up 19.3 MB and the database file took up 29.3 MB


def route_data(given_route):
  
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  output = cur.execute("SELECT AVG(rides) FROM bus_rides WHERE (route ==?);",(str(given_route)))
  data = output.fetchall()
  for i in data:
     for i in i:
       print("The average daily ridership for the route",given_route,"was",i)
  #Up to here, I basically used SQL to select the average of all rides where the route is equal to the given route. I then went ahead and made the print statement as well. 

  output2 = cur.execute("SELECT rides FROM bus_rides WHERE (route==?);",(str(given_route)))
  data2 = output2.fetchall()
  total_route_entries = 0
  for i in data2:
    total_route_entries += 1
  #For this part, I went ahead and picked out all the instances of the route. All this means is how many total days the route was tracked for in this file, so that I'm able to calculate my percentage later.
          
  output3 = cur.execute("SELECT rides FROM bus_rides WHERE (route==?) AND (rides>=1200);",(str(given_route)))
  data3 = output3.fetchall()
  #Up to here, I selected the instances of where the number of rides was greater than or equal to 1200 in that given route. 
  entries_counter = 0
  for i in data3:
    entries_counter += 1
  percentage =(entries_counter/total_route_entries)*100
  print("About",percentage,"% of the days in route",given_route,"were in heavy use")
  conn.close()
#I was able to calculate the percentage of days that were considered heavy for that specific route by dividing the total number of days by the days that were heavy. I then multiplied that by 100 to get a nice percentage. 


def yr_sum(*args):
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  sum = 0
  for i in args:
    output = cur.execute("SELECT SUM(rides) FROM bus_rides WHERE date LIKE (?);",('%'+str(i),))
  #I used the LIKE keyword to grab the sum of the rides for all the entries that have a date that ends in each of the given years we're adding. I had to make a for loop because we are looking for the sum for multiple years so I found it easier to get the sum of rides for each year and then add them all up after. 
    data = output.fetchall()
    for i in data:
      for i in i:
        sum = sum + i 
  conn.close()
  print("The total sum of rides for the years provided is",sum,"rides")


def my_func():
  x = np.linspace(0,1460)
  y = []
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  for i in ["2019","2020","2021"]:
    output = cur.execute("SELECT rides FROM bus_rides WHERE date LIKE (?);",("%"+i,))
    data = output.fetchall()
    for i in data:
      for i in i:
        print(i)
        y.append(int(i))
  plt.plot(x,y)
  plt.show()
  plt.savefig("COVID_ON_TRANS")
  conn.close()
  #Here, I grabbed the number of rides between the years 2019,2021 just to kind of compare how drastic of a change COVID made on public transportation. 2019 was normal, 2020 went down drastically, and 2021 was also abnormally low but slowly creeping back up! Of course people were scared of being in any public space and so public transportation was out of the question to a lot of people at the time. 

def update():
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  cur.execute("UPDATE bus_rides SET rides = (rides-(FLOOR(rides*.1))) WHERE (daytype='A')")
  conn.commit()
  conn.close()
  
    
              
  

    
    

  