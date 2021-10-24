class kernel:
    objects = []

    def __init__(self, id, length=None, area=None, material = None):
        if length == '':
            length = 0
        if material == '':
            material = 0
        if material == '':
            material = 1
        self.id = int(id)
        self.length = float(length)
        self.material = int(material)
        self.area = float(area)
        self.__class__.objects.append(self)

class material:
    objects = []
    def __init__(self, id, elasticity, sigma):
        self.id = id
        self.elasticity = float(elasticity)
        self.sigma = float(sigma)
        self.__class__.objects.append(self)


class concentrated:
    objects = []

    def __init__(self, point, power=0):
        self.point = int(point)
        self.power = float(power)
        self.__class__.objects.append(self)

class running:
    objects = []

    def __init__(self, kernel, power=0):
        self.kernel = kernel
        self.power = float(power)
        self.__class__.objects.append(self)