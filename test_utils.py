import cv2
import math
import os
import threading
import time
import os

class test_utils( object ):

    def thres_segment( self, filename ):
        def nothing(x):
            pass

        # filename = 'mask.png'
        frame = cv2.imread(filename)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        cv2.namedWindow('threshold',256)
        cv2.createTrackbar('H_min', 'threshold', 0, 180, nothing)
        cv2.createTrackbar('H_max', 'threshold', 180, 180, nothing)
        cv2.createTrackbar('S_min', 'threshold', 0, 255, nothing)
        cv2.createTrackbar('S_max', 'threshold', 255, 255, nothing)
        cv2.createTrackbar('V_min', 'threshold', 0, 255, nothing)
        cv2.createTrackbar('V_max', 'threshold', 255, 255, nothing)

        while True:
            H_min = cv2.getTrackbarPos('H_min','threshold')
            H_max = cv2.getTrackbarPos('H_max', 'threshold')
            S_min = cv2.getTrackbarPos('S_min', 'threshold')
            S_max = cv2.getTrackbarPos('S_max', 'threshold')
            V_min = cv2.getTrackbarPos('V_min', 'threshold')
            V_max = cv2.getTrackbarPos('V_max', 'threshold')
            droplet_lower = (H_min, S_min, V_min)
            droplet_upper = (H_max, S_max, V_max)  # hue, sat, value
            bound_drop = [droplet_lower, droplet_upper]
            out = cv2.inRange(hsv, droplet_lower, droplet_upper)
            cv2.imshow('out',out)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destoryAllWindows()

    def batch_converter( self,  origpath, target_hard_disk ):
        # origpath = r"D:\070718_2"
        os.mkdir(target_hard_disk + origpath[1:])
        count = 0

        for (root, dirs, files) in os.walk(origpath):
            for dir in dirs:
                a = target_hard_disk + os.path.join(root, dir)[1:]
                os.mkdir(target_hard_disk + os.path.join(root, dir)[1:])
            for file in files:
                newpath = target_hard_disk + os.path.join(root, file)[1:-3] + 'mp4'

                cap = cv2.VideoCapture(os.path.join(root, file))
                ret, frame = cap.read()
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                videoWriter = cv2.VideoWriter(newpath, cv2.VideoWriter_fourcc(*"MP4V"), math.floor(fps),
                                              (math.floor(width), math.floor(height)))
                while ret:
                    videoWriter.write(frame)
                    ret, frame = cap.read()
                videoWriter.release()
                cap.release()
                count += 1
                print(count)

    def batch_video_catch( self, cam_sum, save, name, exposure ):
        '''

        :param cam_sum: the num of the cam
        :param save: save or not save video 0 or 1
        :param name: the name of the video if not save please send ''
        :param exposure: just exposure
        :return: None
        '''
        def save_video( switch, writer, frame ):
            if switch:
                writer.write( frame )

        def catch_video( cam_num ):
            cap = cv2.VideoCapture( cam_num )
            cap.set( cv2.CAP_PROP_EXPOSURE, exposure )

            writer = cv2.VideoWriter()
            w = ( int )( cap.get( cv2.CAP_PROP_FRAME_WIDTH ) )
            h = ( int )( cap.get( cv2.CAP_PROP_FRAME_HEIGHT ) )
            S = ( w, h )
            r = cap.get( cv2.CAP_PROP_FPS )
            if save:
                if not os.path.exists( './save' ):
                    os.mkdir( './save' )
                writer.open( './save/' + name + str( cam_num ) + '.avi', -1, 60, S, True )

            while ( cv2.waitKey( 30 ) != 27 ):
                ret, frame = cap.read()
                if not ret:
                    print( str( cam_num ) + '号视频信号丢失' )
                    break
                cv2.imshow( "capture" + str( cam_num ), frame )
                save_video( save, writer, frame )
                if cv2.waitKey( 1 ) & 0xFF == ord( 'q' ):
                    break
            cap.release()
            writer.release()
            cv2.destroyAllWindows()


        for i in range( cam_sum ):
            thread = threading.Thread( target = catch_video, args = (i,) )
            thread.start()


    def save_img( self, img, filename ):
        if not ( img.empty() ):
            cv2.imwrite( filename, img )
        else:
            print( 'no img' )


if __name__ == "__main__":
    utils = test_utils()
    utils.batch_video_catch( 3, 1, 'fuck', -5 )