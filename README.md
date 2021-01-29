# TellowFollow

This repos is the code that I used in the 2020 Fall Raytheon Hackathon

Run on the DJI Tello, a live stream of the onboard camera was used to track and direct the drone to follow a colored ball. 
Color filtering was used to detect the presence of the ball. The ball's image momment was used to determine it's centroid/ where the ball was in the image,
it's radius/ depth, and how the drone should move to center the ball in the image. The drone moved linearly with respect to how far the ball was from the center.
Further from center would prompt faster corrections.
