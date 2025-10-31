#!/usr/bin/env python3
import sys
import os
from main import file_2_bits, bits_2_pixels, pixels_2_png, make_gif, add_header
import json

def load_config(path="config.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, path)
    with open(full_path, "r") as f:
        return json.load(f)

def encode(input_path, out_gif=None):
    cfg = load_config()
    frame_width, frame_height = cfg["resolution"]
    scale = cfg["scale"]
    temp_folder = cfg.get("temp_folder", "temp/frames")

    print(f"Loaded config: res={frame_width}x{frame_height}, scale={scale}")

    # read bits from file
    bits = file_2_bits(input_path)

    # diagnostic: show first 64 bits as bytes (useful to compare with decoder)
    if len(bits) >= 64:
        first_bytes = []
        for i in range(0, 64, 8):
            byte = int(''.join(bits[i:i+8]), 2)
            first_bytes.append(hex(byte))
        print("DEBUG: first bytes hex:", ' '.join(first_bytes))
    else:
        print("DEBUG: bits length <", len(bits))

    # add header (filename + payload length) compatible with decode_header in main.py
    bits = add_header(bits, os.path.basename(input_path).encode('utf-8'))

# Number of logical bits in a frame (Based on the specified scale)
    logical_w = frame_width // scale
    logical_h = frame_height // scale
    frame_size = logical_w * logical_h

    total_bits = len(bits)
    num_frames = (total_bits + frame_size - 1) // frame_size
    print(f"Frame logical grid: {logical_w}x{logical_h}, total bits per frame: {frame_size}")


    # create temp folder
    temp_folder = "temp/frames"
    if os.path.exists(temp_folder):
        # keep previous contents or clear
        import shutil
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder)

    # for each frame, take slice of bits, convert to pixels and save png
    for i in range(num_frames):
        start = i * frame_size
        end = min(start + frame_size, total_bits)
        frame_bits = bits[start:end]
        # pad with zeros (black pixels)
        if len(frame_bits) < frame_size:
            frame_bits += ['0'] * (frame_size - len(frame_bits))
        pixels = bits_2_pixels(frame_bits)
        fname = os.path.join(temp_folder, "frame-%05d.png" % i)
        pixels_2_png(pixels, fname, reso=(frame_width, frame_height), scale=scale)

        print("Wrote", fname)

    # make gif 
    base_out = out_gif[:-4] if out_gif and out_gif.endswith(".gif") else (out_gif or "out")
    gif_path = make_gif(temp_folder, base_out)
    print("Created:", gif_path)
    return gif_path
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encode.py <input_file> [output.gif]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    encode(inp, out)
