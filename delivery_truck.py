import datetime
import locations

class DeliveryTruck:
    NUM_TRUCKS = 3
    TRUCKS_DELAYED = 1
    TRUCK_MPH = 18
    trucks_list = []

    def __init__(self, truck_number, delayed = False):
        self.truck_number = truck_number
        if delayed == False:
            self.depart_time = datetime.timedelta(hours = 8)
        else:   
            self.depart_time = datetime.timedelta(hours = 9, minutes = 5)
        self.current_location = locations.Location.locations_list[0]
        self.route_list = []
        self.current_time = None

    @classmethod
    def create_trucks(cls, selected_route):
        #Create NUM_TRUCKS for delivery, if trucks are delayed start time is later
        delayed_number = DeliveryTruck.TRUCKS_DELAYED
        for x in range(DeliveryTruck.NUM_TRUCKS, 0, -1):
            if delayed_number > 0:
                new_truck = DeliveryTruck(x, True)
                delayed_number = delayed_number - 1
            else:
                new_truck = DeliveryTruck(x)

            #Assign truck route
            new_truck.route_list = selected_route.route_list[x - 1]
            DeliveryTruck.trucks_list.append(new_truck)

            #Assign truck to deliveries
            for delivery_tup in new_truck.route_list:
                delivery_tup[0].assign_truck(new_truck)


    def __str__(self):
        truck_string =  "\nTruck number: {}\nDeparture: {}\nRoute:\n".format(self.truck_number, self.depart_time)
        for delivery in self.route_list:
            truck_string = truck_string + str(delivery[0])
        return truck_string

    @classmethod
    def start_deliveries(cls):
        for truck in DeliveryTruck.trucks_list:
            truck.deliver_packages()

    #Used to make deliveries in truck route list and assign delivery times
    def deliver_packages(self):
        previous_delivery = None
        self.current_time = self.depart_time

        for delivery_tup in self.route_list:
            if previous_delivery is None:
                    miles = delivery_tup[0].location.distances_list[0]
            else:
                previous_location = previous_delivery.location
                previous_location_id = previous_location.id
                miles = delivery_tup[0].location.distances_list[previous_location_id]

            #Calculate time spent and assign delivery time    
            minutes_spent = (miles / DeliveryTruck.TRUCK_MPH) * 60
            self.current_time = self.current_time + datetime.timedelta(minutes = minutes_spent)
            delivery_tup[0].assign_delivery_time(self.current_time)
            previous_delivery = delivery_tup[0]

