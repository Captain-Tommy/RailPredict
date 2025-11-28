from flask import Flask, render_template, request
from src.model import WaitlistPredictor
from src.database import get_db_connection
import os

app = Flask(__name__)

# Initialize predictor
# In a production app, you might want to load the model once at startup
predictor = WaitlistPredictor()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        train_no = request.form['train_no']
        wl_status = int(request.form['wl_status'])
        
        # Date Logic
        journey_date_str = request.form['journey_date']
        from datetime import datetime
        journey_date = datetime.strptime(journey_date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        days_to_journey = (journey_date - today).days
        
        if days_to_journey < 0:
            return render_template('index.html', error="Journey date cannot be in the past!")
        
        # Ensure model is trained/loaded
        # For this demo, we'll just ensure it's trained quickly if no file exists
        if not os.path.exists('wl_prediction_model.pkl'):
            predictor.train()
            
        prob, reasons = predictor.predict(days_to_journey, wl_status)
        percentage = round(prob * 100, 1)
        
        # Fetch Train Details
        conn = get_db_connection()
        train = conn.execute('SELECT * FROM trains WHERE train_number = ?', (train_no,)).fetchone()
        
        # Check if train exists AND has the new details (speed/image)
        # If avg_speed is None, it means it's an old record or incomplete
        if not train or train['avg_speed'] is None:
            print(f"Train {train_no} missing or incomplete. Scraping...")
            # Trigger on-demand scrape
            from src.scraper import RailwayScraper
            scraper = RailwayScraper()
            scraper.scrape_train_schedule(train_no)
            scraper.close()
            # Fetch again
            train = conn.execute('SELECT * FROM trains WHERE train_number = ?', (train_no,)).fetchone()
            
        conn.close()
        
        train_details = {}
        if train:
            train_details = {
                'name': train['train_name'],
                'source': train['source'],
                'dest': train['destination'],
                'speed': train['avg_speed'] if 'avg_speed' in train.keys() else 'N/A',
                'composition': train['coach_composition'] if 'coach_composition' in train.keys() else 'N/A',
                'image': train['image_url'] if 'image_url' in train.keys() else 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Indian_Railways_WAP-4_locomotive.jpg/640px-Indian_Railways_WAP-4_locomotive.jpg'
            }
        else:
            train_details = {
                'name': 'Unknown Train',
                'source': 'N/A',
                'dest': 'N/A',
                'speed': 'N/A',
                'composition': 'N/A',
                'image': ''
            }
        
        # Chart Status Logic
        chart_status = "Not Prepared"
        chart_color = "orange"
        if days_to_journey > 0:
            chart_status = "Not Prepared"
            chart_color = "#d93025" # Red-ish
        else:
            chart_status = "Chart Prepared / In Progress"
            chart_color = "#188038" # Green
            
        return render_template('result.html', 
                               train_no=train_no, 
                               wl_status=wl_status, 
                               days=days_to_journey, 
                               probability=percentage,
                               factors=reasons, 
                               train=train_details,
                               chart_status=chart_status,
                               chart_color=chart_color)
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
