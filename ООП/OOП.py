class Vehacle:
    def __init__(self, make, model):
        self.make = make
        self.model = model
    def get_info(self):
        return f'The make of this car is {self.make}, the model is {self.model}.'


class Car(Vehacle):
    def __init__(self, make, model, wheels):
        super().__init__(make, model)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis car has {self.wheels} wheels.'


class Moto(Vehacle):
    def __init__(self, make, model, wheels):
        super().__init__(make, model)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis motorcycle has {self.wheels} wheels.'


class Electric:
    def __init__(self, battery):
        self.battery = battery
    def charge(self):
        return f'This car has {self.battery}% battery.' if self.battery <= 100 else f'Your battery is bullshit.'


class ElectricCar(Vehacle, Electric):
    def __init__(self, make, model, battery, wheels):
        Vehacle.__init__(self, make, model)
        Electric.__init__(self, battery)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis car has {self.wheels} wheels. \n{super().charge()}'


class ElectricMoto(Vehacle, Electric):
    def __init__(self, make, model, battery, wheels):
        Vehacle.__init__(self, make, model)
        Electric.__init__(self, battery)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis motorcycle has {self.wheels} wheels. \n{super().charge()}'


car = Car('BMW', 'M5', 4)
motorcycle = Moto('Toyota', 'CH2843', 2)
electric_car = ElectricCar('Tesla', '3H4J5K6', 100, 4)
electric_moto = ElectricMoto('Honda', '83HGD6', 110, 2)

print(car.get_info())
print(motorcycle.get_info())
print(electric_car.get_info())
print(electric_moto.get_info())

print(isinstance(car, ElectricMoto))
print(isinstance(motorcycle, Moto))
print(isinstance(electric_car, Vehacle))
print(isinstance(electric_moto, ElectricCar))

print(Car.mro())
print(ElectricMoto.mro())
print(Moto.mro())
print(ElectricCar.mro())
print(Vehacle.mro())
print(Electric.mro())
