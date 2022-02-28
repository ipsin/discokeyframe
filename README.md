# discokeyframe
Manage your camera controls for [Disco Diffusion v5](https://colab.research.google.com/github/alembics/disco-diffusion/blob/main/Disco_Diffusion.ipynb) using a simple config file.

```
# Comments start with #.
# Change zoom to 1.03 at frame 300
00300 Z 1.03

# Rotate camera (x y z).  Here, (y by -1 degree per frame and z by 1 degree per frame) at frame 350.
# Here (x y z) are in radians, so each degree is 3.14/180, or about 0.0174.
00350 C 0 -0.0174 0.0174

# Translate camera (x y z). Translate camera by (10,-10,5) at frame 500.
00500 T 10 -10 5
```
