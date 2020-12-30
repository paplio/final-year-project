
import wave
import moviepy.editor as mp
import numpy as np
import os
import srt

def convert(filename):
  clip = mp.VideoFileClip(os.path.join("static/", filename))
  clip.audio.write_audiofile("audio_extract.wav")

  os.system("deepspeech --model deepspeech-0.9.1-models.pbmm --scorer deepspeech-0.9.1-models.scorer --audio audio_extract.wav >> recognized.txt")

  def gettimestamp(secs):
    hrs=int(secs/3600)
    secs=secs%3600
    min=int(secs/60)
    secs=int(secs%60)
    print('{0}'.format(str(hrs).zfill(2))+':'+'{0}'.format(str(min).zfill(2))+':'+'{0}'.format(str(secs).zfill(2))+",000")
    return '{0}'.format(str(hrs).zfill(2))+':'+'{0}'.format(str(min).zfill(2))+':'+'{0}'.format(str(secs).zfill(2))+",000"

  f = open("recognizedsrtfrmt.srt", "w")
  t = open("recognized.txt", "r")
  thingy = list(t)
  wordsInFile = str(thingy[0]).split()
  seqs = []
  for i in range(0, len(wordsInFile), 10):
    try:
      seqs.append(str(wordsInFile[i: i+10]))
    except: 
      seqs.append(str(wordsInFile[i:])) #when lesser than 10 words are left


  #write srt as text file
  audiolen=clip.duration
  x = 0
  offset=0
  seq=1
  while x<len(seqs):
    leng=5 if audiolen-offset>5 else audiolen-offset
    f.write(str(seq)+"\n")
    seq=seq+1
    f.write(gettimestamp(int(offset))+" -->"+" "+gettimestamp(int(offset+leng))+"\n")
    f.write(str(seqs[x]) + "\n") 
    x = x+1
    offset=offset+leng
    f.write("\n")
  f.close()

  outfile = os.path.join("static/", "subbed-"+filename)
  os.system("ffmpeg -i recognizedsrtfrmt.srt subtitles.ass")
  os.system('ffmpeg -i ' + os.path.join("static/", filename) + " -vf ass=subtitles.ass " + outfile)

  #cleanup
  os.system("rm subtitles.ass")
  os.system("rm recognized.txt")
  os.system("rm recognizedsrtfrmt.srt")
  os.system("rm audio_extract.wav")

if __name__ == "__main__":
  convert("palebluedot.mp4")
