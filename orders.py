class UnparsableOrderException(Exception):
    def __init__(self, input_values):
        self.txt = f"Cant' parse the following elements: {input_values}"


class Order:
    def __init__(self, order_type, order_id, price, volume):
        if (order_type == "B" or order_type == "S") and isinstance(eval(order_id), int) \
                and isinstance(eval(price), int) and isinstance(eval(volume), int):
            self.type = order_type
            self.id = order_id
            self.price = price
            self.volume = volume
        else:
            raise UnparsableOrderException([order_type, order_id, price, volume])


class IcebergOrder(Order):
    def __init__(self, order_type, order_id, price, volume, peak_size):
        super().__init__(order_type, order_id, price, volume)
        if isinstance(eval(peak_size), int) and peak_size < self.volume:
            self.peak_size = peak_size
        else:
            raise UnparsableOrderException([order_type, order_id, price, volume, peak_size])
