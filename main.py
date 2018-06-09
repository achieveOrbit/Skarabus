#!/usr/bin/python3

import os
import pwd

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


if __name__ == "__main__":
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

