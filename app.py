import streamlit as st
import pandas as pd
import pickle

with open('./model.pkl', 'rb') as file:
    model = pickle.load(file)
with open('./encoder.pkl', 'rb') as file:
    encoder = pickle.load(file)

df = pd.read_csv('Data_change.csv')

st.image('./Photos/photo2.jpg',use_column_width=True)

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 40px;
    }
    </style>
    <div class="title">Commodity Price Prediction</div>
    """,
    unsafe_allow_html=True
)

# Collect user input
state = st.selectbox('Select State', ['Tamil Nadu', 'Uttar Pradesh', 'Maharashtra', 'West Bengal',
       'Madhya Pradesh', 'Haryana', 'Punjab', 'Kerala', 'Telangana', 'Tripura',
       'Gujarat', 'Odisha', 'Himachal Pradesh', 'Rajasthan', 'Bihar',
       'Chandigarh', 'Uttrakhand', 'Karnataka', 'Chattisgarh',
       'Andhra Pradesh'])
district = st.selectbox('Select District',list(df[df['State'] == state].value_counts('District').keys()))
market = st.selectbox('Select Market',list(df[df['State'] == state].value_counts('Market').keys()))
commodity = st.selectbox('Select Commodity',list(df[df['State'] == state].value_counts('Commodity').keys()))
variety = st.selectbox('Select Variety',list(df[df['State'] == state].value_counts('Variety').keys()))
grade = st.selectbox('Select Grade',list(df[df['State'] == state].value_counts('Grade').keys())) 



# Center the button using custom CSS
st.markdown(
    """
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True
)

# Create the centered button
submit = st.button("Submit")

# Handle submission and display the response box
if submit:
    # Assuming you have variables `state`, `district`, `market`, `commodity`, `variety`, and `grade`
    new_data = pd.DataFrame({
        'State': [state], 
        'District': [district], 
        'Market': [market], 
        'Commodity': [commodity], 
        'Variety': [variety], 
        'Grade': [grade]
    })

    # Perform further actions with new_data if needed
    st.write("Data for prediction:", new_data)

    # Center the response box using custom CSS
    st.markdown(
        """
        <style>
        div.response-box {
            display: block;
            margin: 20px auto;
            padding: 15px;
            border-radius: 10px;
            background-color: #f0f0f0;
            width: 50%;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True
    )

    new_data_encoded = encoder.transform(new_data)

    # Predict min and max prices
    predicted_price = model.predict(new_data_encoded)

    # Display the results
    st.subheader(f"**Predicted Price: ₹**{predicted_price[0]}")
