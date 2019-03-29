from progressbar import ProgressBar, Bar, Percentage, ETA, FileTransferSpeed

class progress_bar_mine:
    widgets = [Bar(marker='=',left='[',right=']')]
    progress_bar = ProgressBar(widgets=widgets, maxval=100)
    
    def __init__(self, max_val, widgets=[Bar(marker='=',left='[',right=']'), ' ', Percentage(), ' ', ETA(), ' ', FileTransferSpeed()]):
        self.widgets = widgets
        self.progress_bar = ProgressBar(widgets=widgets, maxval=max_val)
    def start(self):
        self.progress_bar.start()
    def update(self, i):
        self.progress_bar.update(int(i))
    def finish(self):
        self.progress_bar.finish()