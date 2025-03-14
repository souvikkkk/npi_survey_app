def predict_best_doctors(input_time, data_path):
    import joblib
    import os
    import pandas as pd
    from preprocess import load_and_clean_data

    MODEL_PATH = "survey_model.pkl"

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Trained model not found. Please run model.py first.")

    print(f"🔄 Loading dataset from {data_path}...")
    df = load_and_clean_data(data_path)

    print("✅ Dataset loaded successfully!")
    
    # Load trained model
    print(f"🔄 Loading trained model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)

    input_hour = int(input_time.split(':')[0])
    print(f"🔍 Searching for doctors active at {input_hour}:00...")

    df['Login Hour'] = df['Login Time'].dt.hour
    df['Logout Hour'] = df['Logout Time'].dt.hour

    # Debug: Print the number of doctors in dataset
    print(f"📊 Total doctors in dataset: {len(df)}")

    filtered_df = df[(df['Login Hour'] <= input_hour) & (df['Logout Hour'] >= input_hour)]

    # Debug: Print the number of filtered doctors
    print(f"🩺 Doctors available at {input_hour}: {len(filtered_df)}")

    if filtered_df.empty:
        print("❌ No doctors found for this time slot!")
        return []

    # Prepare data for prediction
    X = filtered_df[['Login Hour', 'Logout Hour', 'Session Duration', 'Count of Attempts']]
    
    predictions = model.predict(X)

    # Debug: Count predicted positive responses
    num_predicted_doctors = sum(predictions)
    print(f"✅ Doctors predicted to attend survey: {num_predicted_doctors}")

    return filtered_df.loc[predictions == 1, 'NPI'].tolist()
