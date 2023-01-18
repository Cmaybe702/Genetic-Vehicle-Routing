from enum import Enum

class DeliveryStatus:
    AT_THE_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3

    #Constructor for delivery status, set by default to "At the hub"
    def __init__(self, status_number):
        if status_number == 1:
            self.status = DeliveryStatus.AT_THE_HUB
        elif status_number == 2:
            self.status = DeliveryStatus.EN_ROUTE
        else:
            self.status = DeliveryStatus.DELIVERED

    #Used to print the status 
    def __str__(self):
        status_string = ""
        if self.status == 1:
            status_string = 'At the hub'
        elif self.status == 2:
            status_string = 'En route'
        else:
            status_string = 'Delivered'
        return status_string