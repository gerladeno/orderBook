import sys

from prettytable import PrettyTable

from orders import Order


class OrderBook:
    def __init__(self):
        self.sell_queue = []
        self.buy_queue = []
        self.order_counter = 0

    def display_state(self):
        if not (self.sell_queue or self.buy_queue):
            print('Order book is empty')
        else:
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
    def proc_order_execution(orders, order_act):
        deal_volume = 0
        if (len(orders) > 1) and (orders[0].price == orders[1].price):
            deal_volume = min(orders[0].peak_size, order_act.volume)
        else:
            deal_volume = min(orders[0].volume, order_act.volume)

        buy_id = orders[0].id if orders[0].type == "B" else order_act.id
        sell_id = orders[0].id if orders[0].type == "S" else order_act.id
        price = orders[0].price
        print('{0},{1},{2},{3}'.format(buy_id, sell_id, price, deal_volume))
        orders[0].volume = max(0, orders[0].volume - deal_volume)
        order_act.volume = max(0, order_act.volume - deal_volume)

    def is_id_presented(self, new_id):
        a = True in (x.id == new_id for x in self.sell_queue)
        b = True in (x.id == new_id for x in self.buy_queue)
        return a or b

    def update_counter(self, order):
        order.time = self.order_counter
        self.order_counter = self.order_counter + 1

    def proc_new_order(self, order):
        if self.is_id_presented(order.id):
            sys.stderr.write(f"Duplicate ID: {order.id}, order skipped\n")
            return
        self.update_counter(order)
        orders = self.buy_queue
        orders_opposite = self.sell_queue
        if order.type == "B":
            orders = self.sell_queue
            orders_opposite = self.buy_queue

        while (len(orders) > 0 and orders[0].price <= order.price) and (order.volume > 0):
            self.proc_order_execution(orders, order)
            if orders[0].volume == 0:
                orders.pop(0)
            else:
                self.update_counter(orders[0])
        if order.volume > 0:
            orders_opposite.append(order)
        self.buy_queue.sort(key=lambda x: (x.price, -x.time), reverse=True)
        self.sell_queue.sort(key=lambda x: (x.price, x.time))
        self.display_state()


if __name__ == "__main__":
    ob = OrderBook()
    ob.sell_queue.append(Order('S', '1231', '1000', '10'))
    ob.sell_queue.append(Order('S', '1232', '1010', '5'))
    ob.sell_queue.append(Order('S', '1233', '1020', '8'))
    ob.sell_queue.append(Order('S', '1234', '1234', '2'))
    ob.sell_queue.append(Order('S', '1235', '1010', '100000', '1000'))
    ob.buy_queue.append(Order('B', '1236', '990', '7'))
    ob.buy_queue.append(Order('B', '1237', '980', '3'))
    ob.buy_queue.append(Order('B', '1238', '950', '100', '10'))
    ob.buy_queue.append(Order('B', '1238', '940', '500', '10'))
    ob.display_state()
