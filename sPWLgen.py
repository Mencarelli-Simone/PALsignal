import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


# %% parameters
## fun
def save_to_ltspice_plf(filename, time_array, voltage_array):
    """
    Save time and voltage arrays to an LTSpice-compatible Piecewise Linear Function (PLF) file.

    :param filename: Name of the output file (e.g., 'output.plf')
    :param time_array: Numpy array of time values
    :param voltage_array: Numpy array of voltage values
    """
    with open(filename, 'w') as file:
        for t, v in zip(time_array, voltage_array):
            file.write(f"{t:.12e} {v:.6f}\n")


# Example usage:
# save_to_ltspice_plf("vga_signal.plf", imposed_time, imposed_voltage)
# class

class VGAsignal:
    def __init__(self):
        ## timing parameters from www.batsocks.co.uk/readme/video_timing.htm
        line_period = 64.05e-6  # 64us
        self.line_period = line_period
        line_blanking = 12.05e-6  # 12us pm .25us ( line_period - visual_time )
        line_sync = 4.7e-6  # 4.7us pm 0.1us
        self.line_sync = line_sync
        front_porch = 1.65e-6  # 1.65us pm 0.1us
        self.front_porch = front_porch
        visual_time = 51.95e-6  # 52us
        self.visual_time = visual_time
        back_porch = 5.7e-6  # 5.7us pm 0.1us
        self.back_porch = back_porch

        # vertical sync parameters
        short_sync = 2.35e-6  # 2.35us pm 0.1us # for vertical blanking
        broad_sync = line_period / 2 - 4.7e-6  # 59.35us pm 0.1us # for vertical blanking

        ## voltage parameters
        black_level = 0.3
        self.black_level = black_level
        white_level = 1.0
        self.white_level = white_level

        ## video resolution
        self.horizontal_resolution = 8  # 720 simplified to 8 for grey bars
        self.vertical_resolution = 576

        ## video matrix
        video_matrix = np.zeros((self.horizontal_resolution, self.vertical_resolution))
        # fill matrix with grey bars
        gray_levels = np.linspace(black_level, white_level, self.horizontal_resolution)
        for i in range(self.horizontal_resolution):
            video_matrix[i, :] = gray_levels[i]
        self.video_matrix = video_matrix

        ## sequences
        self.half_broad_scanline = \
            {
                'time': np.array([0, broad_sync, broad_sync, line_period / 2]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'half broad scanline, starts with broad_sync lasts for 1/2 line_period'
            }
        self.half_short_scanline = \
            {
                'time': np.array([0, short_sync, short_sync, line_period / 2]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'half short scanline, starts with short_sync lasts for 1/2 line_period'
            }

        self.blank_line = \
            {
                'time': np.array([0, line_sync, line_sync, line_period]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'blank line, starts with line_sync lasts for line_period'
            }

        self.half_blank_line = \
            {
                'time': np.array([0, line_sync, line_sync, line_period / 2]),
                'voltage': np.array([0, 0, black_level, white_level]),
                'description': 'half blank line, starts with line_sync lasts for 1/2 line_period'
            }

        self.half_display_line = \
            {
                'time': np.array([0, line_sync, line_sync, line_period / 2]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'half display line, starts with line_sync lasts for 1/2 line_period'
            }
        # self.display_line = \
        #     {
        #         'time': np.array([0, line_sync, line_sync, line_period]),
        #         'voltage': np.array([0, 0, black_level, white_level]),
        #         'description': 'full display line, starts with line_sync lasts for 1/2 line_period'
        #     }
        self.display_line = \
            {
                'time': np.array([0, line_sync, line_sync, line_period]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'full display line, starts with line_sync lasts for 1/2 line_period'
            }
        self.half_null_line = \
            {
                'time': np.array([0, line_period / 2]),
                'voltage': np.array([black_level, black_level]),
                'description': 'half null line, starts with line_sync lasts for 1/2 line_period'
            }
        self.half_line_sync = \
            {
                'time': np.array([0, line_sync, line_sync, line_period / 2]),
                'voltage': np.array([0, 0, black_level, black_level]),
                'description': 'half line sync, starts with line_sync lasts for 1/2 line_period'
            }
        self.end_zero = \
            {
                'time': np.array([0]),
                'voltage': np.array([0]),
                'description': 'end zero, signal stop'
            }

        self.get_signal()
        # interlaced sequence
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
        Concatenates all the sequences to form the video signal and creates an empty video time matrix containing
        the timestamps of video pixel transitions according to the set resolution.
        """
        # Map sequence names to actual sequence objects
        sequence_map = {
            'half_broad_scanline': self.half_broad_scanline,
            'half_short_scanline': self.half_short_scanline,
            'blank_line': self.blank_line,
            'half_blank_line': self.half_blank_line,
            'half_display_line': self.half_display_line,
            'display_line': self.display_line,
            'half_null_line': self.half_null_line,
            'half_line_sync': self.half_line_sync,
            'end_zero': self.end_zero
        }

        # Order of sequences and corresponding repetition counts
        sequence_order = [
            ('half_broad_scanline', 5),  # 5 half broad scanlines
            ('half_short_scanline', 5),  # 5 half short scanlines
            ('blank_line', 17),  # 17 blank lines
            ('half_blank_line', 1),  # 1 half blank line
            ('half_display_line', 1),  # 1 half display line
            ('display_line', 287),  # 287 even display lines
            ('half_short_scanline', 5),  # 5 half short scanlines
            ('half_broad_scanline', 5),  # 5 half broad scanlines
            ('half_short_scanline', 5),  # 5 half short scanlines
            ('half_null_line', 1),  # 1 half null line
            ('blank_line', 17),  # 17 blank lines
            ('display_line', 287),  # 287 odd display lines
            ('half_line_sync', 1),  # 1 half line sync
            ('half_short_scanline', 5),  # 5 half short scanlines
            ('end_zero', 1)  # 1 end zero
        ]

        # Initialize signal arrays
        full_time = []
        full_voltage = []
        # initialize video signal array
        video_time = []
        video_voltage = []

        # Concatenate sequences
        current_time_offset = 0
        line_counter = 0  # to keep track of the line number
        for sequence_name, repetitions in sequence_order:
            sequence = sequence_map[sequence_name]
            for _ in range(repetitions):
                # Add time and voltage for this sequence
                full_time.extend(sequence['time'] + current_time_offset)
                full_voltage.extend(sequence['voltage'])
                if sequence_name == 'display_line':
                    line_start_time = current_time_offset + self.line_sync + self.front_porch
                    line_end_time = line_start_time + self.visual_time

                    # Calculate pixel times and voltages for a step-like signal
                    pixel_times = np.linspace(line_start_time, line_end_time, self.horizontal_resolution + 1)
                    pixel_voltages = self.video_matrix[:, line_counter * 2 % self.vertical_resolution]

                    # Create step-like behavior: each pixel holds constant until the next pixel
                    for i in range(self.horizontal_resolution):
                        video_time.extend([pixel_times[i], pixel_times[i + 1]])
                        video_voltage.extend([pixel_voltages[i], pixel_voltages[i]])

                    # Add black level to transition after the last pixel
                    video_time.append(pixel_times[-1])
                    video_voltage.append(self.black_level)
                # Update time offset for the next sequence
                current_time_offset += sequence['time'][-1]

        # Convert to numpy arrays
        self.signal_time = np.array(full_time)
        self.signal_voltage = np.array(full_voltage)
        self.video_time = np.array(video_time)
        self.video_voltage = np.array(video_voltage)

        # Return the concatenated signal
        return self.signal_time, self.signal_voltage, self.video_time, self.video_voltage

    def impose_video_signal(self):
        """
        Imposes the video signal on the full VGA signal by summing their voltages
        while merging time indices and preserving step transitions.
        """
        # Get original signal and video components
        signal_time, signal_voltage, video_time, video_voltage = self.get_signal()

        # Step 1: Merge time axes **without removing duplicates**
        merged_time = np.concatenate((signal_time, video_time))  # Merge without filtering
        merged_voltage = np.concatenate((signal_voltage, video_voltage))  # Merge voltages

        # Step 2: Sort everything while keeping order stable
        sorted_indices = np.argsort(merged_time, kind='stable')  # Sort indices
        final_time = merged_time[sorted_indices]  # Sorted time axis
        final_voltage = merged_voltage[sorted_indices]  # Sort corresponding voltages

        # smooter

        for i in range(len(final_time)):
            if i > 1:
                if final_time[i] == final_time[i - 1]:
                    final_time[i] = final_time[i] + 1e-6  # add a microsec
        save_to_ltspice_plf('pal.pwl', final_time, final_voltage)
        return final_time, final_voltage


# Test code to plot the generated signal

if __name__ == "__main__":
    # Instantiate the VGAsignal class
    vga_signal = VGAsignal()

    # Retrieve the signal and video components
    signal_time, signal_voltage, video_time, video_voltage = vga_signal.get_signal()

    # Plot the full signal
    plt.figure(figsize=(12, 6))
    plt.plot(signal_time, signal_voltage, label="Full Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Full VGA Signal")
    plt.grid()
    plt.legend()
    plt.show()

    # Plot the video portion of the signal
    # plt.figure(figsize=(12, 6))
    plt.plot(video_time, video_voltage, label="Video Signal", color='orange')
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("Video Signal Overlay")
    plt.grid()
    plt.legend()
    plt.show()

    # Apply the video signal onto the full signal
    imposed_time, imposed_voltage = vga_signal.impose_video_signal()

    # Plot the imposed signal
    plt.figure(figsize=(12, 6))
    plt.plot(imposed_time, imposed_voltage, label="Imposed Signal", color="red")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.title("VGA Signal with Imposed Video Signal")
    plt.grid()
    plt.legend()
    plt.show()
