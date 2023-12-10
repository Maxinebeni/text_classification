import streamlit as st
from bs4 import BeautifulSoup
import requests
import joblib
import validators  # Import the validators library to check if the input is a valid URL

# Define a custom exception for model prediction errors
class ModelPredictionError(Exception):
    pass

# Load your trained model
model = joblib.load('htext_classification_model.pkl')

# Function to extract text from a URL using Beautiful Soup
def get_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if "example1.com" in url: # Check if the URL contains "example1.com"
            paragraphs = soup.find_all('p') # Adjust this based on the HTML structure of the articles for "example1.com"
        elif "example2.com" in url: # Check if the URL contains "example2.com"
            paragraphs = soup.find_all('div') # Adjust this based on the HTML structure of the articles for "example2.com"
        else:
            paragraphs = soup.find_all('p') # Adjust this based on the HTML structure of the articles for any other domain
            
        text = ' '.join([paragraph.get_text() for paragraph in paragraphs])
        
        # Check if text is empty after extraction
        if not text.strip():
            raise ValueError("Unable to determine content from the website.")
        
        return text
    except Exception as e:
        st.error(f"Error retrieving content from the URL: {str(e)}")
        return None

# Streamlit app
def main():
    
    custom_css = """
    <style>
        body {
            background-image: url('background image.jpg'); /* Replace with your background image URL */
            background-size: cover;
        }
        .logo {
            max-width: 50px; /* Adjust the width of your logo */
            margin-bottom: 10px;
            height: 50px; /* Adjust this based on your desired logo height */
            justify-content: center;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Add logo
    st.image('logo.jpg', width=150, output_format='JPG', use_column_width=False)

    st.write("\n\n")

    st.title("Health Article Repository")

    # Input box for the topic of the article
    topic = st.text_input("Topic of your article (e.g., Cancer, HIV/AIDS):")

    # User input for the URL
    url = st.text_input("Enter the URL of the article:")

    # Check if the user has provided a URL
    if st.button("POST"):
        if url:
            # Check if the input is a valid URL
            if not validators.url(url):
                st.error("Non-URL text entered. Please enter a valid URL and try again.")
                return
            
            try:
                # Extract text from the URL
                article_text = get_text_from_url(url)

                # Check if text extraction was successful
                if article_text:
                    # Use the model to make predictions
                    prediction = model.predict([article_text])[0]

                    # Display the appropriate message
                    if prediction == 1.0:
                        st.success(f"Thank you for adding to the Health Clique! Your article on '{topic}' has been saved.")
                    else:
                        st.warning(f"Sorry, your article on '{topic}' is not health-related and cannot be saved. Try again.")

            except ValueError as ve:
                st.error(f"Error: {ve}")
            except ModelPredictionError as mpe:
                st.error(f"Model Prediction Error: {str(mpe)}")
            except Exception as e:
                st.error("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
