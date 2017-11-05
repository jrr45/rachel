import master_locator
import numpy as np
import sound_locator

randn = np.random.randn
d = randn(7, 1)
d_mat = abs(randn(7, 7))

x_mat=master_locator.locations(d_mat)
x=sound_locator.sound_finder(d,x_mat)
