import sys
path_0 = '/home/user/workspace/priv-0220/Vas/logs/fog_server.log'
path_1 = '/home/user/workspace/priv-0220/Vas/logs/car_server.log'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = path_0
    else:
        names = locals()
        mode = int(sys.argv[1])
        path = names['path_{}'.format(mode)]
    sum = 0
    print(path)
    with open(path, 'r') as conf:
        txt_conf = conf.readlines()
    for item in txt_conf:
        item = eval(item)
        sum += item
    print(len(txt_conf))
    print(sum/len(txt_conf))