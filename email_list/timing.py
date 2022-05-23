import datetime
import time

"""
函数也是对象，可以四处传递供以后调用
回调函数
"""


class TimedEvent:
    def __init__(self, end_time, callback):
        self.end_time = end_time
        self.callback = callback

    def ready(self):
        return self.end_time <= datetime.datetime.now()


class Timer:
    def __init__(self):
        self.events = []

    def call_after(self, delay, callback):
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=delay)
        self.events.append(TimedEvent(end_time, callback))

    def run(self):
        while True:
            ready_events = (e for e in self.events if e.ready())
            for event in ready_events:
                event.callback(self)
                self.events.remove(event)
            time.sleep(0.5)


def format_time(message, *args):
    now = datetime.datetime.now().strftime("%I:%M:%S")
    print(message.format(*args, now=now))


def one(Timer):
    format_time("{now}: Called one")


def two(Timer):
    format_time("{now}: Called two")


def three(Timer):
    format_time("{now}: Called three")


class Repeater:
    def __init__(self):
        self.count = 0

    def repeater(self, Timer):
        format_time("{now}: repeat {0}", self.count)
        self.count += 1
        timer.call_after(5, self.repeater)


timer = Timer()
timer.call_after(1, one)
timer.call_after(2, one)
timer.call_after(2, two)
timer.call_after(4, two)
timer.call_after(3, three)
timer.call_after(6, three)
repeater = Repeater()
timer.call_after(5, repeater.repeater)
format_time("{now}: Starting")
timer.run()
