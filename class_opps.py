class Car:
    seat=6
    def __init__(self,name,model_name):
        self.name = name
        self.model_name = model_name

    def gear(self):
        print("Top Gear")

    def get_car_name(self):
        return self.name,self.model_name

car_obj=Car("maruti",800)

car_info = car_obj.get_car_name()

print(car_info)

print(car_obj.seat)

# name = car_obj.get_car_name()

# print(name)