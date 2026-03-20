import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

def train():
    print("Loading dataset...")
    df = pd.read_csv("ndss_traffic_dataset.csv")
    
    X = df[["packet_count", "packet_size", "entropy"]]
    y = df["label"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc*100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, preds))
    
    # Save the model
    with open("ndss_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved to ndss_model.pkl")

if __name__ == "__main__":
    train()
