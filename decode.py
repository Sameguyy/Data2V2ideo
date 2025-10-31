#!/usr/bin/env python3
import os
import sys
import json
import shutil
import imageio
from main import png_2_pixels, pixels_2_bits, bits_2_file, decode_header, file_2_bits
from PIL import Image

def load_config(path="config.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, path)
    with open(full_path, "r") as f:
        return json.load(f)

def extract_frames_from_gif(gif_path, out_folder="temp/frames_dec"):
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.makedirs(out_folder)
    vid = imageio.get_reader(gif_path)
    for i, frame in enumerate(vid):
        fname = os.path.join(out_folder, "frame-%05d.png" % i)
        imageio.imwrite(fname, frame)
    return out_folder

def decode(gif_path, output_folder=".", temp_folder="temp/frames_dec"):
    cfg = load_config()
    scale = cfg.get("scale", 1)

    frames_folder = extract_frames_from_gif(gif_path, temp_folder)

    # read logical pixels from each frame using png_2_pixels with scale
    logical_pixels = []
    frame_files = sorted(os.listdir(frames_folder))
    for fname in frame_files:
        if not fname.lower().endswith(".png"):
            continue
        full = os.path.join(frames_folder, fname)
        pixels = png_2_pixels(full, scale=scale)
        logical_pixels.extend(pixels)

    # convert logical pixels to bits
    bits = pixels_2_bits(logical_pixels)
    # diagnostic: show first 128 bits as bytes
    sample = bits[:128]
    byts = ['{0:08b}'.format(int(''.join(sample[i:i+8]),2)) for i in range(0, len(sample), 8)]
    print("DEBUG first bytes (bin):", ' '.join(byts))
    print("DEBUG first bytes (hex):", ' '.join(hex(int(b,2)) for b in byts))


    # decode header to get filename and payload bits
    fname, payload_bits = decode_header(bits)

    out_name = os.path.splitext(fname)[0] + "-recovered." + os.path.splitext(fname)[1]
    out_path = os.path.join(output_folder, out_name)

    # write payload bits to file
    bits_2_file(payload_bits, out_path)
    print("Decoded and wrote:", out_path)
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode.py <input.gif> [output_folder]")
        sys.exit(1)
    gif = sys.argv[1]
    outf = sys.argv[2] if len(sys.argv) > 2 else "."
    decode(gif, outf)

