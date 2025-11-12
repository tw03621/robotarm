#!/bin/bash
export DISPLAY=:0
export RESOLUTION=2500x1250x16

# Start Xvfb (virtual framebuffer)
Xvfb :0 -screen 0 $RESOLUTION &

# Start XFCE desktop
startxfce4 &

# Start VNC server
x11vnc -display :0 -rfbauth /root/.vnc/passwd -forever -shared -rfbport 5900 -listen 0.0.0.0 &

# Start noVNC (web access)
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# Keep container running
tail -f /dev/null
