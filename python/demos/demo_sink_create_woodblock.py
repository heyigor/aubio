#! /usr/bin/env python

import sys
from math import pi, e
from aubio import sink
from numpy import arange, resize, sin, exp, zeros

if len(sys.argv) < 2:
    print 'usage: %s <outputfile> [samplerate]' % sys.argv[0]
    sys.exit(1)

samplerate = 44100 # samplerate in Hz
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

pitch = 2200            # in Hz
blocksize = 256         # in samples
duration = 0.02         # in seconds

twopi = pi * 2.

duration = int ( samplerate * duration ) # convert to samples
attack = int (samplerate * .001 )
decay = .5

period = float(samplerate) /  pitch
# create a sine lookup table
tablelen = 1000
sinetable = arange(tablelen + 1, dtype = 'float32')
sinetable = 0.7 * sin(twopi * sinetable/tablelen)
sinetone = zeros((duration,), dtype = 'float32')

# compute sinetone at floating point period
for i in range(duration):
    x = int((i % period) / float(period) * tablelen)
    sinetone[i] = (sinetable[x] + sinetable[x+1]) / 2

# apply some envelope
float_ramp = arange(duration, dtype = 'float32')
sinetone *= exp( - e * float_ramp / duration / decay)
sinetone[:attack] *= exp( e * ( float_ramp[:attack] / attack - 1 ) )

if 0:
    import matplotlib.pyplot as plt
    plt.plot(sinetone)
    plt.show()

my_sink = sink(sys.argv[1], samplerate)

total_frames = 0
while total_frames + blocksize < duration:
    my_sink(sinetone[total_frames:total_frames+blocksize], blocksize)
    total_frames += blocksize
my_sink(sinetone[total_frames:duration], duration - total_frames)
