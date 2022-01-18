class Property:
    """
    基础属性类
    """

    def __init__(self, square_feet='', beds='', baths='', **kwargs):
        super().__init__(**kwargs)  # 防止不是在继承链的最后一层被调用
        print("the kwargs in property: ", kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths

    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()

    def prompt_init():
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms: "),
                    baths=input("Enter number of baths: "))

    prompt_init = staticmethod(prompt_init)


def get_valid_input(input_string, valid_options):
    input_string += "({})".format(" ,".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


class Apartment(Property):
    """
    继承基础属性类，构建公寓类
    介绍公寓的基础属性，例如：阳台、洗衣机（投币或者配套）
    """
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s" % self.laundry)
        print("has balcony: %s" % self.balcony)
        print()

    def prompt_init():
        parent_init = Property.prompt_init()  # 类函数只能通过类来进行调用，不能通过对象调用
        laundry = get_valid_input("What laundry facilities does the property have?", Apartment.valid_laundries)
        balcony = get_valid_input("Does the property have a balcony?", Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return parent_init

    prompt_init = staticmethod(prompt_init)


class House(Property):
    """
    继承基础属性类，构建房子类
    介绍房子的基础属性，例如：围墙、车库、楼层
    """
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories='', garage='', fenced='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))
        print()

    def prompt_init():
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced?", House.valid_fenced)
        garage = get_valid_input("Is there is a garage?", House.valid_garage)
        num_stories = input("How many stories?")

        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        return parent_init

    prompt_init = staticmethod(prompt_init)


class Purchase:
    """
    购买房屋
    展示出价格和纳税
    """

    def __init__(self, price='', taxes='', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))
        print()

    def prompt_init():
        return dict(
            price=input("What is the selling price?"),
            taxes=input("What are the estimated taxes?")
        )

    prompt_init = staticmethod(prompt_init)


class Rental:
    """
    出租房屋，展示租金、配套家具、水电费等
    """

    def __init__(self, furnished='', utilities='', rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities

    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished: {}".format(self.furnished))
        print()

    def prompt_init():
        return dict(
            rent=input("What is the monthly rent? "),
            utilities=input("What are the estimated utilities? "),
            furnished=get_valid_input("Is the property furnished? ", ("yes", "no"))
        )

    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):
    """
    组合房屋类和出租类，实现房屋出租功能
    """

    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init

    prompt_init = staticmethod(prompt_init)


class ApartmentRental(Rental, Apartment):
    """
    组合公寓类和出租类，实现公寓出租
    先放Rental，再放Apartment，因为
    先super rental 再是 Apartment，再是基类
    多重继承的性质，其他几个类类似
    """

    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init

    prompt_init = staticmethod(prompt_init)


class ApartmentPurchase(Purchase, Apartment):
    """
    同上
    """

    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init

    prompt_init = staticmethod(prompt_init)


class HousePurchase(Purchase, House):
    """
    同上
    """

    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init

    prompt_init = staticmethod(prompt_init)


class Agent:
    """
    房屋中介
    负责创建新的项目以及展示已存在的项目
    """
    # 构建一个类变量
    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def __init__(self):
        self.property_list = []

    def display_properties(self):
        for property_ in self.property_list:
            property_.display()

    def add_property(self):
        property_type = get_valid_input("What type of property? ",
                                        ("house", "apartment")).lower()
        payment_type = get_valid_input("What payment type? ",
                                       ("purchase", "rental")).lower()
        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))