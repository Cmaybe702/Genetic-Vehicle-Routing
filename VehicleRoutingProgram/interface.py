import double_hash_table, delivery_package, delivery_status
import datetime, sys
class Interface:

    @classmethod
    def request_user_command(cls, package_table, best_route):
        #Request a command from the user
        request_command = "\nEnter a command 1-4:\n\t1. Package insert\n\t2. Package look-up\n\t3. Get all package statuses\n\t4. Get total mileage\n\t5. Exit program\n"
        valid_selections = [1, 2, 3, 4, 5]
        user_entry = input(request_command)

        #Verify entry is a number
        while not user_entry.isnumeric():
            print("Please enter a number")
            user_entry = input(request_command)
        
        user_choice = int(user_entry)

        #Verify entry is a valid choice
        while not user_choice in valid_selections:
            print("Please enter a valid command")
            user_entry = input(request_command)
            user_choice = int(user_entry)

        #Run selected method
        if user_choice == 1:
            Interface.insert_package(package_table, best_route)
        elif user_choice == 2:
            Interface.provide_package_information(package_table, best_route)
        elif user_choice == 3:
            Interface.provide_statuses_at(package_table, best_route)
        elif user_choice == 4:
            print("Total milage for route: {}".format(round(best_route.total_distance, 2)))
            Interface.request_user_command(package_table, best_route)
        else:
            sys.exit("Goodbye!")

    @classmethod
    def provide_package_information(cls, package_table, best_route):
        #Request the package ID being searched
        request_package = "Please enter a valid package ID:\n"
        package_id = input(request_package)

        #Verify entry is a number
        while not package_id.isnumeric():
            print("Please enter a number")
            package_id = input(request_package)

        package_id = int(package_id)

        #Verify entry is a valid choice
        while not package_id in range(1, len(package_table.table) + 1):
            package_id = input(request_package)
            package_id = int(package_id)
        
        #Request a time from the user
        request_time = "Please enter a time in the format HH:MM\n"
        user_input = input(request_time)
        user_hours = user_input[0:2]
        user_minutes = user_input[3:5]

        #Verify hours is a numeric value
        while not user_hours.isnumeric():
            print("Hours should be a numeric value in the format HH")  
            user_hours = input("Please enter hours:\n")

        #Verify minutes is a numeric value
        while not user_minutes.isnumeric():
            print("Minutes should be a numeric value in the format MM")  
            user_minutes = input("Please enter minutes:\n")

        user_hours = int(user_hours)
        user_minutes = int(user_minutes)

        #Verify hour value is valid
        while not user_hours in range(1, 25):
            print("Hours should be between 1 and 24")  
            hours = input("Please enter hours:\n")
            hours = int(hours)

        #Verify minute value is valid
        while not user_minutes in range(0, 60):
            print("Minutes should be between 0 and 59")  
            minutes = input("Please enter minutes:\n")
            minutes = int(minutes)   

        #Find package and print data
        time = datetime.timedelta(hours = user_hours, minutes = user_minutes)
        requested_package = package_table.look_up(package_id)
        status = requested_package.get_package_status(time)
        print(requested_package)
        print("At {}".format(time))
        print(status)

        #Check another package or exit
        check_again = input("Would you like to check another package? Enter y for yes\n")
        if check_again == 'y':
            Interface.provide_package_information(package_table, best_route)
        #Return to command request
        else:
            Interface.request_user_command(package_table, best_route)

    @classmethod
    def provide_statuses_at(cls, package_table, best_route):
        package_list = package_table.table

        #Request a time from the user
        request_time = "Please enter a time in the format HH:MM\n"
        user_input = input(request_time)
        user_hours = user_input[0:2]
        user_minutes = user_input[3:5]

        #Verify hours is a numeric value
        while not user_hours.isnumeric():
            print("Hours should be a numeric value in the format HH")  
            user_hours = input("Please enter hours:\n")

        #Verify minutes is a numeric value
        while not user_minutes.isnumeric():
            print("Minutes should be a numeric value in the format MM")  
            user_minutes = input("Please enter minutes:\n")

        user_hours = int(user_hours)
        user_minutes = int(user_minutes)

        #Verify hour value is valid
        while not user_hours in range(1, 25):
            print("Hours should be between 1 and 24")  
            hours = input("Please enter hours:\n")
            hours = int(hours)

        #Verify minute value is valid
        while not user_minutes in range(0, 60):
            print("Minutes should be between 0 and 59")  
            minutes = input("Please enter minutes:\n")
            minutes = int(minutes)   

        #Print package statuses at provided time
        time = datetime.timedelta(hours = user_hours, minutes = user_minutes)
        time_10_20 = datetime.timedelta(hours = 10, minutes = 20)
        print("At {}".format(time))
        for package in package_list:
            if package.package_id == 9:
                if time < time_10_20:
                    package.delivery_address = "300 State St"
                    package.delivery_zip = "84103"
                else:
                    package.delivery_address = "410 S State St"
                    package.delivery_zip = "84111"
            if type(package) is delivery_package.Package:
                status = package.get_package_status(time)
                print(package)
                print(status)
                print("\n")

        #Check another time or exit
        check_again = input("Would you like to check another time? Enter y for yes\n")
        if check_again == 'y':
            Interface.provide_statuses_at(package_table, best_route)
        #Return to command request
        else:
            Interface.request_user_command(package_table, best_route)

    @classmethod
    def insert_package(cls, package_table, best_route):
        current_packages = list(range(1,41))

        #Request a package ID
        request_id = "Please enter a package ID to insert:\n"
        package_id = input(request_id)

        #Verify id is a numeric value
        while not package_id.isnumeric():
            print("Package ID should be a numeric value")  
            package_id = input(request_id)

        package_id = int(package_id)

        # Package ID can not be an existing ID number
        while package_id in current_packages:
            print("Package ID must be a unique value, can not match other package IDs")
            package_id = input(request_id)

        package_id = int(package_id)
        current_packages.append(package_id)

        #Request the package address
        request_address = "Please enter the package's address:\n"
        package_address = input(request_address)

        #Request delivery deadline
        request_delivery_deadline = "Please enter a delivery deadline, if none enter EOD:\n"
        delivery_deadline = input(request_delivery_deadline)

        #Request delivery city
        delivery_city = input("Please enter the delivery city:\n")

        #Request delivery zip
        deivery_zip = input("Please enter the delivery zip code:\n")

        #Request package weight
        request_weight = "Please enter the package weight:\n"
        package_weight = input(request_weight)

        while not package_weight.isnumeric():
            print("Package weight should be a numeric value")  
            package_weight = input(request_weight)

        #Request package status
        valid_statuses = [1, 2, 3]
        request_status = "Please enter the package's status (1-3): 1. At the hub 2. En Route 3. Delivered\n"
        package_status_id = input(request_status)

        while not package_status_id.isnumeric():
            print("Package status should be a number 1-3")
            package_status_id = input(request_status)

        #Verify a valid status was entered
        package_status_id = int(package_status_id)
        while not package_status_id in valid_statuses:
            print("Package status should be a number 1-3")
            package_status_id = input(request_status)

        special_notes = ""

        package_status_id = int(package_status_id)

        insert_success, delivery_loc = package_table.insert(package_id,  package_address, delivery_deadline, delivery_city, deivery_zip, package_weight, special_notes, delivery_status.DeliveryStatus(package_status_id))

        #If the table is full resize + 5
        if insert_success == False:
            package_table.resize_table()
            insert_success, delivery_loc = package_table.insert(package_id,  package_address, delivery_deadline, delivery_city, deivery_zip, package_weight, special_notes, delivery_status.DeliveryStatus(package_status_id))
        else:
            print("Insert successful")

        #Add another package or exit
        add_more = input("Would you like to add another package? Enter y for yes\n")
        if add_more == 'y':
            Interface.insert_package(package_table, best_route)
        #Return to command request
        else:
            Interface.request_user_command(package_table, best_route)








