import os
from openai import OpenAI

class AICopilot:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("WARNING: OPENAI_API_KEY not found in environment variables.")
            
        self.client = OpenAI(api_key=self.api_key)
        
        self.system_prompt = """
You are an expert AI Copilot for a flight simulator (X-Plane).
Your job is to assist the pilot with professional, concise, and accurate aviation information.
You will be provided with the current telemetry of the aircraft. 
Use this data to answer the pilot's questions or provide situational awareness.
Respond naturally like a real human copilot. Keep responses relatively brief so they can be spoken quickly over the radio/intercom.
"""
        # Keep a brief memory of the conversation
        self.chat_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _format_telemetry(self, telemetry):
        if not telemetry:
            return "Telemetry data is currently unavailable."
            
        telemetry_str = "Current Aircraft Telemetry:\n"
        for key, value in telemetry.items():
            telemetry_str += f"- {key}: {value}\n"
        return telemetry_str

    def get_response(self, user_message, telemetry):
        if not self.api_key:
            return "API key not configured. Cannot process request."
            
        # Inject telemetry as a system message to provide context for this turn
        context_msg = {
            "role": "system", 
            "content": self._format_telemetry(telemetry)
        }
        
        # Add user message
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Build messages list for the API call
        messages = self.chat_history.copy()
        # Insert context right before the latest user message
        messages.insert(-1, context_msg)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            
            ai_text = response.choices[0].message.content
            
            # Save AI response to history
            self.chat_history.append({"role": "assistant", "content": ai_text})
            
            # Keep history from growing indefinitely (keep system + last 10 turns)
            if len(self.chat_history) > 21:
                self.chat_history = [self.chat_history[0]] + self.chat_history[-20:]
                
            return ai_text
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "I'm sorry, I encountered an error while trying to think."
