import joblib
import mysql.connector

# Load model and vectorizer
loaded_model = joblib.load('models/complaint_classifier_model.joblib')
vectorizer = joblib.load('models/vectorizer.joblib')

topic_names = {
    0: "Bank Account services",
    1: "Credit card or prepaid card",
    2: "Others",
    3: "Theft/Dispute Reporting",
    4: "Mortgage/Loan"
}

print("AI Complaint Classifier is ready! Type 'exit' to quit.\n")

while True:
    new_complaint = input("Enter a new complaint: ")
    if new_complaint.lower() == 'exit':
        print("Exiting AI Complaint Classifier. Goodbye!")
        break

    try:
        X_new = vectorizer.transform([new_complaint])
        predicted_index = loaded_model.predict(X_new)[0]
        predicted_name = topic_names.get(predicted_index, "Unknown Topic")
        print(f"Predicted Topic: '{predicted_name}'")
    except Exception as e:
        print(f"❌ Prediction Error: {e}")
        continue

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="peeuparth",
            database="complaint_db"
        )
        cursor = db.cursor()
        sql = "INSERT INTO conversation_logs (user_query, predicted_topic) VALUES (%s, %s)"
        val = (new_complaint, predicted_name)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        print("Interaction logged to database.\n")
    except Exception as e:
        print(f"❌ Error logging to database: {e}\n")
