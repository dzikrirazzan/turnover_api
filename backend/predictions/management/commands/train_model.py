from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from predictions.models import Employee, MLModel
from predictions.ml_utils import TurnoverPredictor, prepare_employee_data_for_ml, get_model_save_path
import os

class Command(BaseCommand):
    help = 'Train ML model for turnover prediction'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model-name',
            type=str,
            default='turnover_model_v1',
            help='Name of the model to train'
        )

    def handle(self, *args, **options):
        model_name = options['model_name']
        
        self.stdout.write(self.style.SUCCESS(f'Starting to train model: {model_name}...'))
        
        # Check if we have enough data
        employees = Employee.objects.all()
        if employees.count() < 50:
            self.stdout.write(
                self.style.ERROR(
                    f'Insufficient data for training. Need at least 50 employee records. '
                    f'Current count: {employees.count()}'
                )
            )
            return
        
        try:
            # Prepare data
            self.stdout.write('Preparing data...')
            employee_data = [prepare_employee_data_for_ml(emp) for emp in employees]
            
            # Initialize and train the predictor
            self.stdout.write('Training models...')
            predictor = TurnoverPredictor()
            X, y = predictor.prepare_data(employee_data)
            
            results, best_model_name = predictor.train_models(X, y)
            
            # Save the model
            self.stdout.write('Saving model...')
            model_path = get_model_save_path(model_name)
            predictor.save_model(model_path)
            
            # Get feature importance
            feature_importance = predictor.get_feature_importance()
            
            # Save model info to database
            # Deactivate other models
            MLModel.objects.filter(is_active=True).update(is_active=False)
            
            # Get admin user
            admin_user = User.objects.filter(is_superuser=True).first()
            
            # Convert hyperparameters to JSON serializable format
            hyperparams = results[best_model_name]['hyperparameters']
            serializable_hyperparams = {}
            for key, value in hyperparams.items():
                if hasattr(value, '__dict__'):
                    serializable_hyperparams[key] = str(value)
                else:
                    try:
                        # Try to convert to basic types
                        import json
                        json.dumps(value)
                        serializable_hyperparams[key] = value
                    except:
                        serializable_hyperparams[key] = str(value)
            
            # Create new model record
            ml_model = MLModel.objects.create(
                name=model_name,
                model_type=best_model_name,
                model_file_path=model_path,
                accuracy=results[best_model_name]['accuracy'],
                f1_score=results[best_model_name]['f1_score'],
                auc_score=results[best_model_name]['auc_score'],
                hyperparameters=serializable_hyperparams,
                feature_importance=feature_importance,
                is_active=True,
                trained_by=admin_user
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nModel training completed successfully!\n'
                    f'Model ID: {ml_model.id}\n'
                    f'Best Model: {best_model_name}\n'
                    f'Model saved at: {model_path}\n'
                )
            )
            
            # Print results
            self.stdout.write('\nModel Performance:')
            for name, result in results.items():
                marker = "★" if name == best_model_name else " "
                self.stdout.write(
                    f'{marker} {name}:\n'
                    f'  - Accuracy: {result["accuracy"]:.4f}\n'
                    f'  - F1-Score: {result["f1_score"]:.4f}\n'
                    f'  - AUC Score: {result["auc_score"]:.4f}'
                )
            
            # Print feature importance
            if feature_importance:
                self.stdout.write('\nTop 5 Most Important Features:')
                for i, (feature, importance) in enumerate(list(feature_importance.items())[:5], 1):
                    self.stdout.write(f'{i}. {feature}: {importance:.4f}')
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error training model: {str(e)}')
            )
            import traceback
            traceback.print_exc()
