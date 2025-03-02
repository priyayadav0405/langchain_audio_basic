import streamlit as st
from audio_recorder_streamlit import audio_recorder
import base64
import whisper
import os
from langchain_groq import ChatGroq
from gtts import gTTS
from PIL import Image,ImageSequence
import time

os.environ["GROQ_API_KEY"] = "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"
# Initialize the ChatGroq model
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.6, max_tokens=500)

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    # page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    
)





def transcribe_audio(audio_file):
    """Transcribe audio using the Whisper model."""
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result["text"]


def fetch_ai_response(input_text):
    """Generates an AI response using ChatGroq."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_text}
    ]
    
    response = llm.invoke(messages)
    
    # Extracting the content from the AI response
    if hasattr(response, 'content'):
        return response.content
    elif 'choices' in response and len(response.choices) > 0:
        return response.choices[0].message.content
    else:
        return "I'm sorry, I couldn't generate a response."


def text_to_audio(ai_response, response_audio_file):
    """Convert text to audio using gTTs and save it to a file."""
    if isinstance(ai_response, str):  # Ensure it's a string
        tts = gTTS(text=ai_response, lang="en")
        tts.save(response_audio_file)
    else:
        raise ValueError("AI response must be a string.")


def create_text_card(text, title="Response"):
    st.markdown(f"""
        <div style="
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
            background-color:rgb(198, 176, 176) 180, 180);
            margin: 10px 0;
            color:#430606;
            text-align:center; 
        ">
            <h4 style="margin-bottom: 10px;">{title}</h4>
            <p style="font-size: 14px; color: #430606;">{text}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
        h1 {
            text-align: center;
            background-color:rgb(220, 169, 107);
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
    <style>
        /* Style the audio recorder button */
        *{
            background-color:  #fdc7bd;  /* Tomato color */
            color: black;
            font-size: 18px;
            
            border-radius: 12px;
            align-items:center;
            
        }

    </style>
""", unsafe_allow_html=True)







def auto_play_audio(audio_file):
    """Automatically play the audio file."""
    with open(audio_file,"rb") as f:
        audio_bytes = f.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f'<audio src="data:audio/mp3;base64,{base64_audio}" controls autoplay></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

def main():
    st.title("🎤🎤🎤 Aurora SpeakEasy 💬")
    st.write("Hi there! Click on the voice recorder to interact with me. How can I assist you?")
    recorded_audio = audio_recorder(key="audio_recorder_1")
    
    

    if recorded_audio:
        audio_file = "audio.mp3"
        with open(audio_file, "wb") as f:
            f.write(recorded_audio)

        st.write("Processing your audio....")

        

        # Transcribe the audio
        transcribed_text = transcribe_audio(audio_file)
        create_text_card(transcribed_text, "Transcribed Text")

        # Get AI response
        ai_response = fetch_ai_response(transcribed_text)
        response_audio_file = "response_audio.mp3"
        text_to_audio(ai_response, response_audio_file)
        gif_placeholder = st.empty()
        create_text_card(ai_response, "AI Response")
        

        gif = Image.open("speaking.gif")  # Replace with the path to your GIF
        gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

        # Animate GIF while audio plays
        def animate_gif():
            while True:
                for frame in gif_frames:
                    gif_placeholder.image(frame)
                    time.sleep(0.1)  # Adjust for smoother animation
                    if not st.session_state["audio_playing"]:
                        return

        # Set session state to track audio
        if "audio_playing" not in st.session_state:
            st.session_state["audio_playing"] = True

        st.session_state["audio_playing"] = True
        auto_play_audio(response_audio_file)
        animate_gif()  # Start GIF animation
        
        st.session_state["audio_playing"] = False
        st.audio(response_audio_file, format="audio/mp3")
        


if __name__ == "__main__":
    main()
