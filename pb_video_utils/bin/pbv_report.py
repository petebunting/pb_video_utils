#!/usr/bin/env python

import os
import argparse

from pb_video_utils import pbv_utils

def report_video_file(input_file):
    print("Video: {}".format(input_file))
    try:
        video_params = pbv_utils.get_video_params(input_file)
        print("\t Size ({}, {})".format(video_params['frame_width'], video_params['frame_height']))
        if (video_params['frame_height'] > video_params['frame_width']) or ((video_params['rotation'] != 0) and (video_params['rotation'] != 180)):
            print("\t\tRotation: {}".format(video_params['rotation']))
            print("\t\t**This is portrait video** - you might want to manually edit this one.")
            if (video_params['frame_height'] == 1080) and (video_params['frame_width'] == 1920):
                print("\t\t\t*Automated Fix Possible* - this video is the correct size (1080).")
            elif (video_params['frame_height'] == 720) and (video_params['frame_width'] == 1280):
                print("\t\t\t*Automated Fix Possible* - this video is small (720).")
            elif (video_params['frame_height'] == 2160) and (video_params['frame_width'] == 4096):
                print("\t\t\t*Automated Fix Possible* - this video is large (4k).")
            elif (video_params['frame_height'] == 2160) and (video_params['frame_width'] == 3840):
                print("\t\t\t*Automated Fix Possible* - this video is large (4k).")
            elif (video_params['frame_height'] == 1920) and (video_params['frame_width'] == 1080):
                print("\t\t\t*Automated Fix Possible* - this video is the correct size (1080).")
            elif (video_params['frame_height'] == 1280) and (video_params['frame_width'] == 720):
                print("\t\t\t*Automated Fix Possible* - this video is small (720).")
            elif (video_params['frame_height'] == 4096) and (video_params['frame_width'] == 2160):
                print("\t\t\t*Automated Fix Possible* - this video is large (4k).")
            elif (video_params['frame_height'] == 3840) and (video_params['frame_width'] == 2160):
                print("\t\t\t*Automated Fix Possible* - this video is large (4k).")
            else:
                print("\t\t\t**Manual Fix Required** - do not recognise the size of this video but will try a automated fix.")
        else:
            if (video_params['frame_height'] == 1080) and (video_params['frame_width'] == 1920):
                print("\t\t*Good* - this video is the correct size (1080).")
            elif (video_params['frame_height'] == 720) and (video_params['frame_width'] == 1280):
                print("\t\t*Automated Fix* - this video is small (720).")
            elif (video_params['frame_height'] == 2160) and (video_params['frame_width'] == 4096):
                print("\t\t*Automated Fix* - this video is large (4k).")
            elif (video_params['frame_height'] == 2160) and (video_params['frame_width'] == 3840):
                print("\t\t*Automated Fix* - this video is large (4k).")
            else:
                print("\t\t**Manual Fix Required** - do not recognise the size of this video.")
        print("\t FPS: {}".format(video_params['fps']))
        if (video_params['fps'] > 25) and (video_params['fps'] < 31):
            print("\t\t*Good* - frame rate is within normal bounds.")
        else:
            print("\t\t*Automated Fix* - this frame rate is expected to be about 30.")
    except Exception:
        print("\t***File Failed***")
    print("")

def report_dir_videos(input_dir):
    input_files = os.listdir(input_dir)
    not_video_files = []
    for input_file in input_files:
        input_file = os.path.join(input_dir, input_file)
        if os.path.isfile(input_file):
            file_ext = os.path.splitext(input_file)[1]
            if file_ext.lower() in pbv_utils.VIDEO_EXTS:
                report_video_file(input_file)
            else:
                not_video_files.append(input_file)
    print("The following where not videos files:")
    for input_file in not_video_files:
        print("\t{}".format(input_file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file or directory.")

    args = parser.parse_args()

    if os.path.isfile(args.input):
        report_video_file(args.input)
    elif os.path.isdir(args.input):
        report_dir_videos(args.input)
    else:
        raise Exception("Input is neither a file or directory...")

