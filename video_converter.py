import ffmpeg
import os

video = (ffmpeg
	.input('*.jpg', pattern_type='glob', framerate=1)
	.filter('scale', size='hd1080', force_original_aspect_ratio='increase')
	.output('movie.mp4', crf=20, preset='slower', movflags='faststart', pix_fmt='yuv420p')
	.run()
)