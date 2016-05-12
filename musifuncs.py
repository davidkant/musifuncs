import numpy as np

# acoustics ------------------------------------------------------------------ #

def dB_to_amp(dB):
  
     """Decibels to amplitude."""

     return 10**(dB/20.)


def amp_to_dB(amp):

    """Amplitude to decibels."""
      
    return 20*np.log10(amp)


def power_to_dB(pwr):    
        
    """Power to decibels."""
 
    return 10*np.log10(pwr)


# pitch and tuning ----------------------------------------------------------- #

def ratio_to_cents(r): 

	"""Ratio to cents."""

	return 1200.0 * np.log2(r)


def cents_to_ratio(c): 

	"""Cents to ratio."""

	return np.power(2, c/1200.0)


def freq_to_midi(f): 

	"""Frequency to midi note number."""

	return 69.0 + 12.0 * np.log2(f/440.0)


def midi_to_freq(m): 

	"""Midi note number to frequency."""

	return np.power(2, (m-69.0)/12.0) * 440.0 if m!= 0.0 else 0.0


def midi_to_cents(m):

    """Split 12tet and cents."""
    
    p = np.round(m)
    c = (m - p)* 100
   
    return p,c


# FFT helpers ---------------------------------------------------------------- #

def bin_to_freq(b, p): 

    """FFT bin to frequency."""

    return b * float(['sr']) / float(p['n'])


def freq_to_bin(f, p): 

    """Frequency to FFT bin."""

    return np.round(f/(float(p['sr'])/float(p['n']))).astype('int')


def frame_to_sec(f, p):

    """Frame to seconds."""

    return f * float(p['hop']) / float(p['sr'])


def sec_to_frame(s, p, trunc='floor'):

    """Seconds to frame.
  
    trunc = 'round', 'floor', 'ceil'

    """

    if trunc == 'round':
      trunc = np.round
    elif trunc == 'floor':
      trunc = np.floor
    elif trunc == 'ceil':
      trunc = np.ceil
    elif trunc == None:
      trunc = lambda x: x

    return trunc((s * float(p['sr'])) / float(p['hop']))


# audio dsp ------------------------------------------------------------------ #

def normalize(x):

    """Normalize waveform."""

    return x/np.max(np.abs(x)) 


# numbers -------------------------------------------------------------------- #

def scale(x, from_lo=None, from_hi=None, to_lo=0, to_hi=1, clip=False):

    """Scale array."""

    if from_lo is None: from_lo = np.min(x)
    if from_hi is None: from_hi = np.max(x)

    out = to_lo + (to_hi - to_lo) * (x - from_lo) / float(from_hi - from_lo)
    
    return out if not clip else np.clip(out, min([to_lo, to_hi]), max([to_hi, to_lo]))
