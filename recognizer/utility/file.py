import os


def read(path):
    file = open(path, 'r')
    lines = file.readlines()
    file.close()
    return lines

    # lines = []
    # if file.mode == 'r':
    #     data = file.read();
    #     return data

    # return ''


def write(path, flag, data):
    file = open(path, flag)
    file.write(data)
    file.close()


def write_a(path, data):
    if os.path.exists(path):
        flag = 'a'
    else:
        flag = 'w'

    write(path, flag, data)


def write_w(path, data):
    write(path, 'w', data)
