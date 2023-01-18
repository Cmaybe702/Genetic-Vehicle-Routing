# Genetic-Vehicle-Routing

For developers:

This implementation loads package data and locations from a CSV file to a double hash table with 40 entries. To add additional entries please edit the double hash table file. Distances between locations is provided by the distance table.cs file. In order to customize the solution for your use case please update all files with relevant information. To adjust delivery contstraints please see the generation file.

About the project:

This project uses a genetic algorithm to create a solution to the VRP that can not only be scaled to apply to larger sets of data but can also be customized to meet the requirements presented by unique constraints that arise when the solution is applied to real life situations. The genetic algorithm is a heuristic algorithm that utilizes the theory of natural selection to find the most fit solution to a problem within a given number of generations. When applied to the VRP each solution is considered a chromosome, representing the sequence of stops for each vehicle.

The first-generation chromosomes are created by randomly generating a sequence value that represents the truck number the delivery is assigned to and the order in which the location will be visited by that truck. Each chromosome is then assessed a fitness value that consists of the distance traveled by each vehicle and penalty values added if any of the constraints placed on the deliveries are not met. The chromosomes are then ranked by fitness, a low fitness value indicating that the chromosome is a good fit for the problem. Subsequent generations are created by taking a percentage of the most fit chromosomes from the prior generation, creating a percentage of chromosomes from sequence value crossover of randomly selected parents from the previous generation, and a percentage of new chromosomes generated randomly. Through this natural selection process the route that is the most fit for the parameters provided will found.

The genetic algorithm is a great solution to the VRP because it can be easily adapted to a larger volume of input and can handle additional restrictions without a significant increase in runtime. When working with an increased number of packages and vehicles, the number of generations created can be tuned to find a balance between the fitness of the solution and the time it takes to generate it. When creating the hash table to store package data, the number of lines in the file is first read and a hash table is created with the number of buckets needed. Additionally, no additional programming is needed to adapt the solution to a changing number of packages, locations, or vehicles. Any variables that determine the functionality of route or generation creation have been coded as constants that can be easily updated in the code or a GUI can be created so a user can update these values before generating a solution. The solution also leaves room to adapt to changing priorities through the generation of the fitness value. For this implementation the fitness value is determined by the distance the vehicles travel, if deadlines are met, and if vehicles are over their package limit. If heavy packages are being shipped the fitness value could be updated to account for weight with only a few lines of code being added. 

As mentioned above the software created for this project was created with efficiency and ease of maintenance in mind. To achieve efficient route generation with a growing number of packages the number of generations can be adjusted and tuned to find a balance between the fitness of the solution generated for the provided input and the time it takes to generate the solution. Before any package data is read, the number of lines in the CSV file is determined and a data structure with a matching capacity is created. Storage for the delivery table is dynamically allocated after the number of locations that will be visited is determined by the package insertion function and can be adapted to any number of locations. The program can also be adjusted by changing constant values in the generation module to account for premature convergence of values if many generations are needed to find an appropriate solution. If the number of vehicles that are servicing the area changes a constant value in the delivery truck module can be easily adjusted to adapt the program to use a smaller/large number of vehicles in the solution. Values used to assess the fitness of the route (delivery deadline times, penalty values, and package limits) have also been coded as constants so they can be easily adjusted if the restrictions placed on the deliveries change over time. 
