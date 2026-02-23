Real-Time Fraud Detection System
Overview
I built this project to move beyond basic data analysis and create a system that reflects how fraud detection works in a professional environment. The goal was to build a tool that doesn't just predict fraud in a notebook, but provides a live dashboard and a permanent record of every decision made.
The Data Challenge
The biggest hurdle with this dataset was the extreme imbalance. Only 0.17% of the transactions were fraudulent. If I had trained the model on the raw data, it would have learned to simply guess "Normal" every time to achieve high accuracy. To fix this, I used SMOTE (Synthetic Minority Over-sampling Technique) during the training phase to create synthetic examples of fraud, forcing the model to actually learn the patterns of suspicious behavior.
The Trillion-Dollar Lesson
A key learning point during testing was the "Amount" problem. I noticed that entering a trillion-dollar transaction would often get approved if the behavioral features (V1-V28) were set to normal.
This taught me that in financial AI, the raw dollar amount is often less important than the behavioral indicators. I had to experiment with specific features like V14 and V17 to understand which ones were the true "red flags" that trigger the model's alarm.
How the System Works
The project is split into three main parts:
Training: I used a Random Forest classifier and handled scaling with RobustScaler to manage outliers in transaction amounts.
The Dashboard: Built with Streamlit, this allows a user to input transaction details and get an instant risk probability.
Audit Log: Every transaction checked through the dashboard is automatically saved to an SQLite database (fraud_audit.db). This ensures there is a persistent record of every prediction for security auditing.
Project Structure
main.ipynb: The development notebook where I handled data cleaning, scaling, and training.
app.py: The live dashboard code.
fraud_detection_model.pkl & scaler.pkl: The saved model and scaling parameters.
fraud_audit.db: The local SQL database used for logging alerts.
How to Run
Install the necessary libraries: pip install pandas scikit-learn streamlit joblib imbalanced-learn
Download the creditcard.csv dataset from Kaggle and place it in the project folder.
Launch the dashboard by running: streamlit run app.py

