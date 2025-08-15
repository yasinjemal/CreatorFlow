import subprocess, shlex, tempfile, os

def transcode_to_mp4(input_path: str, output_path: str, width: int = 1080, height: int = 1920, fps: int = 30):
    cmd = f"ffmpeg -y -i {shlex.quote(input_path)} -vf scale={width}:{height} -r {fps} -c:v libx264 -pix_fmt yuv420p {shlex.quote(output_path)}"
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
