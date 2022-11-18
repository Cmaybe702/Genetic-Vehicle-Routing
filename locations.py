import csv

#Class used to store location data and distances between locations
class Location:
    locations_list = []
    
    #Constructor for locaitons
    def __init__(self, location_id, location_address, location_zip):
        self.id = location_id
        self.address = location_address
        self.zip = location_zip
        self.distances_list = []

    #Used to print a reprsentation of the location
    def __str__(self):
        return str("ID: {}, Address: {}".format(self.id, self.address))

    #Used to read in location data from a csv file and create the locations list
    @classmethod
    def initilize_locations(cls):
        #Open csv locations file
        with open("Distance_table.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            count = 0

            #For each row in the locations list read in the address and zip
            for row in csv_reader:
                address_line = row[0].strip()

                #Hub locaiton does not include zip in csv
                if count == 0:  
                    address = address_line
                    zip_code = "84107"
                else:
                    address_line = address_line.split('\n')
                    address = address_line[0]
                    zip_code = address_line[1]
                    zip_code = zip_code[1:6]

                #Create location and add to locations list
                new_location = Location(count, address, zip_code)
                Location.locations_list.append(new_location)

                #Assign distances from distance file
                for x in range(0,count + 1):
                        new_location.distances_list.append(float(row[x + 1]))
                count = count + 1

            #Assign missing distances from table
            for x in range(len(Location.locations_list) -1 , -1, -1):
                missing_distances = len(Location.locations_list) - x - 1
                if missing_distances == 0:
                    pass
                else:
                    for y in range(0, missing_distances):
                        Location.locations_list[x].distances_list.append(0)
                #Find associated distance and assign
                for z in range(len(Location.locations_list) - 1 , x, -1):
                    Location.locations_list[x].distances_list[z] = Location.locations_list[z].distances_list[x]
    @classmethod
    def print_locations(cls):
        for location in Location.locations_list:
            print(location)