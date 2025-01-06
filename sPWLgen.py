import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')

# %% parameters

## timing parameters from www.batsocks.co.uk/readme/video_timing.htm
line_period = 64.05e-6  # 64us
line_blanking = 12.05e-6  # 12us pm .25us ( line_period - visual_time )
line_sync = 4.7e-6  # 4.7us pm 0.1us
front_porch = 1.65e-6  # 1.65us pm 0.1us
visual_time = 51.95e-6 # 52us
back_porch = 5.7e-6  # 5.7us pm 0.1us

# vertical sync parameters
short_sync = 2.35e-6  # 2.35us pm 0.1us # for vertical blanking
broad_sync = line_period - 4.7e-6  # 59.35us pm 0.1us # for vertical blanking

# interlaced sequence todo translate to a list of sequnces
# half_broad_scanlines = 5 # each starts with broad_sync
# half_short_scanlines = 5 # each starts with short_sync
# blank_lines = 17 # starts with line_sync than black
# half_blank_line = 1 # starts with line_sync than black
# half_display_line = 1 # the video starts at 1/2 of the line
# even_display_lines = 287 # plus the half above each starts with line_sync
# half_short_scanlines = 5 # each starts with short_sync
# half_broad_scanlines = 5 # each starts with broad_sync
# half_short_scanlines = 5 # each starts with short_sync
# blank_lines = 17 # starts with line_sync than black
# odd_display_lines = 287 #
# half_line_sync = 1 # starts with line_sync video stops at 1/2 of the line
# half_short_scanlines = 5 # each starts with short_sync

# let's define a sequence as a dictionary containing a time and a voltage key
# then we can define a list of sequences (video sync)
# also need a matrix to describe the vga video signal 720 x 576









## resolution parameters
horizontal_lines = 625

## voltage parameters
black_level = 0.3
white_level = 1.0
