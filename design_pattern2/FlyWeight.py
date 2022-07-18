import weakref

"""
享元模式：
一种内存优化的模式。可以确保对象中的共享状态使用同一内存进行存储。
弱引用介绍：
弱引用不会增加对象的引用数量。引用的目标对象称为 所指对象 （referent）。因此，弱引用不会妨碍所指对象被当作垃圾回收。
也就是说，一个对象，只要强引用个数为0，就会触发python的垃圾回收机制，而不管你有多少个弱引用，都是没关系的。
弱引用在缓存应用中很有用，因为不想仅因为被缓存引用着而始终保存缓存对象。
详细介绍见：https://www.cnblogs.com/marsggbo/p/14831456.html
"""


class CarModel:
    """
    1、__new__ 方法创建实例对象供__init__ 方法使用，__init__方法定制实例对象。
    2、__new__ 方法必须返回值，__init__方法不需要返回值。(如果返回非None值就报错)。
    每次根据名字构建新的享元对象时，首先从弱引用字典中查询这一名字。如果存在这个名字，即返回相应型号；
    如果不存在，将会创建一个新名字。
    """
    _models = weakref.WeakValueDictionary()

    def __new__(cls, model_name, *args, **kwargs):
        model = cls._models.get(model_name)
        if not model:
            model = super().__new__(cls)
            cls._models[model_name] = model

        return model

    def __init__(self, model_name, air=False, tilt=False,
                 cruise_control=False, power_locks=False,
                 alloy_wheels=False, usb_charger=False):
        # 确保只有第一次执行__init__时才会进行初始化操作
        if not hasattr(self, "initted"):
            self.model_name = model_name
            self.air = air
            self.tilt = tilt
            self.cruise_control = cruise_control
            self.power_locks = power_locks
            self.alloy_wheels = alloy_wheels
            self.usb_charger = usb_charger
            self.initted = True

    def check_serial(self, serial_number):
        print("sorry, we are unable to check "
              "the serial number {0} on the {1} "
              "at this time".format(serial_number, self.model_name))


class Car:
    def __init__(self, model, color, serial):
        self.model = model
        self.color = color
        self.serial = serial

    def check_serial(self):
        return self.model.check_serial(self.serial)

# 需要在命令行敲出来，直接运行达不到效果
# if __name__ == "__main__":
#     dx = CarModel("FIT DX")
#     lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True, tilt=True)
#     car1 = Car(dx, "blue", "12345")
#     car2 = Car(dx, "black", "12346")
#     car3 = Car(lx, "red", "12347")
#     print(id(lx))
#     del lx
#     del car3
#     import gc
#     print(gc.collect())
#     lx = CarModel("FIT LX", air=True, cruise_control=True, power_locks=True, tilt=True)
#     print(id(lx))
#     lx = CarModel("FIT LX")
#     print(id(lx))
#     print(lx.air)
