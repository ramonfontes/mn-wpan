"""Script to plot CPU usage and energy consumption from .log files"""

import re
from datetime import datetime
import glob

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import ScalarFormatter


def extract_number(filename):
    """Extracts the first number from a filename for sorting."""
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')


def read_data_from_file(file_path):
    """Reads a .log file and returns timestamps, CPU usage, and energy consumption values."""
    timestamps = []
    values1 = []  # To store CPU usage values
    values2 = []  # To store energy consumption values

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split(',')
            if len(parts) == 3:
                timestamp = parts[0].strip()
                value1 = float(parts[1].strip())
                value2 = float(parts[2].strip())

                timestamps.append(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'))
                values1.append(value1)
                values2.append(value2)

    return timestamps, values1, values2


# Path to .log files
file_paths = sorted(glob.glob('*.log'), key=extract_number)

# Layout configuration using GridSpec
num_files = len(file_paths)
num_rows = (num_files + 1) // 2
fig = plt.figure(figsize=(10, 2 * num_rows))
gs = GridSpec(num_rows, 2, figure=fig)
fig.suptitle("Energy Consumption", fontsize=13)

# Generate subplots for each file
for i, path in enumerate(file_paths):
    ts, cpu_usage, energy = read_data_from_file(path)

    label_name = path.split('/')[-1]
    row, col = divmod(i, 2)
    ax = fig.add_subplot(gs[row, col])

    ax.plot(ts, cpu_usage, linestyle='-', label='CPU Usage', color='tab:blue')
    ax2 = ax.twinx()
    ax2.plot(ts, energy, linestyle='--', label='Energy Consumption', color='tab:orange')

    ax.set_title(f'{label_name[:-4]}', fontsize=12)
    ax.set_xlabel('Time', fontsize=8)
    ax.set_ylabel('CPU Usage (%)', color='tab:blue', fontsize=8)
    ax.tick_params(axis='y', labelcolor='tab:blue')
    ax.set_ylim(top=5)

    ax2.set_ylabel('Energy \nConsumption (Wh)', color='tab:orange', fontsize=8)
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    ax2.set_ylim(top=0.0007)

    # Show up to 3 X-axis labels
    if len(ts) >= 3:
        xticks = ts[::len(ts) // 3]
        ax.set_xticks(xticks)
        ax.set_xticklabels([t.strftime('%H:%M:%S') for t in xticks], fontsize=6)
    else:
        ax.set_xticks(ts)
        ax.set_xticklabels([t.strftime('%H:%M:%S') for t in ts], fontsize=6)

fig.subplots_adjust(hspace=0.4, wspace=0.4)
plt.show()
# plt.savefig("cpu_load.eps")
