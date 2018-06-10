#!/usr/bin/python3

import os
import pwd
import signal
from gi.repository import Gtk as gtk 
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


indicator_id = 'skarabusindicator'


text_files = ['doc', 'docx', 'log', 'msg', 'odt', 'pages', 'rtf', 'tex', 'txt', 'wpd', 'wps']
data_files = ['csv', 'dat', 'ged', 'key', 'keychain', 'pps', 'ppt', 'pptx', 'sdf', 'tar', 'tax2016', 'tax2017', 'vcf', 'xml']
audio_files = ['aif', 'iff', 'm3u', 'm4a', 'mid', 'mp3', 'mpa', 'wav', 'wma']
video_files = ['3g2', '3gp', 'asf', 'flv', 'm4v', 'mov', 'mp4', 'mpg', 'rm', 'srt', 'swf', 'vob', 'wmv']
#TODO: Add more filetypes -> https://fileinfo.com/filetypes/common

username = pwd.getpwuid(os.getuid())[0]

desktop_dir = "/home/%s/Desktop/" % username
documents_dir = "/home/%s/Documents/" % username


def mover(folder, filename):
    from_dir = desktop_dir + filename
    to_dir = documents_dir + folder + "/" + filename

    os.rename(from_dir, to_dir)


def file_looper(self):
    if not os.listdir(desktop_dir):
        notification('Skarabus is bored', 'There was nothing for him to do...')
    else:
        for filename in os.listdir(desktop_dir):
            if filename.split('.')[1] in text_files: # Text files
                try:
                    mover("Text_Files", filename)
                except FileNotFoundError:
                    os.makedirs(documents_dir + "Text_Files")
                    print("Created Text_Files folder...")
                    mover("Text_Files", filename)
                print("Moved file %s..." % filename)
            elif filename.split('.')[1] in data_files: # Data files
                try:
                    mover("Data_Files", filename)
                except FileNotFoundError:
                    os.makedirs(documents_dir + "Data_Files")
                    print("Created Data_Files folder...")
                    mover("Data_Files", filename)
                print("Moved file %s..." % filename)
            elif filename.split('.')[1] in audio_files: # Audio files
                try:
                    mover("Audio_Files", filename)
                except FileNotFoundError:
                    os.makedirs(documents_dir + "Audio_Files")
                    print("Created Audio_Files folder...")
                    mover("Audio_Files", filename)
                print("Moved file %s..." % filename)
            elif filename.split('.')[1] in video_files: # Video files
                try:
                    mover("Video_Files", filename)
                except FileNotFoundError:
                    os.makedirs(documents_dir + "Video_Files")
                    print("Created Video_Files folder...")
                    mover("Video_Files", filename)
                print("Moved file %s..." % filename)
        notification('Skarabus is happy', 'All your dong has been rolled...')


def menu_builder():
    menu = gtk.Menu()

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    item_sort = gtk.MenuItem('Roll all the dung')
    item_sort.connect('activate', file_looper)
    
    menu.append(item_sort)
    menu.append(item_quit)
    menu.show_all()

    return menu


def notification(title, text):
    notify.Notification.new(title, text, None).show()
    #TODO: Add a timer to see how long it took


def quit(source):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL) # makes the app react to CTRL + C

    notify.init(indicator_id)

    indicator = appindicator.Indicator.new(indicator_id, os.path.abspath('icon.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu_builder())

    gtk.main()
    