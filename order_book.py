import sys

from prettytable import PrettyTable

from orders import Order, IcebergOrder


class OrderBook:
    def __init__(self):
        self.sell_queue = []
        self.buy_queue = []

    def display_state(self):
        table = PrettyTable()
        table.field_names = ['1', '2', '3', '4', '5', '6']
        sell = len(self.sell_queue)
        buy = len(self.buy_queue)
        for i in range(min(sell, buy)):
            table.add_row(self.buy_queue[i].get_order() + self.sell_queue[i].get_order())
        if buy > sell:
            for i in range(sell, buy):
                table.add_row(self.buy_queue[i].get_order() + ['', '', ''])
        elif buy < sell:
            for i in range(buy, sell):
                table.add_row(['', '', ''] + self.sell_queue[i].get_order())

        table.align = "r"
        table.header = False
        table._min_width = {'1': 10, '2': 13, '3': 7, '4': 7, '5': 13, '6': 10}
        table.padding_width = 0
        header = '+' + '-' * 65 + '+\n| BUY' + ' ' * 28 + '| SELL' + ' ' * 27 + \
                 '|\n| Id       | Volume      | Price | Price | Volume      | Id       |\n'

        print(header + table.get_string())

    @staticmethod
    def proc_order_execution(order_pass, order_act):
        volume = min(order_pass.volume, order_act.volume)
        buy_id = order_pass.id if order_pass.type == "B" else order_act.id
        sell_id = order_pass.id if order_pass.type == "S" else order_act.id
        price = order_pass.price
        print('{0},{1},{2},{3}'.format(buy_id, sell_id, price, volume))
        order_pass.volume = max(0, order_pass.volume - volume)
        order_act.volume = max(0, order_act.volume - volume)

    def is_id_presented(self, new_id):
        a = True in (x.id == new_id for x in self.sell_queue)
        b = True in (x.id == new_id for x in self.buy_queue)
        print(a)
        print(b)
        res = a or b
        print(res)
        return res

    def proc(self, order):
        if self.is_id_presented(order):
            sys.stderr.write("Duplicated ID")
            return
        if order.type == "B":
            while (len(self.sell_queue) > 0 and self.sell_queue[0].price <= order.price) and (order.volume > 0):
                self.proc_order_execution(self.sell_queue[0], order)
                if self.sell_queue[0].volume == 0:
                    self.sell_queue.pop(0)
            if order.volume > 0:
                self.buy_queue.append(order)
                self.buy_queue.sort(key=lambda x: x.price, reverse=True)
        else:
            while (len(self.buy_queue) > 0 and self.buy_queue[0].price >= order.price) and (order.volume > 0):
                self.proc_order_execution(self.buy_queue[0], order)
                if self.buy_queue[0].volume == 0:
                    self.buy_queue.pop(0)
            if order.volume > 0:
                self.sell_queue.append(order)
                self.sell_queue.sort(key=lambda x: x.price)
        self.display_state()


if __name__ == "__main__":
    ob = OrderBook()
    ob.sell_queue.append(Order('S', '1231', '1000', '10'))
    ob.sell_queue.append(Order('S', '1232', '1010', '5'))
    ob.sell_queue.append(Order('S', '1233', '1020', '8'))
    ob.sell_queue.append(Order('S', '1234', '1234', '2'))
    ob.sell_queue.append(IcebergOrder('S', '1235', '1010', '100000', '1000'))
    ob.buy_queue.append(Order('B', '1236', '990', '7'))
    ob.buy_queue.append(Order('B', '1237', '980', '3'))
    ob.buy_queue.append(IcebergOrder('B', '1238', '950', '100', '10'))
    ob.buy_queue.append(IcebergOrder('B', '1238', '940', '500', '10'))
    ob.display_state()
