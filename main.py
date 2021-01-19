import input
from order_book import OrderBook

book = OrderBook()
while True:
    order = input.read_string()
    if order != None:
        book.proc(order)