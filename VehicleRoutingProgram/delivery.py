import double_hash_table, delivery_status
import datetime

class Delivery:

    #Used to create deliveries
    def __init__(self, id, address, location):
        self.id = id
        self.address = address 
        self.packages_list = []
        self.packages_deadline = False
        self.early_deadline = False
        self.packages_delayed = False
        self.wrong_address = False
        self.truck_2_delivery = False
        self.combine_delivery = False
        self.location = location
        self.delivery_time = None
        self.assigned_truck = None

    #Used to print delivery data
    def __str__(self):
        delivery_string ="Delivery number: {}\nAddress: {}\nPackages: ".format(self.id, self.address)
        for package in self.packages_list:
            delivery_string = delivery_string + str(package.package_id) + ','
        delivery_string = delivery_string + "\nHas deadline: {}\nDelivered at: {}\n".format(self.packages_deadline, str(self.delivery_time))
        return delivery_string

    #Used to combine packages with matching addresses into one delivery
    @classmethod
    def combine_matching_deliveries(cls, package_table, num_locations):
        #Create a double hash table for deliveries
        delivery_list = double_hash_table.DoubleHashingTable(num_locations)
        
        #Add packages to delivery list, combinding packages with the same address
        delivery_count = 1
        for bucket in package_table:
            found = False
            #Verify bucket holds a package
            if type(bucket) is double_hash_table.EmptyBucket:
                pass
            else:
                #Search deliveries list for matching address
                for delivery_bucket in delivery_list.table:
                    if type(delivery_bucket) is double_hash_table.EmptyBucket:
                        pass
                    else:
                        #If matching address is found add to delivery
                        if bucket.delivery_address == delivery_bucket.address:
                            #If delivery has wrong address tag create a new delivery
                            if delivery_bucket.wrong_address == True:
                                pass
                            else:
                                delivery_bucket.packages_list.append(bucket)
                                bucket.delivery_number = delivery_bucket.id 
                                #Verify if package in delivery has a deadline
                                if bucket.deadline_bool == True:
                                    delivery_bucket.packages_deadline = True
                                    if bucket.early_deadline_bool == True:
                                        delivery_bucket.early_deadline = True
                                #Verify if package in delivery is delayed
                                if bucket.package_delayed == True:
                                    delivery_bucket.packages_delayed = True
                                #Verify if package must be on truck 2
                                if bucket.truck_2_delivery == True:
                                    delivery_bucket.truck_2_delivery = True
                                #Verify if part of a combine delivery
                                if bucket.combine_delivery == True:
                                    delivery_bucket.combine_delivery = True
                                #Verify if package in delivery has the wrong address
                                if bucket.wrong_address == True:
                                    delivery_bucket.wrong_address = True
                                found = True
                                break
                #If no matching address was found create a new delivery
                if found == False:
                        new_delivery = delivery_list.insert_delivery(delivery_count, bucket.delivery_address, bucket.delivery_location)
                        new_delivery.packages_list.append(bucket)
                        bucket.delivery_number = delivery_count

                        #Verify if package in delivery has a deadline
                        if bucket.deadline_bool == True:
                            new_delivery.packages_deadline = True
                            if bucket.early_deadline_bool == True:
                                    new_delivery.early_deadline = True

                        #Verify if package in delivery is delayed
                        if bucket.package_delayed == True:
                            new_delivery.packages_delayed = True

                        #Verify if package in delivery has the wrong address
                        if bucket.wrong_address == True:
                            new_delivery.wrong_address = True

                        #Verify if package must be on truck 2
                        if bucket.truck_2_delivery == True:
                            new_delivery.truck_2_delivery = True

                        #Verify if part of a combine delivery
                        if bucket.combine_delivery == True:
                            new_delivery.combine_delivery = True
                        delivery_count += 1
        return delivery_list.table

    def assign_delivery_time(self, time):
        self.delivery_time = time
        for package in self.packages_list:
            package.delivery_time = time
            package.delivery_status = delivery_status.DeliveryStatus(3)
    
    def assign_truck(self, truck):
        self.assigned_truck = truck
        for package in self.packages_list:
            package.assigned_truck  = truck