import delivery_package, delivery_status, delivery

#Class used to represent and empty bucket in the hash table
class EmptyBucket:
    pass

#Hash table class for storing packages
class DoubleHashingTable:

    #Constructor for hash table, all buckets are set to EMPTY_SINCE_START upon creation
    def __init__(self, initial_capacity):

        #Constants used to identify empty buckets and types
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()

        #All table cells set to EMPTY_SINCE_START
        self.table = [self.EMPTY_SINCE_START] * initial_capacity

    #Secondary hash function
    def h2(self, package_id):
        return 43 - hash(package_id) % 43

    #Used to create and insert packages into the package table
    def insert(self, package_id, address, delivery_deadline, city, zip_code, weight, special_notes, delivery_status = delivery_status.DeliveryStatus(1)):

        new_package = delivery_package.Package(package_id, address, zip_code, city, delivery_deadline, weight, special_notes, delivery_status)

        #Calculate bucket and search for insert location
        for x in range(len(self.table)):
            #Bucket index for iteration x
            bucket = (hash(package_id) + self.h2(package_id) * x) % len(self.table)
            if type(self.table[bucket]) is EmptyBucket:
                self.table[bucket] = new_package
                return True, new_package.delivery_location

        #All table locations are full, could not insert package
        return False, None

    #Used to create deliveries and associate packages
    def insert_delivery(self, delivery_id, address, location):

        new_delivery = delivery.Delivery(delivery_id, address, location)
        
        #Calculate bucket and search for insert location
        for x in range(len(self.table)):
            #Bucket index for iteration x
            bucket = (hash(delivery_id) + self.h2(delivery_id) * x) % len(self.table)
            if type(self.table[bucket]) is EmptyBucket:
                self.table[bucket] = new_delivery
                return new_delivery
        return None
        

    #Searches for a package with the indicated package_number, if not found reuturns None
    def look_up(self, package_id):
        for x in range(len(self.table)):
            #Calculate bucket number
            bucket = (hash(package_id) + self.h2(package_id) * x) % len(self.table)
            if self.table[bucket].package_id == package_id:
                return self.table[bucket]

        #Package number was not found        
        return None

    #Removes an item with a matching package number from the table if found
    def remove(self, package_id):
        for x in range(len(self.table)):
            #Calculate bucket number
            bucket = (hash(package_id) + self.h2(package_id) * x) % len(self.table)
            if self.table[bucket].package_id == package_id:
                 self.table[bucket] = self.EMPTY_AFTER_REMOVAL

    #Used to print a representation of the package table 
    def __str__(self):
        bucket_print = "Packages in bucket:\n"
        index = 0
        for bucket in self.table:
            if type(bucket) is EmptyBucket:
                value = "{}:\nEmpty bucket".format(index)
            else:
                value = "{}:\n{}".format(index, str(bucket))
            bucket_print += "{}\n".format(value)
            index += 1
        return bucket_print

    def resize_table(self):
        for x in range(5):
            self.table.append(self.EMPTY_SINCE_START)






