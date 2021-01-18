import re

from orders import Order, IcebergOrder, UnparsableOrderException


def read_string():
    input_string = input()
    order = re.sub('#.*', '', input_string).replace(' ', '').split(',')
    try:
        if len(order) == 0:
            return None
        elif len(order) == 4:
            return Order(*order)
        elif len(order) == 5:
            return IcebergOrder(*order)
        else:
            raise UnparsableOrderException(*order)
    except UnparsableOrderException as err:
        # write to stderr
        print(err.txt)
        return None


if __name__ == "__main__":
    print(read_string())

# adsasdas ads hdaksjdhag sldj hbaslkddas# sdkjfh sdkjfsf89 43 3oi43
# B,12312,312312,41541234,342 #dffkvcjdnfvd
