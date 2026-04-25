import time
import keyboard
from dotenv import load_dotenv
from simulator_connectors import XPlaneConnector
from ai_copilot import AICopilot
from voice_module import VoiceModule

load_dotenv()

def main():
    print("Initializing AI Copilot for X-Plane...")
    
    # Initialize modules
    sim = XPlaneConnector()
    copilot = AICopilot()
    voice = VoiceModule()
    
    print("Copilot initialized. Connecting to X-Plane...")
    
    # Wait for connection
    while not sim.is_connected():
        try:
            telemetry = sim.get_telemetry()
            if telemetry:
                print("Connected to X-Plane successfully!")
                break
        except Exception as e:
            pass
        print("Waiting for X-Plane connection...")
        time.sleep(2)
        
    print("\n--- AI Copilot Ready ---")
    print("Press and hold the 'Space' bar to talk to your copilot.")
    print("Release the 'Space' bar to send the message.")
    print("Press 'Ctrl+C' to exit.")
    
    try:
        while True:
            # Check for push-to-talk (Space bar)
            if keyboard.is_pressed('space'):
                print("\n[Listening... Speak now]")
                # Record audio while space is held
                audio_file = voice.record_audio_until_key_release('space')
                if audio_file:
                    print("\n[Transcribing...]")
                    user_text = voice.transcribe_audio(audio_file)
                    
                    if user_text:
                        print(f"You: {user_text}")
                        
                        # Get current telemetry
                        telemetry = sim.get_telemetry()
                        
                        # Get response from AI
                        print("\n[Copilot is thinking...]")
                        ai_response = copilot.get_response(user_text, telemetry)
                        print(f"Copilot: {ai_response}")
                        
                        # Speak response
                        voice.speak_text(ai_response)
                    else:
                        print("\n[Could not understand audio]")
            
            # Add a small sleep to prevent high CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting AI Copilot.")
    finally:
        sim.close()

if __name__ == "__main__":
    main()
