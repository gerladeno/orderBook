from prettytable import PrettyTable
from input import read_string
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
            tmp = self.sell_queue[i].get_order()
            table.add_row(self.buy_queue[i].get_order() + self.sell_queue[i].get_order())
        if buy > sell:
            for i in range(sell, buy):
                table.add_row(self.buy_queue[i].get_order() + ['', '', ''])
        elif buy < sell:
            for i in range(buy, sell):
                table.add_row(['', '', ''] + self.sell_queue[i].get_order())

        table.align = "r"
        table.header = False
        table._min_width = {'1': 8, '2': 11, '3': 5, '4': 5, '5': 11, '6': 8}
        header = '+' + '-' * 65 + '+\n| BUY' + ' ' * 28 + '| SELL' + ' ' * 27 + \
                 '|\n| Id       | Volume      | Price | Price | Volume      | Id       |\n'

        print(header + table.get_string())

    def proc_one(self, order_pass, order_act):
        volume = min(order_pas.volue, order_act.volume)
        buy_id = order_pass.id if order_pass.type == "B" else order_act.id
        sell_id = order_pass.id if order_pass.type == "S" else order_act.id
        price = order_pass.price
        print ('{0},{1},{2},{3}'.format(buy_id, sell_id, price, volume))
        order_pass.volume = max(0, order_pass.volume - volume)
        order_act.volume = max(0, order_act.volume - volume)
    
    def proc_queue(self, queue, order, other_queue):
        while (self.queue[0].price <= order.price) and (order.volume > 0):
            self.proc_one(queue[0], order)
            if queue[0].volume == 0:
                queue[0].pop()
        if order.volume > 0:
            self.other_queue.append(order)
            self.other_queue.sort()
    
    def proc(self, order):
        if order.type == "B":
            self.proc_queue(self.sell_queue, order, self.buy_queue)
        else:
            self.proc_queue(self.buy_queue, order, self.sell_queue)

if __name__ == "__main__":
    ob = OrderBook()
    ob.sell_queue.append(Order('S', '1231', '1000', '10'))
    ob.sell_queue.append(Order('S', '1232', '1010', '5'))
    ob.sell_queue.append(Order('S', '1233', '1020', '8'))
    ob.sell_queue.append(Order('S', '1234', '1000', '2'))
    ob.sell_queue.append(IcebergOrder('S', '1235', '1010', '100', '10'))
    ob.buy_queue.append(Order('B', '1236', '990', '7'))
    ob.buy_queue.append(Order('B', '1237', '980', '3'))
    ob.buy_queue.append(IcebergOrder('B', '1238', '950', '100', '10'))
    ob.buy_queue.append(IcebergOrder('B', '1238', '940', '500', '10'))
    ob.display_state()
