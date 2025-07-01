
from django.core.management.base import BaseCommand, CommandError
from predictions.models import Employee, MLModel
from predictions.ml_utils import TurnoverPredictor, get_model_save_path
from predictions.load_data import load_training_data
import pandas as pd
from pathlib import Path

# Define the base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    help = 'Trains the machine learning model from the CSV file.'

    def handle(self, *args, **options):
        self.stdout.write('Starting model training from CSV...')

        # Load data from the CSV file
        df = load_training_data()
        if df is None or len(df) < 100:
            raise CommandError('Insufficient data from CSV for training. Need at least 100 records.')

        # Rename columns to match the expected format
        df = df.rename(columns={
            'sales': 'department',
            'average_montly_hours': 'average_monthly_hours',
            'Work_accident': 'work_accident'
        })

        # Convert DataFrame to list of dictionaries
        employee_data = df.to_dict('records')

        # Initialize and train the predictor
        predictor = TurnoverPredictor()
        X, y = predictor.prepare_data(employee_data)
        
        results, best_model_name = predictor.train_models(X, y)
        
        model_name = 'production_model_from_csv'
        # Save the model
        model_path = get_model_save_path(model_name)
        self.stdout.write(f"Attempting to save model to: {model_path}")
        predictor.save_model(model_path)
        self.stdout.write(self.style.SUCCESS(f"Model saved successfully to: {model_path}"))
        
        # Get feature importance
        feature_importance = predictor.get_feature_importance()
        
        # Filter hyperparameters to only include JSON-serializable values
        hyperparams = results[best_model_name]['hyperparameters']
        filtered_hyperparams = {}
        for key, value in hyperparams.items():
            try:
                import json
                json.dumps(value)  # Test if value is JSON serializable
                filtered_hyperparams[key] = value
            except (TypeError, ValueError):
                # Skip non-serializable objects like StandardScaler
                filtered_hyperparams[key] = str(type(value).__name__)
        
        # Deactivate other models before creating a new active one
        MLModel.objects.filter(is_active=True).update(is_active=False)
        
        # Create new model record
        ml_model, created = MLModel.objects.update_or_create(
            name=model_name,
            defaults={
                'model_type': best_model_name,
                'model_file_path': model_path,
                'accuracy': results[best_model_name]['accuracy'],
                'f1_score': results[best_model_name]['f1_score'],
                'auc_score': results[best_model_name]['auc_score'],
                'hyperparameters': filtered_hyperparams,
                'feature_importance': feature_importance,
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created and trained new model "{model_name}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated and retrained model "{model_name}".'))

        self.stdout.write(self.style.SUCCESS('Model training complete.'))
