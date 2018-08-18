class EventLoop:
    def __init__(self):
        self.subs = {}

    def sub(self, event, handler):
        if not event in self.subs:
            self.subs[event] = []
        self.subs[event].append(handler)

    def send(self, event, payload=None):
        if event in self.subs:
            for sub in self.subs[event]:
                sub(payload)
