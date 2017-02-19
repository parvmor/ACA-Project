#!/usr/bin/env python2

import zmq
import sys
import time

def main():
    start=""
    context=zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:9004")
    for i in range(10):
        subscriber.setsockopt(zmq.SUBSCRIBE,str(i)) 
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:9006") 
    if len(sys.argv)==2:
        start=sys.argv[1]
    if start!="":
        print("Starting to pass the number to play the Collatz Conjecture Game.")
        time.sleep(1)
        publisher.send(start)
    collatzNumber=0
    while True:
        message = subscriber.recv()
        collatzNumber=int(message)
        print("Recieved [ %d ]..." % collatzNumber) 
        if collatzNumber==1:
            print("I have converged to 1.")
            publisher.send(str(collatzNumber))
            sys.exit()
        elif collatzNumber%2==0:
            collatzNumber/=2
        else:
            collatzNumber = 3*collatzNumber+1
        if collatzNumber<0:
            print("Impossible event.")
            publisher.send("-1")
            sys.exit()
        print("Sending [ %d ]..." % collatzNumber)
        publisher.send(str(collatzNumber))

if __name__=='__main__':
    main()
