from PIL import Image, ImageOps
import ffmpeg
from typing import Tuple
import os


def generate_thumbnail(input_path: str, output_path: str, size: Tuple[int, int] = (1280, 720)) -> str:
	img = Image.open(input_path)
	thumb = ImageOps.fit(img, size, method=Image.LANCZOS)
	thumb.save(output_path, format="JPEG", quality=90)
	return output_path


def transcode_video_for_platform(input_path: str, output_path: str, platform: str) -> str:
	# basic presets per platform
	presets = {
		"instagram": {"vcodec": "libx264", "crf": 23, "pix_fmt": "yuv420p", "r": 30, "aspect": "9:16"},
		"tiktok": {"vcodec": "libx264", "crf": 23, "pix_fmt": "yuv420p", "r": 30, "aspect": "9:16"},
		"youtube": {"vcodec": "libx264", "crf": 20, "pix_fmt": "yuv420p", "r": 30, "aspect": "16:9"},
	}
	preset = presets.get(platform, presets["youtube"])
	stream = ffmpeg.input(input_path)
	if preset["aspect"] == "9:16":
		stream = ffmpeg.filter(stream, 'scale', '1080:-2')
	else:
		stream = ffmpeg.filter(stream, 'scale', '1280:-2')
	out = ffmpeg.output(stream, output_path, vcodec=preset["vcodec"], crf=preset["crf"], pix_fmt=preset["pix_fmt"], r=preset["r"])
	ffmpeg.run(out, overwrite_output=True, quiet=True)
	return output_path