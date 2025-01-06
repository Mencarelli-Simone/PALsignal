import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


# %% parameters


class VGAsignal:
    def __init__(self):
        ## timing parameters from www.batsocks.co.uk/readme/video_timing.htm
        line_period = 64.05e-6  # 64us
        line_blanking = 12.05e-6  # 12us pm .25us ( line_period - visual_time )
        line_sync = 4.7e-6  # 4.7us pm 0.1us
        front_porch = 1.65e-6  # 1.65us pm 0.1us
        visual_time = 51.95e-6  # 52us
        back_porch = 5.7e-6  # 5.7us pm 0.1us

        # vertical sync parameters
        short_sync = 2.35e-6  # 2.35us pm 0.1us # for vertical blanking
        broad_sync = line_period / 2 - 4.7e-6  # 59.35us pm 0.1us # for vertical blanking

        ## voltage parameters
        black_level = 0.3
        white_level = 1.0

        ## video resolution
        horizontal_resolution = 8  # 720 simplified to 8 for grey bars
        vertical_resolution = 576

        ## video matrix
        video_matrix = np.zeros((horizontal_resolution, vertical_resolution))
        # fill matrix with grey bars
        gray_levels = np.linspace(black_level, white_level, horizontal_resolution)
        for i in range(horizontal_resolution):
            video_matrix[i, :] = gray_levels[i]

        ## sequences
        half_broad_scanline = \
            {
                'time': np.array([0, broad_sync, line_period / 2]),
                'voltage': np.array([0, black_level, black_level]),
                'description': 'half broad scanline, starts with broad_sync lasts for 1/2 line_period'
            }
        half_short_scanline = \
            {
                'time': np.array([0, short_sync, line_period / 2]),
                'voltage': np.array([0, black_level, black_level]),
                'description': 'half short scanline, starts with short_sync lasts for 1/2 line_period'
            }

        blank_line = \
            {
                'time': np.array([0, line_sync, line_period]),
                'voltage': np.array([0, black_level, black_level]),
                'description': 'blank line, starts with line_sync lasts for line_period'
            }

        half_blank_line = \
            {
                'time': np.array([0, line_sync, line_period / 2]),
                'voltage': np.array([0, black_level, white_level]),
                'description': 'half blank line, starts with line_sync lasts for 1/2 line_period'
            }

        half_display_line = \
            {
                'time': np.array([0, line_sync, line_period / 2]),
                'voltage': np.array([0, black_level, black_level]),
                'description': 'half display line, starts with line_sync lasts for 1/2 line_period'
            }
        display_line = \
            {
                'time': np.array([0, line_sync, line_period]),
                'voltage': np.array([0, black_level, white_level]),
                'description': 'full display line, starts with line_sync lasts for 1/2 line_period'
            }
        half_null_line = \
            {
                'time': np.array([0, line_period / 2]),
                'voltage': np.array([black_level, black_level]),
                'description': 'half null line, starts with line_sync lasts for 1/2 line_period'
            }

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
        # half_nul_line = 1 # constant black line lasts for 1/2 line_period
        # blank_lines = 17 # starts with line_sync than black
        # odd_display_lines = 287 #
        # half_line_sync = 1 # starts with line_sync video stops at 1/2 of the line
        # half_short_scanlines = 5 # each starts with short_sync

        # let's define a sequence as a dictionary containing a time and a voltage key
        # then we can define a list of sequences (video sync)
        # also need a matrix to describe the vga video signal 720 x 576

    def set_video_matrix(self, video_matrix):
        self.video_matrix = video_matrix

    def get_signal(self):
        """
        concatenates all the sequences to form the video signal and creates an empty video time matrix
        """
        pass
    def impose_video_signal(self):
        """
        imposes the video signal on the signal
        """
        pass

## resolution parameters
horizontal_lines = 625
