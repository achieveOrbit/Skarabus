#!/usr/bin/python3

import os
import pwd
import signal
from gi.repository import Gtk as gtk 
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

#TODO: Add ability to sort by timestamp rather than file type

indicator_id = 'skarabusindicator'

icon_light = os.path.abspath('icon_light.svg')
icon_dark = os.path.abspath('icon_dark.svg')
light_icon_bool = True


folder_names = ['text_files', 'data_files', 'audio_files', 'video_files', 'model-ing_files', 'raster_files', 
    'vector_files', 'page_files', 'spreadsheet_files', 'database_files', 'executable_files', 'game_files', 'cad_files', 
    'gis_files', 'web_files', 'font_files', 'system_files', 'settings_files', 'encoded_files', 'compressed_files', 'disk_files', 
    'developer_files', 'backup_files', 'misc_files']

file_types = [
    ['doc', 'docx', 'log', 'msg', 'odt', 'pages', 'rtf', 'tex', 'txt', 'wpd', 'wps'],
    ['csv', 'dat', 'ged', 'key', 'keychain', 'pps', 'ppt', 'pptx', 'sdf', 'tar', 'tax2016', 'tax2017', 'vcf', 'xml'],
    ['aif', 'iff', 'm3u', 'm4a', 'mid', 'mp3', 'mpa', 'wav', 'wma'],
    ['3g2', '3gp', 'asf', 'flv', 'm4v', 'mov', 'mp4', 'mpg', 'rm', 'srt', 'swf', 'vob', 'wmv'],
    ['3dm', '3ds', 'max', 'obj'],
    ['bmp', 'dds', 'gif', 'jpg', 'png', 'psd', 'pspimage', 'tga', 'thm', 'tif', 'tiff', 'yuv'],
    ['ai', 'eps', 'ps', 'svg'],
    ['indd', 'pct', 'pdf'],
    ['xlr', 'xls', 'slsx'],
    ['accdb', 'db', 'dbf', 'mdb', 'pdb', 'sql'],
    ['apk', 'app', 'bat', 'cgi', 'com', 'exe', 'gadget', 'jar', 'wsf'],
    ['b', 'dem', 'gam', 'nes', 'rom', 'sav'],
    ['dwg', 'dxf'],
    ['gpx', 'kml', 'kmz'],
    ['aps', 'aspx', 'cer', 'cfm', 'csr', 'css', 'dcr', 'htm', 'html', 'js', 'jsp', 'php', 'rss', 'xhtml'],
    ['fnt', 'fon', 'otf', 'ttf'],
    ['cab', 'cpl', 'cur', 'deskthemepack', 'dll', 'dmp', 'drv', 'icns', 'ico', 'lnk', 'sys'],
    ['cfg', 'ini', 'prf'],
    ['hqx', 'mim', 'uue'],
    ['7z', 'cbr', 'deb', 'gz', 'pkg', 'rar', 'rpm', 'sitx', 'tar', 'zip', 'zipx'],
    ['bin', 'cue', 'dmg', 'iso', 'mdf', 'toast', 'vcd'],
    ['c', 'class', 'cpp', 'cs', 'dtd', 'fla', 'h', 'java', 'lua', 'm', 'pl', 'py', 'sh', 'sln', 'swift', 'vb', 'vcxproj', 'xcodeproj'],
    ['bak', 'tmp'],
    ['crdownload', 'ics', 'msi', 'part', 'torrent'],
]

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
            for x in range (0, len(folder_names)):
                if filename.split('.')[1] in file_types[x]:
                    if os.path.isdir(documents_dir + '/' + folder_names[x]):
                        mover(folder_names[x], filename)
                    else:
                        os.makedirs(documents_dir + '/' + folder_names[x])
                        print("Created %s folder..." % folder_names[x])
                        mover(folder_names[x], filename)
                    print("Moved file %s..." % filename)
    notification('Skarabus is happy', 'All your dong has been rolled...')


def menu_builder():
    menu = gtk.Menu()

    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    item_sort = gtk.MenuItem('Roll all the dung')
    item_sort.connect('activate', file_looper)
    item_icon_changer = gtk.MenuItem('Switch icon')
    item_icon_changer.connect('activate', icon_switcher)
    
    menu.append(item_sort)
    menu.append(item_icon_changer)
    menu.append(item_quit)
    menu.show_all()

    return menu


def icon_switcher(self):
    global light_icon_bool

    if light_icon_bool:
        indicator.set_icon(icon_dark)
        light_icon_bool = False
    else:
        indicator.set_icon(icon_light)


def notification(title, text):
    notify.Notification.new(title, text, None).show()
    #TODO: Add a timer to see how long it took


def quit(source):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL) # makes the app react to CTRL + C

    notify.init(indicator_id)

    indicator = appindicator.Indicator.new(indicator_id, icon_light, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu_builder())

    gtk.main()
    