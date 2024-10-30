"""
Define a class TCP_Segment that contains two points.
Define a set of observers (i.e. oss1, oss2, oss3) interested in the
'too small segment' event.
and another set of observers (i.e. oss1, oss4, oss5) interested in
the 'too big segment' event.

P = (x,t) => x=space t=time
min or max jitter =min or max [ (x2-x1)^2 + (t2-t1)^2 ]^1/2
From Service Level Agreement document you can accept min_threshold and max_threshold as 1 and 10
"""

import copy
import math

class Subscriber: #IoT Object
    def __init__(self, name):
        self._name=name
    """def update1(self, message_from_Publisher): # warning for segmentLength > maxThresh
        print("[SUBSCRIBER, " + str(self._name) + "]: (update method : warning for segmentLength > maxThresh)"
        +"\n" +" Received this : " +message_from_Publisher)
    def update2(self, message_from_Publisher): # warning for segmentLength < minThresh
        print("[SUBSCRIBER, " + str(self._name) + "]: (update method : warning for segmentLength < minThresh)"
              + "\n" + " Received this : " + message_from_Publisher)
        print("The actual jitter is : ") # HOW CAN I PLOT A PUBLISHER ATTRIBUTE ?
        # the response is : in the dispatch method of the Publisher you can call:
        # sub_k.callback_k(self, msg)"""

    def update1(self, pub_obj, message_from_Publisher):  # warning for segmentLength > maxThresh
        print("[SUBSCRIBER, " + str(self._name) + "]: (update method : warning for segmentLength > maxThresh)"
              + "\n" + " Received this : " + message_from_Publisher)
        print("The actual jitter is : " + str(pub_obj.pktLenght))

    def update2(self, pub_obj, message_from_Publisher):  # warning for segmentLength < minThresh
        print("[SUBSCRIBER, " + str(self._name) + "]: (update method : warning for segmentLength < minThresh)"
              + "\n" + " Received this : " + message_from_Publisher)
        print("The actual jitter is : " + str(pub_obj.pktLenght))




class Publisher: # BTS object

    def __init__(self, events_List, firstMeasure, secondMeasure, minThresh=1, maxThresh=10):
        """

        :param events_List: example -> events_List = ["Above_upper_bound_SLA", "Under_lower_bound_SLA"]
        :param firstMeasure: p1 = Point(0,0) # x=0 m [Tx] , t=0 ms [before coder]
        :param secondMeasure: p2 = Point(1000,200) # x=1000 m [Tx] , t=200 ms [post STB processing]
        :param minThresh: min_jitter acceptable
        :param maxThresh: max_jitter acceptable
        """
        #fundamental attributes:
        self._subscriberList = {event_k : dict() for event_k in events_List}

        #adder attributes to the specific context
        self._p1 = copy.copy(firstMeasure)
        self._p2 = copy.copy(secondMeasure)
        self._min = minThresh
        self._max = maxThresh
        # In absolute this is the 1st pkt length init:
        self.pktLenght = self._p1.distance_from_other_point(self._p2)

    # -------- decorator methods
    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @p1.setter
    def p1(self, P1):
        self._p1 = P1
        # a variation had been ==> it must be call dispatch method with pkt upgraded!
        self._pktLenght_change()

    @p2.setter
    def p2(self, P2):
        self._p2 = P2
        # a variation had been ==> it must be call dispatch method with pkt upgraded!
        self._pktLenght_change()


    #-------- protected methods

    # An important constraint is upgrade points and as corrispondence also the distance every time
    # this change must be reflected into packet length segment
    # A change could be enable the trigger (x,t)>maxThresh or (x,t)<minThresh
    # it's necessary to check each time
    def _pktLenght_change(self):
        # new computation :
        self.pktLenght = self._p1.distance_from_other_point(self._p2)

        if self.pktLenght > self._max:
            print('\n [ PUBLISHER ] The pkt had surpassed the maximum delay jitter')
            self.dispatch('Above_upper_bound_SLA','\n [ PUBLISHER ] The pkt had surpassed the maximum delay jitter')
        elif self.pktLenght < self._min:
            print('\n [ PUBLISHER ] The pkt had surpassed the minimum delay jitter')
            self.dispatch('Under_lower_bound_SLA','\n [ PUBLISHER ] The pkt had surpassed the minimum delay jitter')

    def _getSubscriberList(self, event_k):
        """This method return the dict corresponding to the event_k"""
        return self._subscriberList[event_k]

    #-------- observer pattern methods

    def register(self, nameSub, event_k, callback=None):
        """ seen that callback could be emptym it's better to pass as last argument for the Python interpreter"""
        if callback is None:
            callback = getattr(nameSub,'update1')
        #self._subscriberList[event_k][nameSub] = callback
        self._getSubscriberList(event_k)[nameSub] = callback

    def unregister(self, nameSub, event_k):
        del self._getSubscriberList(event_k)[nameSub]

    def dispatch(self, event_k, msg):
        for sub_k , callback_k in self._getSubscriberList(event_k).items():
            callback_k(self, msg) # update1 or update2



class Point(object): #Jitter object
    def __init__(self, axis_1_Value=0,  axis_2_Value=0):
        self.x = axis_1_Value # x is the space between Tx and Rx
        self.y = axis_2_Value # y is the time between two point x1 and x2 with the corrispondence t1 and t2

    def distance_from_other_point(self, p_other):
        # [ (x2-x1)^2 + (t2-t1)^2 ]^1/2
        return math.sqrt( math.pow(self._x - p_other._x, 2) +  math.pow(self._y- p_other._y,2)    )
    # --------------- decorator methods
    # An important constraint is upgrade points and as corrispondence also the distance every time
    # this change must be reflected into packet length segment
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, vx):
        self._x = vx
    @property
    def y(self):
        self._y
    @y.setter
    def y(self, vy):
        self._y = vy

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('\n\n')
    print('------- Measurement of points  and creation .... ------------')
    p11 = Point(0, 0)
    p22 = Point(1000, 200)

    p3 = Point(10, 3)
    p4 = Point(11, 3)

    print("--------- Publisher [BTS] creation ....")
    print('\n\n')
    events_List = ["Above_upper_bound_SLA", "Under_lower_bound_SLA"]
    pub = Publisher(events_List,p11,p22)
    print("------ Little test to current publisher --------")
    print(pub.__dict__)
    print('\n\n')
    print('\n\n')
    print("----------Subscriber [NODEs] creation .... ")
    print('\n\n')
    sub1 = Subscriber('Nicola')
    # Nicola decides to subscribe himself into "above_upp..." event
    pub.register(sub1, 'Above_upper_bound_SLA') #implicit -> update1

    # Gabriele decides to subscribe himself into "under_low..." event
    sub2 = Subscriber('Gabriele')
    pub.register(sub2, 'Under_lower_bound_SLA',sub2.update2)  # explicit -> update2
    print("------ Little test to current subscribers --------")
    print(sub1.__dict__)
    print(sub2.__dict__)
    print('\n\n')
    print("------ Little test to current publisher --------")
    print(pub.__dict__)
    print('\n\n')
    print('\n\n')
    print('------- first change : (false change ...)' ) # ------- first change : (false change ...)
    pub.p1=p11 # it dues a dispatch call
    print('\n\n')
    print('\n\n')
    pub.p2=p22

    print('\n\n')
    print('\n\n')

    pub.p2=p11



"""
output:

\PycharmProjects\exercise_7_Observable_TCP_jitter_delay\venv\Scripts\python.exe C:/Users/39348/PycharmProjects/exercise_7_Observable_TCP_jitter_delay/main.py



------- Measurement of points  and creation .... ------------
--------- Publisher [BTS] creation ....



------ Little test to current publisher --------
{'_subscriberList': {'Above_upper_bound_SLA': {}, 'Under_lower_bound_SLA': {}}, '_p1': <__main__.Point object at 0x000002426ADE1330>, '_p2': <__main__.Point object at 0x000002426ADE12D0>, '_min': 1, '_max': 10, 'pktLenght': 1019.803902718557}






----------Subscriber [NODEs] creation .... 



------ Little test to current subscribers --------
{'_name': 'Nicola'}
{'_name': 'Gabriele'}



------ Little test to current publisher --------
{'_subscriberList': {'Above_upper_bound_SLA': {<__main__.Subscriber object at 0x000002426ADE1420>: <bound method Subscriber.update1 of <__main__.Subscriber object at 0x000002426ADE1420>>}, 'Under_lower_bound_SLA': {<__main__.Subscriber object at 0x000002426ADE1360>: <bound method Subscriber.update2 of <__main__.Subscriber object at 0x000002426ADE1360>>}}, '_p1': <__main__.Point object at 0x000002426ADE1330>, '_p2': <__main__.Point object at 0x000002426ADE12D0>, '_min': 1, '_max': 10, 'pktLenght': 1019.803902718557}






------- first change : (false change ...)

 [ PUBLISHER ] The pkt had surpassed the maximum delay jitter
[SUBSCRIBER, Nicola]: (update method : warning for segmentLength > maxThresh)
 Received this : 
 [ PUBLISHER ] The pkt had surpassed the maximum delay jitter
The actual jitter is : 1019.803902718557







 [ PUBLISHER ] The pkt had surpassed the maximum delay jitter
[SUBSCRIBER, Nicola]: (update method : warning for segmentLength > maxThresh)
 Received this : 
 [ PUBLISHER ] The pkt had surpassed the maximum delay jitter
The actual jitter is : 1019.803902718557







 [ PUBLISHER ] The pkt had surpassed the minimum delay jitter
[SUBSCRIBER, Gabriele]: (update method : warning for segmentLength < minThresh)
 Received this : 
 [ PUBLISHER ] The pkt had surpassed the minimum delay jitter
The actual jitter is : 0.0

Process finished with exit code 0


"""





