import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


class UnparsableOrderException(Exception):
    def __init__(self, input_values):
        self.txt = f"Cant' parse the following elements: {input_values}"


class Order:
    def __init__(self, order_type, order_id, price, volume):
        if (order_type == "B" or order_type == "S") and isinstance(eval(order_id), int) \
                and isinstance(eval(price), int) and isinstance(eval(volume), int):
            self.type = order_type
            self.id = order_id
            self.price = int(price)
            self.volume = int(volume)
        else:
            raise UnparsableOrderException([order_type, order_id, price, volume])

    def get_order(self):
        volume_fmt = locale.format_string('%d', self.volume, True)
        price_fmt = locale.format_string('%d', self.price, True)
        if self.type == 'B':
            return [self.id, volume_fmt, price_fmt]
        else:
            return [price_fmt, volume_fmt, self.id]


class IcebergOrder(Order):
    def __init__(self, order_type, order_id, price, volume, peak_size):
        super().__init__(order_type, order_id, price, volume)
        if isinstance(eval(peak_size), int) and int(peak_size) < self.volume:
            self.peak_size = int(peak_size)
        else:
            raise UnparsableOrderException([order_type, order_id, price, volume, peak_size])

    def get_order(self):
        volume_fmt = locale.format_string('%d', self.volume, True)
        peak_fmt = locale.format_string('%d', self.peak_size, True)
        price_fmt = locale.format_string('%d', self.price, True)
        if self.type == 'B':
            return [self.id, (volume_fmt, peak_fmt)[self.volume > self.peak_size], price_fmt]
        else:
            return [price_fmt, (volume_fmt, peak_fmt)[self.volume > self.peak_size], self.id]
