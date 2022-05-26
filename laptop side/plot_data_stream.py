#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(0, 2 * np.pi, 100)
t = []
x = []
y = []
z = []
zeroes = None

fig: plt.Figure = None
ax: plt.Axes = None
fig, ax = plt.subplots()
ax.set_xlim(0, 30)
ax.set_ylim(-10, 10)

# animated=True tells matplotlib to only draw the artist when we
# explicitly request it
(ln,) = ax.plot(t, x, animated=False, ls='-')

# make sure the window is raised, but the script keeps going
plt.show(block=False)

# stop to admire our empty window axes and ensure it is rendered at
# least once.
#
# We need to fully draw the figure at its final size on the screen
# before we continue on so that :
#  a) we have the correctly sized and drawn background to grab
#  b) we have a cached renderer so that ``ax.draw_artist`` works
# so we spin the event loop to let the backend process any pending operations
plt.pause(0.1)

# get copy of entire figure (everything inside fig.bbox) sans animated artist
# bg = fig.canvas.copy_from_bbox(fig.bbox)


# # draw the animated artist, this uses a cached renderer
# ax.draw_artist(ln)
# # show the result to the screen, this pushes the updated RGBA buffer from the
# # renderer to the GUI framework so you can see it
# fig.canvas.blit(fig.bbox)
# fig.canvas.flush_events()

import socket
import sys
from struct import unpack

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

while True:
    # Wait for message
    message, address = sock.recvfrom(4096)
    print(f'Received {len(message)} bytes:')
    time_stamp, accel_x, ay, az = unpack('4d', message)
    # print(time_stamp)
    if zeroes is None:
        zeroes = (time_stamp, accel_x, ay, az)
        print(f'Zeroing with {zeroes}')
        continue
    else:
        t.append(time_stamp-zeroes[0])
        x.append(accel_x-zeroes[1])
        y.append(ay-zeroes[2])
        z.append(az-zeroes[3])

    # # reset the background back in the canvas state, screen unchanged
    # # fig.canvas.restore_region(bg)
    #
    # # update the artist, neither the canvas state nor the screen have changed
    ln.set_xdata(t)
    ln.set_ydata(x)
    # # re-render the artist, updating the canvas state, but not the screen
    ax.draw_artist(ln)
    # # copy the image to the GUI state, but screen might not be changed yet
    # # fig.canvas.blit(fig.bbox)
    # # flush any pending GUI events, re-painting the screen if needed
    fig.canvas.flush_events()
    # # you can put a pause in if you want to slow things down
    plt.pause(.1)
