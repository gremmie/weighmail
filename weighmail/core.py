

def weighmail(imap, folder, labels, observer=None):
    """Applies labels to message that meet size criteria.

    imap - IMAPClient
    folder - folder name to operate on
    labels - list of Label tuples
    observer - will call back to report progress

    """
    imap.select_folder(folder)

    for label in labels:
        apply_label(imap, label, observer)

    if observer is not None:
        observer.done()


def get_criteria(label):
    """Returns the RFC 3501 criteria string for the given label"""

    l = 'LARGER %d' % label.min if label.min is not None else ''
    s = 'SMALLER %d' % label.max if label.max is not None else ''

    return '{larger} {smaller}'.format(larger=l, smaller=s).strip()


def apply_label(imap, label, observer=None):
    """Searches for messages that meet the label's criteria and applies the
    label to them.

    """
    criteria = get_criteria(label)

    if observer is not None:
        observer.searching(label.name)

    msgs = imap.search(criteria)

    if len(msgs) > 0:
        if observer is not None:
            observer.labeling(label.name, len(msgs))

        imap.add_gmail_labels(msgs, [label.name])

        if observer is not None:
            observer.done_labeling(label.name, len(msgs))
