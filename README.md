# Gemini Health App

This is a Streamlit web application that uses Google Gemini AI to analyze food images and provide nutritional information, including calorie counts and a health assessment.

## Features

- Upload an image of food items.
- Analyze the uploaded image to get a breakdown of the calories for each food item.
- Provide an overall health assessment of the food items in the image.

## Installation

### Prerequisites

- Python 3.7 or higher
- Streamlit
- Google Generative AI
- dotenv

### Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/gemini-health-app.git
    cd gemini-health-app
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up your environment variables:**

    Create a `.env` file in the project directory with the following content:

    ```plaintext
    GOOGLE_API_KEY=your_google_api_key
    ```

5. **Run the application:**

    ```sh
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit app in your web browser. You should see a page titled "Ankit's Health App".
2. Upload an image file (jpg, jpeg, or png) using the file uploader.
3. Click the "Tell me the total calories" button.
4. The app will display the analyzed result, including the calorie count for each food item and an overall health assessment.

## File Structure

```plaintext
gemini-health-app/
│
├── .env.example           # Example of the environment variables file
├── app.py                 # Main application script
├── requirements.txt       # List of dependencies
└── README.md              # This README file
