# AI Flight Copilot ✈️ (飞行模拟器 AI 副驾驶)

**AI Flight Copilot** is an intelligent, voice-interactive virtual copilot designed for flight simulators (currently supporting **X-Plane 11/12**). Powered by advanced Large Language Models (LLMs) like OpenAI GPT-4o and Whisper, it reads real-time aircraft telemetry (altitude, speed, heading, pitch, roll) and acts as your professional aviation companion. You can talk to it naturally via a push-to-talk interface, ask for flight data, or request situational advice, and it will respond intelligently with synthesized voice.

**AI Flight Copilot (飞行模拟器 AI 副驾驶)** 是一款专为飞行模拟游戏（目前支持 **X-Plane 11/12**）设计的智能语音交互虚拟副驾驶。它由强大的大型语言模型（如 OpenAI GPT-4o 和 Whisper）驱动，能够实时读取飞机的遥测数据（高度、速度、航向、俯仰角、滚转角），并作为您的专业飞行伴侣。您可以通过“一键发言 (Push-to-Talk)”界面自然地与它对话，询问飞行数据或寻求情景建议，它将结合当前飞行状态给出专业的回答，并通过语音播报给您。

## Features (功能特点)
- **Real-time Telemetry (实时数据读取)**: Uses XPlaneConnect to read live aircraft data.
- **Voice Interaction (语音交互)**: Push-to-Talk (Spacebar) to record your voice.
- **Speech-to-Text (语音识别)**: Highly accurate transcription via Whisper API.
- **Context-Aware AI (上下文感知 AI)**: Injects flight telemetry into the GPT prompt for accurate aviation responses.
- **Text-to-Speech (语音合成)**: Natural sounding copilot voice responses.

## Quick Start (快速开始)
1. Install [NASA XPlaneConnect Plugin](https://github.com/nasa/XPlaneConnect/releases) in your X-Plane `Resources/plugins` folder.
2. Rename `.env.example` to `.env` and add your `OPENAI_API_KEY`. (将 `.env` 文件中的 API Key 替换为您自己的)。
3. Install Python dependencies: `pip install -r requirements.txt`.
4. Run the copilot: `python main.py`.
5. Hold **Space** to talk to your copilot! (按住空格键开始对话！)
