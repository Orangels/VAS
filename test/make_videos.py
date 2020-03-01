import os
import cv2

video_path = '/Users/liusen/Documents/sz/智慧工地/test_video/宏江金贸土石方作业/20200226_125756_Trim.mp4'
out_path = '/Users/liusen/Documents/sz/智慧工地/test_video/宏江金贸土石方作业/20200226_125756_Trim_test.mp4'
img_path = '/Users/liusen/Documents/sz/智慧工地/test_video/宏江金贸土石方作业/image'
# fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')  # opencv3.0
# fourcc = cv2.VideoWriter_fourcc('X','V','I','D')  # opencv3.0
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')  # 保存 mp4

def unlock_movie(path):
    """ 将视频转换成图片
    path: 视频路径 """
    cap = cv2.VideoCapture(path)
    suc = cap.isOpened()  # 是否成功打开
    frame_count = 0
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    suc, frame = cap.read()
    # videoWriter = cv2.VideoWriter(out_path, fourcc, fps, (1280, 720))
    # videoWriter.write(frame)
    while suc:
        frame_count += 1
        suc, frame = cap.read()
        print(frame_count)
        # cv2.imwrite('{}/{}.png'.format(img_path, str(frame_count).zfill(5)), frame)
        # videoWriter.write(frame)
        # if frame_count % 500 == 0:
        if frame_count % 4500 == 0:
            print('decode num -- {}'.format(frame_count))
            cv2.imwrite('{}/{}.png'.format(img_path, str(frame_count).zfill(5)), frame)
    # videoWriter.release()

    cap.release()
    print('unlock movie: ', frame_count)


def make_video():
    # fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # opencv3.0
    videoWriter = cv2.VideoWriter(out_path, fourcc, 30, (1280, 720))

    files = os.listdir(img_path)
    files.sort(key=lambda x: int(x.split('.')[0]))

    for i, path in enumerate(files):
        print(i)
        frame = cv2.imread(os.path.join(img_path, path))
        videoWriter.write(frame)
        if i == 500:
            break

    videoWriter.release()


if __name__ == '__main__':
    unlock_movie(video_path)
    # make_video()