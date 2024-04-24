class Vehacle:
    def __init__(self, make, model):
        self.make = make
        self.model = model
    def get_info(self):
        return f'The make of this car is {self.make}, the model is {self.model}'

class Car(Vehacle):
    def __init__(self, make, model, wheels):
        super().__init__(make, model)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis car has {self.wheels} wheels'

class Moto(Vehacle):
    def __init__(self, make, model, wheels):
        super().__init__(make, model)
        self.wheels = wheels
    def get_info(self):
        return f'{super().get_info()} \nThis car has {self.wheels} wheels'

car = Car('BMW', 'M5', 4)
motorcycle = Moto('Toyota', 'CH2843', 2)

print(car.get_info())
print(motorcycle.get_info())
