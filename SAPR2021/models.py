
class material:
    objects = []
    def __init__(self, id, elasticity, sigma):
        self.id = int(id)
        self.elasticity = float(elasticity)
        self.E = self.elasticity
        self.sigma = float(sigma)
        self.__class__.objects.append(self)
        print('material', id)


class kernel:
    objects = []

    def __init__(self, id, length=None, area=None, _material = None):
        if length == '':
            length = 0
        if _material == '':
            _material = 0
        if _material == '':
            _material = 1
        self.id = int(id)
        self.length = float(length)
        self.L = self.length
        self.material = int(_material)
        self.materialObj = None 
        for mat in material.objects:
            if mat.id == self.material:
                self.materialObj = mat
        self.area = float(area)
        self.A = self.area
        self.__class__.objects.append(self)
        self.Q = 0
        for power in running.objects:
            if power.kernel == self.id:
                self.Q += power.power

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