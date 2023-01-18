import random
import delivery, delivery_package, double_hash_table, routes

class Generation:
    NUM_GENERATIONS = 20
    NUM_FROM_PREVIOUS_GEN = 2
    NUM_FROM_CROSSOVER = 6
    NUM_FROM_RANDOM_GENERATION = 2
    current_generation = []
    next_generation = []

    #Used to rank routes in current generation by their fitness value(min value is the most fit route)
    @classmethod
    def rank_routes_in_generation(cls):
        Generation.current_generation.sort(key= lambda route: route.fitness_value)
        
        #FIX ME For testing route ranking
        #for route in Generation.current_generation:
            #print(route)

    #Used to create the next generation of routes
    @classmethod
    def create_next_generation(cls, generation_number, delivery_table):
        #Add NUM_FROM_PREVIOUS_GEN most fit routes to next generation
        for x in range(Generation.NUM_FROM_PREVIOUS_GEN):
            Generation.next_generation.append(Generation.current_generation[x])

        #Generate and add NUM_FROM_CROSSOVER routes 
        Generation.generate_route_via_crossbreed(Generation.NUM_FROM_CROSSOVER, delivery_table, generation_number)

        #Assign current generation with next generation info
        Generation.current_generation.clear()
        Generation.current_generation = list(Generation.next_generation)
        Generation.next_generation.clear()

        #Generate and add NUM_FROM_RANDOM_GENERATION routes
        routes.Route.generate_random_routes(generation_number, delivery_table)

        #Rank routes in current generation
        Generation.rank_routes_in_generation()

        #FIX Me, For testing generation creation
        #print("Generation {}".format(generation_number))
        #for route in Generation.current_generation:
            #print(route)
        
        #Increment generation number, if generation is less than or equal to max generation recursive call
        generation_number = generation_number + 1

        if generation_number <= Generation.NUM_GENERATIONS:
            Generation.create_next_generation(generation_number, delivery_table)
        else:
            return

    #Used to generate num_routes from crossbreeding randomly selected parents for next generation
    @classmethod
    def generate_route_via_crossbreed(cls, num_routes, delivery_table, generation_number):
        for x in range(num_routes):

            #Select parents 
            parent1_num = random.randint(0,9)
            parent2_num = random.randint(0,9)

            parent1 = Generation.current_generation[parent1_num]
            parent2 = Generation.current_generation[parent2_num]

            #Merge route parent delivery list to enable access to all sequence values
            parent1_list = parent1.route_list[0] + parent1.route_list[1] + parent1.route_list[2]
            parent2_list = parent2.route_list[0] + parent2.route_list[1] + parent2.route_list[2]
       
            #Create sequence list for cross breed
            sequence_list = [] 

            #For each delivery select parent sequence number
            for delivery in delivery_table:
                if type(delivery) is double_hash_table.EmptyBucket:
                    pass
                else:
                    selected_parent = random.randint(1, 2)
                    #Find sequence value for delivery in selected parent's list
                    if selected_parent == 1:
                        for tup in parent1_list:
                            if tup[0] == delivery:
                                sequence_value = tup[1]
                    else:
                        for tup in parent2_list:
                            if tup[0] == delivery:
                                sequence_value = tup[1]
                    sequence_list.append({"Delivery" : delivery, "Sequence value" : sequence_value})

            #Create new route
            current_route = routes.Route(x + 10 * generation_number , routes.Route.NUM_TRUCKS)

            #Sort sequence values per delivery to determine route
            sequence_list.sort(key= lambda delivery: delivery['Sequence value'])
            for delivery in sequence_list:
                current_route.add_delivery(delivery["Delivery"], delivery['Sequence value'])
            
            #Calculate route fitness
            current_route.calculate_route_fitness()

            #Add route to current generation
            Generation.next_generation.append(current_route)