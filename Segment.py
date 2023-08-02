import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from PIL import Image

# Load the pre-trained model using pickle
model = pickle.load(open("segment_model.sav", 'rb'))

image = Image.open("pexels-pixabay-264636.jpg")

# Load the label encoder for categorical features (Gender, Device_Type, Order_Priority, Payment_method)
date_encoder = LabelEncoder()  # Replace with the categorical encoder used during training

# Load the label encoder for 'Segment' mapping
segment_mapping = {
    0: 'Lowest-Spending Active Loyal Customers',
    1: 'Churned Best Customers',
    2: 'Good Customers Almost Lost',
    3: 'Platinum Customers',
    4: 'High Spend New Customers',
    5: 'Recent Customers',
    6: 'Lost Cheap Customers',
    7: 'Big Spenders',
    8: 'Others'
}

# Create the Streamlit app
def main():
    st.title("Customer Segmentation")
    st.image(image, width=500)

    # Input feature values from the user
    recency = st.number_input("Recency:", min_value=0)
    frequency = st.number_input("Frequency:", min_value=0)
    monetary = st.number_input("Monetary:", min_value=0)
    g = st.selectbox("Gender", ['Male', 'Female'])  # Categorical feature
    if (g == 'Male'):
        gender = 1
    else: gender = 0
    d = st.selectbox("Device Type", ['Web', 'Desktop'])
    if (d == 'Web'):
        device_type = 1
    else:
        device_type = 0
    quantity = st.number_input("Quantity:", min_value=0)
    discount = st.number_input("Discount:", min_value=0)
    profit =  st.number_input("Profit:", min_value=0)
    priority = st.selectbox("Order Priority",['Critical', 'Low', 'Medium', 'High'])
    if (priority == 'Critical'):
        order_priority = 0
    elif (priority == 'Low'):
        order_priority = 2
    elif (priority == 'Medium'):
        order_priority = 3
    else:
        order_priority = 1
    payment = st.selectbox("Payment Method", ['credit_card', 'money_order', 'e_wallet', 'debit_card'])
    if (payment == 'credit_card'):
        payment_method = 0
    elif (payment == 'money_order'):
        payment_method = 3
    elif (payment == 'e_wallet'):
        payment_method = 2
    else:
        payment_method = 1
   # date1 = st.date_input("First Order Date:")
   # date2 = st.date_input("Last Order Date:")
   # first_date = date_encoder.fit_transform(date1.to_numpy().reshape(-1, 1))
    #last_date = date_encoder.fit_transform(date2.to_numpy().reshape(-1, 1))

    # Create a feature vector based on user input
    user_features = pd.DataFrame({
        'Recency': [recency],
        'Frequency': [frequency],
        'Monetary': [monetary],
        'Gender': [gender],
        'Device_Type': [device_type],
        'Quantity': [quantity],
        'Discount': [discount],
        'Profit': [profit],
        'Order_Priority': [order_priority],
        'Payment_method': [payment_method],
        #'first_date': [first_date],
        #'last_date': [last_date]
    })
    st.write(user_features)
    if st.button("Predict"):
        # Predict the segment for the user input
        predicted_segment = model.predict(user_features)[0]
        st.subheader(f"Customer Segment: :blue[{segment_mapping[predicted_segment]}]")

if __name__ == "__main__":
    main()
