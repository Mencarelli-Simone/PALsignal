
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

# PAL signal parameters
frame_duration = 0.02  # 20ms per frame (50Hz field rate)
line_duration = 64e-6  # 64µs per line
active_video_duration = 52e-6  # Active video part of each line
sync_duration = 4.7e-6  # Horizontal sync pulse duration
blanking_duration = 5.8e-6  # Back porch duration
lines_per_frame = int(frame_duration / line_duration)  # Total number of lines
vertical_sync_lines = 5  # Number of lines for vertical sync
equalizing_pulse_duration = 2.35e-6
broad_sync_duration = 27e-6

# Gray levels for active video (8 levels)
gray_levels = np.linspace(1.0, 0.3, 8)

# Initialize time and voltage arrays
time_points = []
voltage_points = []

current_time = 0.0

# Generate PAL signal
for line in range(lines_per_frame):
    if line < vertical_sync_lines:
        # Vertical sync (broad and equalizing pulses)
        t = current_time
        # Pre-equalizing pulses
        for _ in range(int(line_duration / (2 * equalizing_pulse_duration))):
            time_points.extend([t, t + equalizing_pulse_duration])
            voltage_points.extend([0.0, 0.3])  # Sync and blanking levels
            t += 2 * equalizing_pulse_duration

        # Broad sync pulse
        time_points.extend([t, t + broad_sync_duration])
        voltage_points.extend([0.0, 0.0])  # Sync level
        t += broad_sync_duration

        # Post-equalizing pulses
        for _ in range(int(line_duration / (2 * equalizing_pulse_duration))):
            time_points.extend([t, t + equalizing_pulse_duration])
            voltage_points.extend([0.0, 0.3])  # Sync and blanking levels
            t += 2 * equalizing_pulse_duration

    else:
        # Horizontal sync and active video for normal lines
        t_start = current_time

        # Horizontal sync pulse
        time_points.extend([t_start, t_start + sync_duration])
        voltage_points.extend([0.0, 0.0])

        # Back porch
        time_points.extend([t_start + sync_duration, t_start + blanking_duration])
        voltage_points.extend([0.3, 0.3])

        # Active video (8 gray bands per line)
        t_active_start = t_start + blanking_duration
        for i in range(8):  # 8 gray bands per line
            gray_level = gray_levels[i]
            t_band_start = t_active_start + (i * active_video_duration / 8)
            t_band_end = t_band_start + (active_video_duration / 8)

            time_points.extend([t_band_start, t_band_end])
            voltage_points.extend([gray_level, gray_level])

        # Front porch (return to blanking)
        t_active_end = t_start + line_duration
        time_points.extend([t_active_end])
        voltage_points.extend([0.3])

    # Update time for the next line
    current_time += line_duration

# Convert to numpy arrays
time_points = np.array(time_points)
voltage_points = np.array(voltage_points)

# Ensure time axis is sorted
sorted_indices = np.argsort(time_points)
time_points = time_points[sorted_indices]
voltage_points = voltage_points[sorted_indices]

# Plot the signal
plt.figure(figsize=(15, 5))
plt.plot(time_points, voltage_points, label='PAL Composite Video Signal', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('PAL Composite Video Signal (VSync and Active Video)')
plt.grid()
plt.legend()
plt.show()
