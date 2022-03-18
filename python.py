from time import sleep
from repeater import RepeatedTimer

def hello(name):
    print("Hello %s!" % name)

print("starting...")
rt =  RepeatedTimer(1,hello , "World") # it auto-starts, no need of rt.start()
try:
    sleep(10) # your long-running job goes here...
    print('en el try')
finally:
    print('en el finally')
    rt.stop()