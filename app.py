import streamlit as st
import pandas as pd
import pickle

# Cache the model and encoder loading functions
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkt", "rb"))

@st.cache_resource
def load_encoder():
    return pickle.load(open("encoder.pkt", "rb"))

# Load data
df = pd.read_csv('Data_change.csv')

# Display the image
st.image('./Photos/photo2.jpg', use_column_width=True)

# Title styling
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
state = st.selectbox('Select State', df['State'].unique())

# Filter options based on selected state
districts = df[df['State'] == state]['District'].unique()
district = st.selectbox('Select District', districts)

markets = df[df['District'] == district]['Market'].unique()
market = st.selectbox('Select Market', markets)

commodities = df[df['Market'] == market]['Commodity'].unique()
commodity = st.selectbox('Select Commodity', commodities)

varieties = df[df['Commodity'] == commodity]['Variety'].unique()
variety = st.selectbox('Select Variety', varieties)

grades = df[df['Variety'] == variety]['Grade'].unique()
grade = st.selectbox('Select Grade', grades)

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

# Handle submission and display the response
if submit:
    new_data = pd.DataFrame({
        'State': [state], 
        'District': [district], 
        'Market': [market], 
        'Commodity': [commodity], 
        'Variety': [variety], 
        'Grade': [grade]
    })

    st.write("Data for prediction:", new_data)

    encoder = load_encoder()
    new_data_encoded = encoder.transform(new_data)

    model = load_model()
    predicted_price = model.predict(new_data_encoded)

    # Display the result
    st.subheader(f"**Predicted Price: ₹{predicted_price[0]:.2f}**")
