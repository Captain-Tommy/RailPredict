import argparse
from src.database import init_db
from src.scraper import RailwayScraper
from src.model import WaitlistPredictor
from datetime import datetime, timedelta

def main():
    parser = argparse.ArgumentParser(description="Indian Railway Scraper & Predictor")
    parser.add_argument('action', choices=['setup', 'scrape', 'train', 'predict'], help="Action to perform")
    parser.add_argument('--train-no', type=str, help="Train Number (for scrape/predict)")
    parser.add_argument('--wl', type=int, help="Current Waitlist Number (for predict)")
    parser.add_argument('--days', type=int, help="Days to journey (for predict)")
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        init_db()
        
    elif args.action == 'scrape':
        if not args.train_no:
            print("Please provide --train-no")
            return
        scraper = RailwayScraper()
        scraper.scrape_train_schedule(args.train_no)
        
        # Scrape availability for next 7 days
        today = datetime.now()
        for i in range(1, 8):
            journey_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
            scraper.scrape_availability(args.train_no, journey_date)
            
        scraper.close()
        
    elif args.action == 'train':
        predictor = WaitlistPredictor()
        predictor.train()
        
    elif args.action == 'predict':
        if not args.wl or not args.days:
            print("Please provide --wl and --days")
            return
        
        predictor = WaitlistPredictor()
        # Load model logic would go here, but for now we retrain quickly or assume loaded
        # For this demo script, let's just train-then-predict to ensure it works without file IO issues
        predictor.train() 
        
        prob = predictor.predict(args.days, args.wl)
        print(f"\nPrediction for WL{args.wl} with {args.days} days left:")
        print(f"Confirmation Probability: {prob*100:.1f}%")

if __name__ == "__main__":
    main()
