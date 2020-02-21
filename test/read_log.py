path = '/Users/liusen/Documents/sz/智慧工地/Vas/logs/fog_server.log'
# path = '/Users/liusen/Documents/sz/智慧工地/Vas/logs/car_server.log'

if __name__ == '__main__':
    sum = 0
    with open(path, 'r') as conf:
        txt_conf = conf.readlines()
    for item in txt_conf:
        item = eval(item)
        sum += item
    print(len(txt_conf))
    print(sum/len(txt_conf))