import sys

from orders import Order, IcebergOrder, UnparsableOrderException


def read_string():
    input_string = input()
    order = input_string.split(',')
    try:
        if (len(input_string)) and (input_string[0] != ' ') and (input_string[0] != '#'):
            if len(order) == 4:
                return Order(*order)
            elif len(order) == 5:
                return IcebergOrder(*order)
            else:
                raise UnparsableOrderException(*order)
        order = input_string.replace(' ', '')
        if (order == '') or (order[0] == '#'):
            return None
        else:
            raise UnparsableOrderException(*order)
    except UnparsableOrderException as err:
        sys.stderr.write(err.txt)
        return None


if __name__ == "__main__":
    read_string()
