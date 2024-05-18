from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
import av

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.frame = None

    def recv(self, frame):
        self.frame = frame.to_image()
        return frame

    def get_image(self):
        return self.frame

st.set_page_config(page_title="Gemini Health App")

st.header("Ankit's Health App")

# File uploader for image input
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Button to open camera and capture image
if 'webrtc_ctx' not in st.session_state:
    st.session_state.webrtc_ctx = None

or_text=st.text("or")
open_camera = st.button("Capture from Camera")

if open_camera or st.session_state.webrtc_ctx:
    st.session_state.webrtc_ctx = webrtc_streamer(
        key="camera",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}),
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=VideoProcessor,
        async_processing=True,
    )

# Button to submit the input and get the response
submit = st.button("Tell me the total calories")

input_prompt = """
You are an expert nutritionist. Analyze the food items in the image
and calculate the total calories. Also, provide details of every food item with calorie intake
in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

Finally, mention if the food is healthy or not.
"""

if submit:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.subheader("The Response is:")
        st.write(response)
    elif st.session_state.webrtc_ctx and st.session_state.webrtc_ctx.state.playing:
        frame = st.session_state.webrtc_ctx.video_processor.get_image()
        if frame is not None:
            buffered = BytesIO()
            frame.save(buffered, format="JPEG")
            image_data = [
                {
                    "mime_type": "image/jpeg",
                    "data": buffered.getvalue()
                }
            ]
            response = get_gemini_response(input_prompt, image_data)
            st.subheader("The Response is:")
            st.write(response)
        else:
            st.error("No image captured from camera.")
    else:
        st.error("Please upload an image or capture one using the camera.")

# Ensure proper spacing and clean layout
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)
