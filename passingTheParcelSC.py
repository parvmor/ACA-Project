#!/usr/bin/env python2

import zmq
import sys
import time

def main():
    start=""
    context=zmq.Context()
    subscriber = context.socket(zmq.REP)
    subscriber.bind("tcp://*:9004")
    publisher = context.socket(zmq.REQ)
    publisher.connect("tcp://localhost:9006") 
    if len(sys.argv)==2:
        start=sys.argv[1]
    if start!="":
        print("Starting to pass the number to play the Collatz Conjecture Game.")
        time.sleep(1)
        print("Sending [ %s ]..." % start)
        publisher.send(start)
        temp=publisher.recv()
    collatzNumber=0
    while True:
	if collatzNumber==1:
            print("I have converged to 1.")
            sys.exit()
        message = subscriber.recv()
        collatzNumber=int(message)
        print("Recieved [ %d ]..." % collatzNumber) 
        subscriber.send("Recieved Successfully") 
        if collatzNumber==1:
            print("I have converged to 1.")
            publisher.send(str(collatzNumber))
            sys.exit()
        if collatzNumber%2==0:
            collatzNumber/=2
        else:
            collatzNumber = 3*collatzNumber+1
        if collatzNumber<0:
            print("Impossible event.")
            publisher.send("-1")
            sys.exit()
        print("Sending [ %d ]..." % collatzNumber)
        publisher.send(str(collatzNumber))
        temp=publisher.recv()

if __name__=='__main__':
    main()
