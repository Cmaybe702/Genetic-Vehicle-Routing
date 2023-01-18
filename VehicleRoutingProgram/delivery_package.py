import locations, double_hash_table, delivery_status
import csv, datetime

class Package:
    
    #Constructor for package objects, assigns assoicated delivery location
    def __init__(self, package_id, delivery_address, delivery_zip, delivery_city, delivery_deadline, package_weight, special_notes, delivery_status):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_zip = delivery_zip
        self.delivery_city = delivery_city
        self.delivery_deadline = delivery_deadline
        self.package_weight = int(package_weight)
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.delivery_number = None
        self.delivery_time = None
        self.assigned_truck = None
        self.deadline_bool = False
        self.early_deadline_bool = False
        self.wrong_address = False
        self.package_delayed = False
        self.truck_2_delivery = False
        self.combine_delivery = False

        #Assign a bool value indicating if the package has a dealine
        if delivery_deadline != "EOD":
            self.deadline_bool = True
            if delivery_deadline < datetime.timedelta(hours=10):
                self.early_deadline_bool = True

        #Find address and assign location
        for location in locations.Location.locations_list:
            if location.address.__eq__(self.delivery_address):
                self.delivery_location = location 
                break  
            else:
                self.delivery_location = "Not found"

        #Assign a bool values for special notes
        delayed_string = "Delayed"
        wrong_address = "Wrong address"
        truck_2 = "truck 2"
        combine_deliveries = [13, 14, 15, 16, 19, 20]
        if delayed_string in special_notes:
            self.package_delayed = True
        elif wrong_address in special_notes:
            self.wrong_address = True
        elif truck_2 in special_notes:
            self.truck_2_delivery = True  
        elif package_id in combine_deliveries:
            self.combine_delivery = True  
    
    #Used to print package data
    def __str__(self):
            return 'Package ID: {} \nAddress: {}\nCity: {}\nZip: {}\nDelivery Deadline: {}\nWeight: {}'.format(self.package_id, self.delivery_address, self.delivery_city, self.delivery_zip, self.delivery_deadline, self.package_weight)

    #Reads in package data from associated csv file and transfers data to double hash table for storage
    @classmethod
    def read_packages(cls):
        visited_locations = []
        incorrect_addresses = 0
        #Determine the number of packages
        with open("Package_list.csv") as csv_file:
            csv_reader = csv.reader(csv_file)
            row_count = sum(1 for row in csv_reader)
        
        #Create package table with number of packages
        package_table = double_hash_table.DoubleHashingTable(row_count)

        #Open csv package file & load data
        with open("Package_list.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            #For each row in the package list read in package data
            for row in csv_reader:
                package_number = int(row[0])
                address = row[1].strip()
                city = row[2]
                zip_code = row[4]
                delivery_deadline = row[5]
                weight = int(row[6])
                special_notes = row[7]
                
                #If address is wrong then package is not comind into a delivery
                wrong_address = "Wrong address"
                if wrong_address in special_notes:
                    incorrect_addresses += 1

                #Assign deadline
                early_deadline = "9:00"
                late_deadline = "10:30"
                if early_deadline in delivery_deadline:
                    delivery_deadline = datetime.timedelta(hours = 9)
                elif late_deadline in delivery_deadline:
                    delivery_deadline = datetime.timedelta(hours = 10, minutes = 30)

                #Create package objects and insert into table
                insert_success, location = package_table.insert(package_number, address, delivery_deadline, city, zip_code, weight, special_notes)
                
                #If successfully inserted log location for delivery table
                if insert_success:
                    visited_locations.append(location.id)

                #Determine the number of deliveries
                unique_locations = set(visited_locations)
                num_deliveries = len(unique_locations) + incorrect_addresses
                
        return package_table, package_table.table, num_deliveries
    
    #Used to get the status of a package
    def get_package_status(self, time):
        truck_departure = None
        if self.assigned_truck is None:
            truck_departure = datetime.timedelta(hours= 12)
        elif self.assigned_truck.truck_number == 3:
            truck_departure = datetime.timedelta(hours = 9, minutes = 5)
        else:
            truck_departure = datetime.timedelta(hours = 8)
        
        #If the time is < truck departure status is AT_THE_HUB, if > departure < delivery status is EN_ROUTE, else DELIVERED
        if time < truck_departure:
            status = delivery_status.DeliveryStatus(1)
        elif time < self.delivery_time:
            status = delivery_status.DeliveryStatus(2)
        else:
            status = delivery_status.DeliveryStatus(3)
            status = str(status) + " at {}".format(self.delivery_time)
        return status