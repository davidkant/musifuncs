import midiutil.MidiFileExt as midiutil
import numpy as np

def export_midi(cooked, pgm=1, filename='lospinos.mid', micromidi=True, percussion=False):

  """Write notes to midi file.

    arguments:
    - cooked: list of cooked notes. note objects must support pitch, ontime, 
      offtime, and voice. time should be in secs, pitch should be in midi pitch 
      number.

    returns:
    - nothing! but writes a midi file.

    todo:
    -> pgm + 1?
    -> do we check from np.isnan an != 0?
    -> velocity!!!

  """

  # init MIDIFile Object
  mf = midiutil.MIDIFile(1) # only 1 track
  
  # init channels
  for i in set([c.voice for c in cooked]):

    # this channel 
    channel = i if not percussion else 9
    # the only track
    track = 0
    # start at the beginning
    time = 0
    # name the track?
    mf.addTrackName(track, time, "music is stupid")
    # tempo is 60!
    mf.addTempo(track, time, 60)
    # set pitch bend range: RPN
    mf.addControllerEvent(track, channel, time, 100, 0)
    # set pitch bend range: RPN
    mf.addControllerEvent(track, channel, time, 101, 0)
    # set pitch bend range: range half step
    mf.addControllerEvent(track, channel, time, 6, 1) 
    # program MINUS 1!!! so matches wiki chart
    # mf.addProgramChange(track, channel, time, pgm-1) 

  # loop through notes
  for note in cooked:

      # check for nan and 0.0
      if note.pitch == -np.inf: continue
      if np.isnan(note.pitch): continue

      # note data
      track = 0
      channel = note.voice if not percussion else 9
      time = note.ontime
      dur = note.offtime - note.ontime
      vol = note.vol
      pitch = int(round(note.pitch))
      cents = int(100*(note.pitch-pitch)) 

      # stuff note
      if micromidi: mf.addPitchBend(track, channel, time, cents)
      mf.addNote(track, channel, pitch, time, dur, vol)
 
  # and write it to disk
  binfile = open(filename, 'wb')
  mf.writeFile(binfile)
  binfile.close()

