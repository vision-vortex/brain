from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import DrivingMode, Control
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
import time
class threadLaneDetector(ThreadWithStop):
    """This thread handles LaneDetector.
    Args:
        queueList (dictionary of multiprocessing.queues.Queue): Dictionary of queues where the ID is the type of messages.
        logging (logging object): Made for debugging.
        debugging (bool, optional): A flag for debugging. Defaults to False.
    """

    def __init__(self, queueList, logging, debugging=False):
        super(threadLaneDetector, self).__init__()
        self.queuesList = queueList
        self.logging = logging
        self.debugging = debugging
        self.mode = 'stop'
        self.subscribe()
        self.controlSender = messageHandlerSender(self.queuesList, Control)

        # Test code
        self.i = 0
        self.instructions = [
            {
                'Time': 10,
                'Speed': 100,
                'Steer': 0
            },
            {
                'Time': 10,
                'Speed': 100,
                'Steer': -20
            },
            {
                'Time': 10,
                'Speed': 100,
                'Steer': 0
            },
            {
                'Time': 10,
                'Speed': 100,
                'Steer': 20
            },
        ]

    def subscribe(self):
        """Subscribes to the messages you are interested in"""
        self.drivingModeSubscriber = messageHandlerSubscriber(
            self.queuesList, DrivingMode, "lastOnly", True
        )

    def run(self):
        while self._running:
            # Check if a new mode is set
            try:
                drivingModeRecv = self.drivingModeSubscriber.receive()
                if drivingModeRecv is not None: 
                    self.mode = str(drivingModeRecv)
            except Exception as e:
                print(e)

            if self.mode == 'auto':
                # Check new images from the camera
                # TODO!

                # Send output
                try:
                    '''message = {
                        "Time": 10,
                        "Speed": 100,
                        "Steer": 15
                    }'''
                    message = self.instructions[self.i]
                    time.sleep(self.instructions[self.i]['Time'] / 10)
                    self.i = (self.i + 1) % len(self.instructions)
                    self.controlSender.send(message)
                except Exception as e:
                    print(e)
            elif self.mode == 'stop':
                try:
                    message = {
                        "Time": 0,
                        "Speed": 0,
                        "Steer": 0
                    }
                    self.controlSender.send(message)
                except Exception as e:
                    print(e)



    
