# Let's test the heading angle with CW90 vs CW270
import math

# Suppose when facing North, the raw sensor magnetic vector has:
# In the user's case, when facing North, the reported heading is West (270 deg).
# atan2(-Y, X) = 270 deg => X = 0, Y = +1 (or similar)
# We want reported heading when facing North to be 0 deg => X = 1, Y = 0.

# If we apply CW90:
# X' = Y, Y' = -X
# If X=0, Y=1: X' = 1, Y' = 0 => atan2(0, 1) = 0 deg! Exactly North!
print("CW90_DEG rotates 270 deg (West) to 0 deg (North)!")

# If we apply CW270:
# X' = -Y, Y' = X
# If X=0, Y=1: X' = -1, Y' = 0 => atan2(0, -1) = 180 deg (South)
