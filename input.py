import re
import sys

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
        sys.stderr.write(err.txt)
        return None


if __name__ == "__main__":
    pass
    # d = {0: 234234, 1: 23, 3: 99}

# adsasdas ads hdaksjdhag sldj hbaslkddas# sdkjfh sdkjfsf89 43 3oi43
# B,12312,312312,41541234,342 #dffkvcjdnfvd
