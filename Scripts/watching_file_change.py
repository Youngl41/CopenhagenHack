#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 12:23:44 2018

@author: mia
"""

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

class Watcher:
    DIRECTORY_TO_WATCH = '/Users/Hackathon/CopenhagenHack/Working/'

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print ("Received created event - %s." % event.src_path )
            print('hello new file')

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print ("Received modified event - %s." % event.src_path)
            
            


if __name__ == '__main__':
    w = Watcher()
    w.run()