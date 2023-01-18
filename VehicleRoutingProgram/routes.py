import double_hash_table, delivery_package, delivery, generation, delivery_truck
import random, math, datetime

class Route:
    NUM_TRUCKS = 3
    NUM_ROUTES_FIRST_GEN = 10
    MAX_TRUCK_PACKAGES = 16
    OVER_PACKAGE_PENALTY = 20
    OVER_MILAGE_PENALTY = 40
    DELIVERY_DEADLINE = datetime.timedelta(hours = 10, minutes = 30)
    DELIVERY_DEADLINE_9 = datetime.timedelta(hours = 9)

    #Constructor for route used by genetic algorithm
    def __init__(self, route_id, num_trucks):
        self.route_id = route_id
        self.fitness_value = math.inf
        self.total_distance = 0
        self.trucks_over_package_limit = 0
        #For each truck in the route, create a list to hold assigned deliveries
        self.route_list = []
        self.truck_distances = []
        for x in range(num_trucks):
            self.route_list.append([])

    def __str__(self):
        route_print = "Route {}:\nFitness: {}\n".format(self.route_id, self.fitness_value)
        index = 1
        for truck in self.route_list:
            route_print += 'Truck {}:\n'.format(index)
            for delivery in truck:
                for package in delivery[0].packages_list:
                    route_print += "{}, ".format(package.package_id)
            index += 1
            route_print += "\n"
        return route_print


    #Used to generate a sequence of routes for genetic algorithm
    @classmethod
    def generate_random_routes(cls, generation_number, delivery_table):
        #If it is the first generation, 10 sequences are generated. If future gen 2 sequences are generated for diversity
        if generation_number == 1:
            num_sequences = Route.NUM_ROUTES_FIRST_GEN
            gen_value = 0
        #FIX ME account for convergence
        else:
            num_sequences = generation.Generation.NUM_FROM_RANDOM_GENERATION
            gen_value = generation_number * 10 + 6        
        #Create sequence list for generation
        sequences_list = [] 
        for x in range(num_sequences):
            sequences_list.append([])

        #Generate a random floating point for each delivery to determine ordering
        for x in range(num_sequences):
            for delivery in delivery_table:
                if type(delivery) is double_hash_table.EmptyBucket:
                    pass
                else:
                    #Generate sequence value if deadline / 2
                    sequence_value = random.uniform(a= 0, b=1)
                    if delivery.packages_deadline == True:
                        sequence_value = sequence_value / 4

                    #If a package has the wrong address delivery is delayed
                    if delivery.wrong_address == True:
                        sequence_value = sequence_value * 5

                    #Generate truck number, if a package is delayed it will be on truck # 3 if specified it will be on truck # 2
                    if delivery.packages_delayed == True:
                        sequence_value = sequence_value + 3
                    elif delivery.truck_2_delivery == True:
                        sequence_value = sequence_value + 2
                    elif delivery.combine_delivery == True:
                        sequence_value = sequence_value + 1
                    else:
                        sequence_value = sequence_value + random.randint(1, 3)
                    sequence_value = round(sequence_value, 2)
                    sequences_list[x].append({"Delivery" : delivery, "Sequence value" : sequence_value})

        #Sort sequence values per delivery to determine route
        for x, sequence in enumerate(sequences_list):
            current_route = Route(x + gen_value, Route.NUM_TRUCKS)
            sequence = sorted(sequence, key= lambda item: item['Sequence value'])
            for delivery in sequence:
                current_route.add_delivery(delivery["Delivery"], delivery['Sequence value'])
        
            #If not gen 1 calculate fitness value for route
            if generation_number > 1:
                current_route.calculate_route_fitness()

            #Add route to current generation
            generation.Generation.current_generation.append(current_route)
        
        #FIX ME, to test route generation
        #for route in generation.Generation.current_generation:
           # print(route)
        

    #Used to add a delivery to a route in genetic sequence order            
    def add_delivery(self, delivery, sequence_value):
        tup = (delivery, sequence_value)
        #Integer of sequence value determines truck number
        if sequence_value < 2:
            self.route_list[0].append(tup)
        elif sequence_value < 3:
            self.route_list[1].append(tup)
        else:
            self.route_list[2].append(tup)

    #Used to calculate and assign a fitness value to a route
    def calculate_route_fitness(self):
        route_fitness_val = 0
        total_distance = 0
        trucks_over_package_limit = 0
        truck_number = 1
        late_packages = 0
        time_over_limit = 0

        #For each truck in the route calculate the distance traveled and number of packages
        for truck in self.route_list:
            previous_delivery = None
            num_packages = 0
            truck_distance = 0

            #Assign truck start time
            if truck_number == 3:
                current_time = datetime.timedelta(hours = 9, minutes = 5)
            else:
                current_time = datetime.timedelta(hours = 8)

            for delivery_tup in truck:
                #If no previous location then departure from hub, calculate distance between locations and add to total
                if previous_delivery is None:
                    current_distance = delivery_tup[0].location.distances_list[0]
                else:
                    previous_location = previous_delivery.location
                    previous_location_id = previous_location.id
                    current_distance = delivery_tup[0].location.distances_list[previous_location_id]
                
                #Calculate delivery time, add penalty if deadline was not met 
                minutes_spent = (current_distance / delivery_truck.DeliveryTruck.TRUCK_MPH) * 60
                current_time = current_time + datetime.timedelta(minutes = minutes_spent)
                if delivery_tup[0].packages_deadline == True:
                    if delivery_tup[0].early_deadline == True:
                        if current_time > Route.DELIVERY_DEADLINE_9:
                            late_packages += 1
                            time_late = current_time - Route.DELIVERY_DEADLINE_9
                            seconds_late = time_late.total_seconds()
                            minutes_late = seconds_late // 60
                            time_over_limit = time_over_limit + minutes_late
                    elif current_time > Route.DELIVERY_DEADLINE:
                        late_packages += 1
                        time_late = current_time - Route.DELIVERY_DEADLINE
                        seconds_late = time_late.total_seconds()
                        minutes_late = seconds_late // 60
                        time_over_limit = time_over_limit + minutes_late
                truck_distance = truck_distance + current_distance
                
                #Calculate packages in truck
                for y in range(len(delivery_tup[0].packages_list)):
                    num_packages = num_packages + 1

                #Assign current location to previous_delivery location for next delivery
                previous_delivery = delivery_tup[0]

            #Add distance traveled / truck to list
            self.truck_distances.append(round(truck_distance, 2))

            # For testing truck route generation
            # print("Truck {}: Distance: {} Packages: {}".format(truck_number, truck_distance, num_packages))
            truck_number += 1
            total_distance = total_distance + truck_distance

            #If truck has more than MAX_TRUCK_PACKAGES it is over limit
            if num_packages > Route.MAX_TRUCK_PACKAGES:
                trucks_over_package_limit += 1

        #Add each trucks distance traveled to the fitness value
        route_fitness_val = route_fitness_val + total_distance

        #Assess penality if trucks are over milage
        if total_distance > 140:
            route_fitness_val = route_fitness_val + Route.OVER_MILAGE_PENALTY

        #Assess penality if truck is over package limit
        route_fitness_val = route_fitness_val + Route.OVER_PACKAGE_PENALTY * trucks_over_package_limit

        #Assess penality for late packages
        route_fitness_val = route_fitness_val + time_over_limit * (late_packages ** 2)

        #Save fitness values in route
        self.total_distance = total_distance
        self.fitness_value = route_fitness_val
        self.trucks_over_package_limit = trucks_over_package_limit

        #For testing route fitness generation
        #print("Route: {}, Fitness Value: {}, Trucks Over Package Limit: {}\n".format(self.route_id, self.fitness_value, self.trucks_over_package_limit))

