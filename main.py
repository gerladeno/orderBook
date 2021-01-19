from input import read_string
from order_book import OrderBook

book = OrderBook()
while True:
    order = read_string()
    if order:
        book.proc_new_order(order)
