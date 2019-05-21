from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

class progress_bar_mine:
    progress_bar = ProgressBar(widgets=[Bar(marker='=',left='[',right=']')], maxval=100)
    
    def __init__(self, max_val, widgets=None, percentage=True, eta=True, transfer_speed=True):
        if widgets == None:
            widgets = [Bar(marker='=',left='[',right=']')]
        if percentage:
            widgets.append(' ')
            widgets.append(Percentage())
        if eta:
            widgets.append(' ')
            widgets.append(ETA())
        if transfer_speed:
            widgets.append(' ')
            widgets.append(FileTransferSpeed())
        self.progress_bar = ProgressBar(widgets=widgets, maxval=max_val)
    def start(self, label=None):
        if label:
            print('// ---------- ' + label + ' ---------- \\\\')
        self.progress_bar.start()
    def update(self, i):
        self.progress_bar.update(int(i))
    def finish(self):
        self.progress_bar.finish()