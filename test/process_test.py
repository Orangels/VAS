import time
from multiprocessing import Process, Queue, Pool, Manager
import os

path = '/Users/liusen/Documents/sz/智慧工地/Vas/test/test_seg.png'

def read_q(q_file, q_name):
    while True:
        if q_file.empty() and q_name.empty():
            file = q_file.get(True)
            name = q_name.get(True)
            print('file -- {}'.format(file))
            print('name -- {}'.format(name))


def write_q(q_file, q_name):
    num = 0
    while True:
        if q_file.empty() and q_name.empty():
            q_file.put(num)
            q_name.put(num)
        num += 1
        time.sleep(1)


if __name__ == '__main__':
    q_file = Queue()
    q_name = Queue()

    pw_1 = Process(target=read_q, args=(q_file, q_name))
    pr = Process(target=write_q, args=(q_file, q_name))

    pw_1.start()
    time.sleep(2)
    pr.start()

    # pw_1.join()
    # pr.join()

    file = os.path.basename(path)
    print(file)
    dir_name = os.path.dirname(path)
    print(dir_name)
    file_name, extension_name = os.path.splitext(file)
    print(file_name)
    print(extension_name)
    file_name = file_name + '.npy'
    print(os.path.join(dir_name, file_name))


    while True:
        time.sleep(2)
        print('main pid {}'.format(os.getpid()))
