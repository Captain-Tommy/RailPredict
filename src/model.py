import pandas as pd
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import random
from datetime import datetime, timedelta

class WaitlistPredictor:
    def __init__(self):
        if os.path.exists('wl_prediction_model.pkl'):
            self.model = joblib.load('wl_prediction_model.pkl')
            print("Loaded saved model.")
        else:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            print("Initialized new model (untrained).")
        
    def generate_synthetic_data(self, num_samples=1000):
        """
        Generates synthetic historical data for training.
        Simulates the logic: 
        - High WL + Short Duration = Low Chance
        - Low WL + Long Duration = High Chance
        """
        print(f"Generating {num_samples} synthetic records for training...")
        
        data = []
        for _ in range(num_samples):
            days_to_journey = random.randint(1, 120)
            current_wl = random.randint(1, 400)
            total_seats = 1000 # Assume constant for simplicity
            is_weekend = random.choice([0, 1])
            is_holiday = random.choice([0, 1])
            
            # Logic to determine if it eventually confirmed (Target)
            # Probability decreases as WL increases and Days decrease
            
            # Base probability
            prob = 1.0
            
            # Penalties
            prob -= (current_wl / 200) # Higher WL -> Lower prob
            prob += (days_to_journey / 100) # More time -> Higher prob
            
            if is_weekend: prob -= 0.1
            if is_holiday: prob -= 0.2
            
            # Clamp
            prob = max(0, min(1, prob))
            
            is_confirmed = 1 if random.random() < prob else 0
            
            data.append({
                'days_to_journey': days_to_journey,
                'current_wl': current_wl,
                'is_weekend': is_weekend,
                'is_holiday': is_holiday,
                'is_confirmed': is_confirmed
            })
            
        return pd.DataFrame(data)

    def train(self):
        df = self.generate_synthetic_data()
        
        X = df[['days_to_journey', 'current_wl', 'is_weekend', 'is_holiday']]
        y = df['is_confirmed']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training Random Forest Model...")
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"Model Trained. Accuracy: {accuracy:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, predictions))
        
        # Save model
        joblib.dump(self.model, 'wl_prediction_model.pkl')
        print("Model saved to wl_prediction_model.pkl")

    def predict(self, days_to_journey, current_wl, is_weekend=0, is_holiday=0):
        # Load if not loaded (omitted for simplicity, assuming instance usage)
        features = pd.DataFrame([{
            'days_to_journey': days_to_journey,
            'current_wl': current_wl,
            'is_weekend': is_weekend,
            'is_holiday': is_holiday
        }])
        
        prob = self.model.predict_proba(features)[0][1]
        
        # Generate structured factors
        factors = []
        
        # 1. Waitlist Factor
        wl_impact = "Neutral"
        wl_color = "gray"
        if current_wl > 100:
            wl_impact = "High Negative"
            wl_color = "red"
        elif current_wl > 50:
            wl_impact = "Negative"
            wl_color = "orange"
        elif current_wl < 20:
            wl_impact = "Positive"
            wl_color = "green"
            
        factors.append({
            "name": "Current Waitlist",
            "value": str(current_wl),
            "impact": wl_impact,
            "color": wl_color
        })
        
        # 2. Time Factor
        time_impact = "Neutral"
        time_color = "gray"
        if days_to_journey < 3:
            time_impact = "High Negative"
            time_color = "red"
        elif days_to_journey < 10:
            time_impact = "Negative"
            time_color = "orange"
        elif days_to_journey > 30:
            time_impact = "Positive"
            time_color = "green"
            
        factors.append({
            "name": "Days to Journey",
            "value": f"{days_to_journey} Days",
            "impact": time_impact,
            "color": time_color
        })
        
        # 3. Timing Factor (Weekend/Holiday)
        if is_weekend:
            factors.append({
                "name": "Travel Day",
                "value": "Weekend",
                "impact": "Negative",
                "color": "orange"
            })
        else:
            factors.append({
                "name": "Travel Day",
                "value": "Weekday",
                "impact": "Positive",
                "color": "green"
            })
            
        if is_holiday:
            factors.append({
                "name": "Season",
                "value": "Holiday",
                "impact": "High Negative",
                "color": "red"
            })
            
        # 4. Cancellation Analysis (New)
        # Assumptions for estimation
        assumed_total_seats = 1000
        assumed_rac_seats = 100
        
        # For CNF
        needed_cnf = current_wl
        pct_cnf = (needed_cnf / assumed_total_seats) * 100
        
        cnf_impact = "Low Difficulty"
        cnf_color = "green"
        if pct_cnf > 15:
            cnf_impact = "Impossible"
            cnf_color = "red"
        elif pct_cnf > 5:
            cnf_impact = "Hard"
            cnf_color = "orange"
            
        factors.append({
            "name": "Cancellations for CNF",
            "value": f"{needed_cnf} ({pct_cnf:.1f}% of train)",
            "impact": cnf_impact,
            "color": cnf_color
        })
        
        # For RAC
        needed_rac = max(0, current_wl - assumed_rac_seats)
        if needed_rac > 0:
            pct_rac = (needed_rac / assumed_total_seats) * 100
            
            rac_impact = "Low Difficulty"
            rac_color = "green"
            if pct_rac > 10:
                rac_impact = "Hard"
                rac_color = "red"
            elif pct_rac > 3:
                rac_impact = "Moderate"
                rac_color = "orange"
                
            factors.append({
                "name": "Cancellations for RAC",
                "value": f"{needed_rac} ({pct_rac:.1f}% of train)",
                "impact": rac_impact,
                "color": rac_color
            })
        else:
             factors.append({
                "name": "Cancellations for RAC",
                "value": "0 (Already in RAC range)",
                "impact": "Guaranteed",
                "color": "green"
            })
            
        return prob, factors
