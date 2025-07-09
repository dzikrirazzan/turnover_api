from django.core.management.base import BaseCommand
import pandas as pd
from predictions.ml_utils import TurnoverPredictor, get_model_save_path
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Train turnover ML model from CSV in ml_data/training_data.csv and save to ml_models/'

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'ml_data', 'training_data.csv')
        if not os.path.exists(csv_path):
            # Try alternative path
            csv_path = os.path.join(settings.BASE_DIR, 'backend', 'ml_data', 'training_data.csv')
            if not os.path.exists(csv_path):
                self.stderr.write(self.style.ERROR(f"CSV file not found: {csv_path}"))
                return
        
        self.stdout.write(self.style.NOTICE(f"Loading CSV from: {csv_path}"))
        df = pd.read_csv(csv_path)
        
        self.stdout.write(self.style.NOTICE(f"CSV shape: {df.shape}"))
        self.stdout.write(self.style.NOTICE(f"CSV columns: {list(df.columns)}"))
        
        predictor = TurnoverPredictor()
        
        try:
            X, y = predictor.prepare_data(df.to_dict(orient='records'))
            if X is None or y is None:
                self.stderr.write(self.style.ERROR("Failed to prepare data"))
                return
                
            self.stdout.write(self.style.NOTICE(f"Training data shape: X={X.shape}, y={y.shape}"))
            self.stdout.write(self.style.NOTICE("Training model..."))
            
            results, best_model_name = predictor.train_models(X, y)
            
            model_path = get_model_save_path('turnover_model_v1')
            predictor.save_model(model_path)
            
            self.stdout.write(self.style.SUCCESS(f"Model trained and saved to {model_path}"))
            self.stdout.write(self.style.SUCCESS(f"Best model: {best_model_name}"))
            
            # Show training results
            for model_name, metrics in results.items():
                self.stdout.write(self.style.NOTICE(f"{model_name}: Accuracy={metrics['accuracy']:.3f}, F1={metrics['f1']:.3f}"))
                
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Training failed: {str(e)}"))
            import traceback
            self.stderr.write(traceback.format_exc())
