from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import DrivingMode, Control
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender
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
                print('Auto mode')
                # Check new images from the camera
                # TODO!

                # Send output
                try:
                    message = {
                        "Time": 1,
                        "Speed": 100,
                        "Steer": 15
                    }
                    self.controlSender.send(message)
                    print('Auto action sent')
                except Exception as e:
                    print(e)



    
