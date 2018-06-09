import os

def mover(filename):
    from_dir = "/home/achieveorbit/Desktop/%s" % filename
    to_dir = "/home/achieveorbit/Documents/%s" % filename

    os.rename(from_dir, to_dir)

if __name__ == "__main__":
    mover("test.txt")