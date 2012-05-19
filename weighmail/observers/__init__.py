"""Base observer class for weighmail operations.

"""

class BaseObserver(object):
    """Base observer class; does nothing."""

    def searching(self, label):
        """Called when the search process has started for a label"""
        pass

    def labeling(self, label, count):
        """Called when the labelling process has started for a given label

        label - the label we are working on
        count - number of messages to label
        
        """
        pass

    def done_labeling(self, label, count):
        """Called when finished labelling for a given label

        label - the label we were working on
        count - number of messages that were labelled
        
        """
        pass

    def done(self):
        """Called when completely finished"""
        pass
