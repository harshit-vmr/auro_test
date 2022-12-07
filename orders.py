import xml.etree.ElementTree as ET
import time
import sys
import os
import argparse
from collections import OrderedDict


#Will create a class for storing order Info and their methods
class OrderBook:
    def __init__(self, book):
        self.book = book
        self.buy = OrderedDict()
        self.sell = OrderedDict()
        
    #print format for the class
    def __str__(self):
        return "Buy {0}\nSell {1}".format(self.buy, self.sell)

    def delete_order(self, order):
        if order.operation == "BUY":
            if order.price in self.buy:
                for i, o in enumerate(self.buy[order.price]):
                    if o.orderId == order.orderId:
                        del self.buy[order.price][i]
                        break
        elif order.operation == "SELL":
            if order.price in self.sell:
                for i, o in enumerate(self.sell[order.price]):
                    if o.orderId == order.orderId:
                        del self.sell[order.price][i]
                        break
    
    def add_order(self, order):
        if order.operation == "BUY":
            if order.price in self.buy:
                self.buy[order.price].append(order)
            else:
                self.buy[order.price] = [order]
        elif order.operation == "SELL":
            if order.price in self.sell:
                self.sell[order.price].append(order)
            else:
                self.sell[order.price] = [order]

        


class Order:
    def __init__(self, operation, book, price, volume, orderId):
        self.operation = operation
        self.book = book
        self.price = price
        self.volume = volume
        self.orderId = orderId

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.operation, self.book, self.price, self.volume, self.orderId)




def parse_order(order):
    perfom = order.get("operation")
    book = order.get("books")
    if order.get("price") is None:
        price = 0
    else:
        price = float(order.get("price"))
    if order.get("volume") is None:
        volume = 0
    else:
        volume = order.get("volume")
    order_id = order.get("orderId")
    return Order(perfom, book, price, volume, order_id)


def read_order(order, order_books):
    if order.book not in order_books:
        order_books[order.book] = OrderBook(order.book)
    if order.operation == "AddOrder":
        order_books[order.book].add_order(order)
    elif order.operation == "DeleteOrder":
        order_books[order.book].delete_order(order)


def main():

    getparsed = ET.parse('orders.xml')
    root = getparsed.getroot()

    all_books = {}
    for i in root:
        j = parse_order(i)
        read_order(j, all_books)

    for book, order_book in order_books.items():
        print(book)
        print(order_book)


if __name__ == "__main__":
    main()
