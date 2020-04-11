#!/usr/bin/env python

import os
import argparse
import pprint
import subprocess
from pb_video_utils import pbv_utils


def norm_video_1080(input_file, output_file):
    try:
        video_params = pbv_utils.get_video_params(input_file)
        pprint.pprint(video_params)
        if video_params is not None:
            cmd = None
            print(input_file)
            if (video_params['frame_width'] == 1920) and (video_params['frame_height'] == 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
                print("Export Video without rescaling...")
                cmd = 'ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -filter:v fps=fps=30 "{}"'.format(input_file, output_file)
            elif (video_params['frame_height'] > video_params['frame_width']) or ((video_params['rotation'] != 0) and (video_params['rotation'] != 180)):
                print("Portrait Video - needs padding")
            elif (video_params['frame_height'] < 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
                print("Upscale")
                cmd = 'ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -vf "scale=1920x1080:flags=lanczos, fps=fps=30" "{}"'.format(input_file, output_file)
            elif (video_params['frame_height'] > 1080) and ((video_params['rotation'] == 0) or (video_params['rotation'] == 180)):
                print("Downscale")
                cmd = 'ffmpeg -i "{}" -c:v libx265 -preset medium -crf 20 -tag:v hvc1 -c:a aac -b:a 224k -b:v 16M -vf "scale=1920x1080:flags=lanczos, fps=fps=30" "{}"'.format(input_file, output_file)
            else:
                raise Exception("Do not know what to do with input file: '{}'".format(input_file))
            if cmd is not None:
                print(cmd)
                subprocess.call(cmd, shell=True)
        else:
            raise Exception("The video paramaters could not be found...")
    except Exception:
        print("Could not open file: '{}'".format(input_file))
    print("\n\n")


def norm_dir_videos_1080(input_dir, output_dir, replace=False, original=False):
    input_files = os.listdir(input_dir)
    for input_file in input_files:
        input_file = os.path.join(input_dir, input_file)
        if os.path.isfile(input_file):
            file_ext = os.path.splitext(input_file)[1]
            if file_ext.lower() in pbv_utils.VIDEO_EXTS:
                edit_out_names = (not original)
                basename = pbv_utils.get_file_basename(input_file, checkvalid=edit_out_names, lowercase=edit_out_names)
                output_file = os.path.join(output_dir, "{}.mp4".format(basename))
                if (not os.path.exists(output_file)) or replace:
                    norm_video_1080(input_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file or directory.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file or directory.")
    parser.add_argument("--replace", action='store_true', default=False,
                        help='''Specify that output files are to be replaced.''')
    parser.add_argument("--original", action='store_true', default=False,
                        help='''Specify that output file names should be the originals (when input directory.''')
    args = parser.parse_args()
    
    if os.path.isfile(args.input):
        if os.path.isdir(args.output):
            raise Exception("The output must be a file as the input is a file.")
        if (not os.path.exists(args.output)) or args.replace:
            norm_video_1080(args.input, args.output)
    elif os.path.isdir(args.input):
        if not os.path.isdir(args.output):
            raise Exception("The output must be a directory as the input is a directory.")
        norm_dir_videos_1080(args.input, args.output, args.replace, args.original)
    else:
        raise Exception("Input is neither a file or directory...")

