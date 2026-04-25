import os
import wave
import pyaudio
import keyboard
import time
from openai import OpenAI
import pygame # Better for playing audio files

class VoiceModule:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Audio recording parameters
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000 # Whisper prefers 16kHz
        self.p = pyaudio.PyAudio()
        
        # Initialize pygame mixer for playback
        pygame.mixer.init()

    def record_audio_until_key_release(self, key='space', filename="temp_record.wav"):
        stream = self.p.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk)
        
        frames = []
        
        # Wait a tiny bit to ensure the key press is registered fully
        time.sleep(0.1)
        
        # Record while the key is pressed
        while keyboard.is_pressed(key):
            data = stream.read(self.chunk)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        # Save to file
        if len(frames) > 5: # Make sure we actually recorded something
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            return filename
        return None

    def transcribe_audio(self, filename):
        if not self.client:
            return None
            
        try:
            with open(filename, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def speak_text(self, text, filename="temp_speech.mp3"):
        if not self.client:
            return
            
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy", # alloy, echo, fable, onyx, nova, shimmer
                input=text
            )
            
            response.stream_to_file(filename)
            
            # Play the audio
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # Free the file so it can be overwritten next time
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f"TTS error: {e}")
