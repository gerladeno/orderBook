import sys

from orders import Order, UnparsableOrderException


def read_string():
    input_string = input()
    order = input_string.split(',')
    try:
        if (len(input_string)) and (input_string[0] != ' ') and (input_string[0] != '#'):
            if len(order) == 4 or len(order) == 5:
                return Order(*order)
            else:
                raise UnparsableOrderException(order)
        input_string = input_string.replace(' ', '')
        if (input_string == '') or (input_string[0] == '#'):
            return None
        else:
            raise UnparsableOrderException(input_string)
    except UnparsableOrderException as err:
        sys.stderr.write(err.txt)
        return None


if __name__ == "__main__":
    read_string()
