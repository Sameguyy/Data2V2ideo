# encode.py
import sys
import os
from main import file_2_bits, bits_2_pixels, pixels_2_png, make_gif

def encode(input_path, out_gif=None, frame_width=3840, frame_height=2160):
    # read bits from file
    bits = file_2_bits(input_path)

    # pad bits to multiple of frame pixel count
    frame_size = frame_width * frame_height
    total_bits = len(bits)
    # use 1 bit per pixel; compute number of frames
    num_frames = (total_bits + frame_size - 1) // frame_size

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
        pixels_2_png(pixels, fname, reso=(frame_width, frame_height))
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
