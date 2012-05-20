import datetime

from . import BaseObserver

class ConsoleObserver(BaseObserver):
    """Console observer class; outputs status to the console."""

    def __init__(self, *args, **kwargs):
        super(BaseObserver, self).__init__(*args, **kwargs)
        self.first_callback = True
        self.total_messages = 0

    def searching(self, label):
        if self.first_callback:
            self.first_callback = False
            self.start_time = datetime.datetime.now()

        print "Searching for %s messages..." % label

    def labeling(self, label, count):
        print "Applying the label %s to %d messages..." % (label, count)

    def done_labeling(self, label, count):
        self.total_messages += count

    def done(self):
        duration = datetime.datetime.now() - self.start_time
        print "Labeled %d messages in %s" % (self.total_messages, duration)
        print "Done."
