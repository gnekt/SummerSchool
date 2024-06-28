import soundfile as sf
import librosa
import numpy as np 

# Load music
music_path = "./temp/music/0.wav"
music_0, music_sr_0 = sf.read(music_path)

music_path = "./temp/music/1.wav"
music_1, music_sr_1 = sf.read(music_path)

# Load voice
voice_path = "./temp/voice/0.wav"
voice_0, voice_sr_0 = sf.read(voice_path)

voice_path = "./temp/voice/1.wav"
voice_1, voice_sr_1 = sf.read(voice_path)

# Mix music and voice
if music_sr_0 != voice_sr_0:
    # Match sample rate
    music_0 = librosa.resample(music_0, music_sr_0, voice_sr_0)
    
if music_sr_1 != voice_sr_1:
    # Match sample rate
    music_1 = librosa.resample(music_1, music_sr_1, voice_sr_1)
    
if len(music_0) > len(voice_0):
    music_0 = music_0[:len(voice_0)]
else:
    voice_0 = voice_0[:len(music_0)]

if len(music_1) > len(voice_1):
    music_1 = music_1[:len(voice_1)]
else:
    voice_1 = voice_1[:len(music_1)]

# Sum (sample,2) + (sample,) -> (sample,2)
mixed_0 = 2/5 * music_0[:,0].repeat(2).reshape(-1,2) + 3/5 * voice_0.repeat(2).reshape(-1, 2)

mixed_1 = 2/5 * music_1[:,0].repeat(2).reshape(-1,2) + 3/5 * voice_1.repeat(2).reshape(-1, 2)
all = np.concatenate((mixed_0, mixed_1), axis=0)

# Save mixed audio
sf.write("./temp/mixed/0.wav", mixed_0, voice_sr_0)
sf.write("./temp/mixed/1.wav", mixed_1, voice_sr_1)
