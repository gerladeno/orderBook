import sys

from orders import Order, IcebergOrder, UnparsableOrderException


def read_string():
    input_string = input()
    order = input_string.split(',')
    try:
        if (input_string[0] != ' ') and (input_string[0] != '#'):
            if len(order) == 4:
                return Order(*order)
            elif len(order) == 5:
                return IcebergOrder(*order)
            else:
                raise UnparsableOrderException(*order)
        order = input_string.replace(' ', '')
        if order[0] == '#':
            return None
        else:
            raise UnparsableOrderException(*order)
    except UnparsableOrderException as err:
        sys.stderr.write(err.txt)
        return None


if __name__ == "__main__":
    read_string()
    # d = {0: 234234, 1: 23, 3: 99}

# adsasdas ads hdaksjdhag sldj hbaslkddas# sdkjfh sdkjfsf89 43 3oi43
# B,12312,312312,41541234,342 #dffkvcjdnfvd
