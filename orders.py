class UnparsableOrderException(Exception):
    def __init__(self, input_values):
        self.txt = f"Can't parse the following elements: {input_values}, entry skipped\n"


class Order:
    def __init__(self, order_type, order_id, price, volume, peak=-1):
        if (order_type == "B" or order_type == "S") and isinstance(eval(order_id), int) \
                and isinstance(eval(price), int) and isinstance(eval(volume), int):
            self.type = order_type
            self.id = order_id
            self.price = int(price)
            self.volume = int(volume)
            self.peak_size = int(volume) if int(peak) == -1 else int(peak)
            self.time = 0
        else:
            raise UnparsableOrderException([order_type, order_id, price, volume])

    def get_order(self):
        volume_fmt = f"{min(self.volume, self.peak_size):,}"
        price_fmt = f"{self.price:,}"
        if self.type == 'B':
            return [self.id, volume_fmt, price_fmt]
        else:
            return [price_fmt, volume_fmt, self.id]