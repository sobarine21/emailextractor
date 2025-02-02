import easyocr
import re
import pandas as pd
import streamlit as st
from io import BytesIO

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Initialize for English language

# Regular expression patterns for extracting mobile numbers and email addresses
mobile_number_pattern = r'\+?\d{1,4}?[\s-]?\(?\d{1,3}?\)?[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,9}'
email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

# Function to extract mobile numbers and email addresses from text
def extract_contacts(text):
    mobile_numbers = re.findall(mobile_number_pattern, text)
    email_addresses = re.findall(email_pattern, text)
    return mobile_numbers, email_addresses

# Function to process an uploaded image and extract mobile numbers and email addresses
def process_image(image_bytes):
    result = reader.readtext(image_bytes)

    # Extract text from OCR result
    text = " ".join([item[1] for item in result])
    
    # Extract mobile numbers and email addresses from the text
    mobile_numbers, email_addresses = extract_contacts(text)
    
    return mobile_numbers, email_addresses

# Function to process multiple images uploaded by the user
def extract_from_images(uploaded_files):
    all_contacts = []
    
    for uploaded_file in uploaded_files:
        # Read image data
        image_bytes = uploaded_file.read()

        # Extract contacts from the image
        mobile_numbers, email_addresses = process_image(image_bytes)
        
        # Store the results
        all_contacts.append({
            'image': uploaded_file.name,
            'mobile_numbers': ', '.join(mobile_numbers),  # Join multiple numbers with commas
            'email_addresses': ', '.join(email_addresses)  # Join multiple emails with commas
        })
    
    return all_contacts

# Streamlit app to upload files and download CSV
def main():
    st.title("Contact Extractor from Images")
    
    # Upload files (images)
    uploaded_files = st.file_uploader("Upload images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.write(f"Found {len(uploaded_files)} files.")
        
        # Extract contacts from the uploaded images
        contacts = extract_from_images(uploaded_files)
        
        # Convert to DataFrame for display
        contacts_df = pd.DataFrame(contacts)
        
        # Display the contacts in the app
        st.subheader("Extracted Contacts")
        st.dataframe(contacts_df)
        
        # Provide download button for CSV
        if not contacts_df.empty:
            csv_data = contacts_df.to_csv(index=False)
            st.download_button(
                label="Download CSV of Extracted Contacts",
                data=csv_data,
                file_name="extracted_contacts.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
