# Courtney Mayberry 001524338

import locations, delivery_package, routes, generation, delivery, delivery_truck, interface
import datetime

#Initilize locations from csv file
locations.Location.initilize_locations()

#Initilize packages from csv file
hash_table, package_table, num_deliveries = delivery_package.Package.read_packages()

delivery_table = delivery.Delivery.combine_matching_deliveries(package_table, num_deliveries)

#Start genetic algorithm to create routes
generation_count = 1
routes.Route.generate_random_routes(generation_count, delivery_table)

#Calculate the fitness of the routes in the current generation
for route in generation.Generation.current_generation:
    route.calculate_route_fitness()

#Rank routes in current generation by fitness value
generation.Generation.rank_routes_in_generation()

#Start mutation of generations
generation_count += 1
generation.Generation.create_next_generation(generation_count, delivery_table)

#Find the best fit route
best_route = generation.Generation.current_generation[0]
print("The selected route is: ")
print(best_route)
print("Truck distances: {}".format(best_route.truck_distances))
print("Total distance: {}".format(round(best_route.total_distance, 2)))
print("Trucks over package limit: {}".format(best_route.trucks_over_package_limit))

#Create trucks and assign routes
delivery_truck.DeliveryTruck.create_trucks(best_route)

#Start deliveries
delivery_truck.DeliveryTruck.start_deliveries()

#Ask user for operation
interface.Interface.request_user_command(hash_table, best_route)
