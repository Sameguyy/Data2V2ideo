# decode.py
import sys
import os
from main import png_2_pixels, pixels_2_bits, bits_2_file
from PIL import Image
import imageio
import shutil

def extract_frames_from_gif(gif_path, out_folder="temp/frames_dec"):
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.makedirs(out_folder)
    vid = imageio.get_reader(gif_path)
    for i, frame in enumerate(vid):
        fname = os.path.join(out_folder, "frame-%05d.png" % i)
        imageio.imwrite(fname, frame)
    return out_folder

def decode(gif_path, output_file=None):
    frames_folder = extract_frames_from_gif(gif_path)
    bits = []
    # iterate frames in sorted order
    items = sorted(os.listdir(frames_folder))
    for fname in items:
        if not fname.endswith(".png"):
            continue
        pixels = png_2_pixels(os.path.join(frames_folder, fname))
        bits += pixels_2_bits(pixels)
    out_path = output_file or (os.path.splitext(gif_path)[0] + ".recovered")
    bits = bits[:len(bits) - (len(bits) % 8)]  # trim to full bytes
    bits_2_file(bits, out_path)
    print("Recovered file:", out_path)
    return out_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode.py <input.gif> [output_file]")
        sys.exit(1)
    gif = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    decode(gif, out)
