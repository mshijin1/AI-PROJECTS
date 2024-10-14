
# Import necessary modules
import streamlit as st
import os
import google.generativeai as genai
from api_key import google_key

# Api key configuration (replace with your actual API key or set it in environment)
genai.configure(api_key=google_key)

# Set up the model configuration
generation_config = {
  "temperature": 0.9,  # Adjust to control randomness
  "top_p": 0.95,       # Controls diversity of the output
  "max_output_tokens": 2048,  # Maximum token length for the generated blog post
  "response_mime_type": "text/plain",
}

# Set up the model
model = genai.GenerativeModel(
  model_name="gemini-1.0-pro",  # Adjust based on the available model
  generation_config=generation_config
)

# Set the layout of the page as wide
st.set_page_config(layout="wide")

# Title of our project
st.title("BlogCraft: Your AI Writing Companion")

# Create subheader
st.subheader("Craft the perfect blog with the help of AI. BlogCraft is your AI blog companion.")

# Sidebar for user input
with st.sidebar:
    st.title("Input your Blog Details")
    st.subheader("Enter details of the blog you want to generate")

    # User inputs from the user
    # Blog title
    blog_title = st.text_input("Blog Title")

    # Keywords input
    keywords = st.text_area("Keywords (comma-separated)")

    # Number of words
    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=50)

    # Number of images (if applicable)
    num_image = st.number_input("Number of images", min_value=1, max_value=5, step=1)

    # Submit button
    submit_button = st.button("Generate Blog")

# When the user clicks the submit button
if submit_button:
    if not blog_title or not keywords:
        st.error("Please fill in both the blog title and keywords to generate the blog.")
    else:
        # Construct the prompt for the generative AI model
        prompt = f'Generate a blog post with the title "{blog_title}" using the following keywords: {keywords}. The blog should be approximately {num_words} words in length and original, informative, and engaging.'

        # Generate the blog content using Google Generative AI
        chat_session = model.start_chat(
            history=[{
                "role": "user",
                "parts": [prompt]
            }]
        )
        
        # Get the response from the model
        response = chat_session.send_message("Generate a blog")
        
        # Display the generated blog in Streamlit
        st.subheader(f"Generated Blog: {blog_title}")
        st.write(response.text)

        # Optionally, allow the user to download the blog
        st.download_button(label="Download Blog", data=response.text, file_name="generated_blog.txt", mime="text/plain")
