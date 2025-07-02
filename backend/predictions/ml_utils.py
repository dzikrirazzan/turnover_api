import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, classification_report
from sklearn.pipeline import make_pipeline
import joblib
import os
from django.conf import settings

class TurnoverPredictor:
    def __init__(self):
        self.models = {
            'RandomForest': RandomForestClassifier(random_state=42),
            'GradientBoosting': GradientBoostingClassifier(random_state=42),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),
            'SVM': SVC(random_state=42, probability=True),
            'KNN': KNeighborsClassifier()
        }
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        
    def prepare_data(self, employees_data):
        """
        Prepare data for ML model based on the Medium article features
        """
        df = pd.DataFrame(employees_data)

        # Auto-rename columns from CSV if needed
        rename_map = {
            'sales': 'department',
            'average_montly_hours': 'average_monthly_hours',
            'Work_accident': 'work_accident',
        }
        for old, new in rename_map.items():
            if old in df.columns:
                df[new] = df[old]
        
        # Features from the article
        feature_columns = [
            'satisfaction_level', 'last_evaluation', 'number_project',
            'average_monthly_hours', 'time_spend_company', 'work_accident',
            'promotion_last_5years', 'salary', 'department'
        ]
        
        # Handle categorical variables
        # Convert salary to ordinal (as mentioned in the article)
        salary_mapping = {'low': 0, 'medium': 1, 'high': 2}
        df['salary_ordinal'] = df['salary'].map(salary_mapping)
        
        # Create dummy variables for department
        department_dummies = pd.get_dummies(df['department'], prefix='department')
        
        # Combine all features
        features_df = df[['satisfaction_level', 'last_evaluation', 'number_project',
                         'average_monthly_hours', 'time_spend_company', 'work_accident',
                         'promotion_last_5years', 'salary_ordinal']].copy()
        
        # Add department dummies (drop first to avoid multicollinearity)
        features_df = pd.concat([features_df, department_dummies.iloc[:, 1:]], axis=1)
        
        # Store feature names if not already stored
        if not self.feature_names:
            self.feature_names = features_df.columns.tolist()
        else:
            # Ensure we have all the expected features
            for feature in self.feature_names:
                if feature not in features_df.columns:
                    features_df[feature] = 0
            
            # Reorder columns to match training data
            features_df = features_df[self.feature_names]
        
        # Return target if available, otherwise return None
        if 'left' in df.columns:
            return features_df, df['left']
        else:
            return features_df, None
    
    def train_models(self, X, y):
        """
        Train models optimized for production environments with limited resources
        """
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Handle class imbalance with upsampling (as suggested in the article)
        X_train_upsampled, y_train_upsampled = self._upsample_minority_class(X_train, y_train)
        
        results = {}
        
        # Use simpler, faster models for production
        print("🚀 Training RandomForest with optimized parameters...")
        rf_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=1  # Use single core to avoid OOM
        )
        rf_pipeline = make_pipeline(StandardScaler(), rf_model)
        rf_pipeline.fit(X_train_upsampled, y_train_upsampled)
        
        print("🚀 Training LogisticRegression...")
        lr_pipeline = make_pipeline(StandardScaler(), LogisticRegression(
            random_state=42, 
            max_iter=1000,
            solver='lbfgs'  # Faster solver
        ))
        lr_pipeline.fit(X_train_upsampled, y_train_upsampled)
        
        print("🚀 Training simplified GradientBoosting...")
        gb_model = GradientBoostingClassifier(
            n_estimators=50,  # Reduced from 100-200
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        gb_pipeline = make_pipeline(StandardScaler(), gb_model)
        gb_pipeline.fit(X_train_upsampled, y_train_upsampled)
        
        # Evaluate models
        models_to_evaluate = {
            'RandomForest': rf_pipeline,
            'LogisticRegression': lr_pipeline,
            'GradientBoosting': gb_pipeline
        }
        
        print("📊 Evaluating models...")
        for name, model in models_to_evaluate.items():
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            
            results[name] = {
                'model': model,
                'accuracy': accuracy_score(y_test, y_pred),
                'f1_score': f1_score(y_test, y_pred),
                'auc_score': roc_auc_score(y_test, y_pred_proba),
                'hyperparameters': model.get_params()
            }
            
            print(f"✅ {name}: Accuracy={results[name]['accuracy']:.3f}, F1={results[name]['f1_score']:.3f}")
        
        # Select best model based on f1-score
        best_model_name = max(results.keys(), key=lambda k: results[k]['f1_score'])
        self.best_model = results[best_model_name]['model']
        
        print(f"🏆 Best model: {best_model_name}")
        return results, best_model_name
    
    def _upsample_minority_class(self, X, y):
        """
        Upsample minority class to handle imbalanced data
        """
        from sklearn.utils import resample
        
        # Combine X and y
        data = pd.concat([pd.DataFrame(X), pd.Series(y, name='target')], axis=1)
        
        # Separate majority and minority classes
        majority = data[data.target == 0]
        minority = data[data.target == 1]
        
        # Upsample minority class
        minority_upsampled = resample(minority,
                                    replace=True,
                                    n_samples=len(majority),
                                    random_state=42)
        
        # Combine majority class with upsampled minority class
        upsampled = pd.concat([majority, minority_upsampled])
        
        # Separate features and target
        X_upsampled = upsampled.drop('target', axis=1)
        y_upsampled = upsampled['target']
        
        return X_upsampled, y_upsampled
    
    def predict_single(self, employee_data):
        """
        Predict turnover for a single employee
        """
        if self.best_model is None:
            raise ValueError("Model not trained yet. Please train the model first.")
        
        # Prepare single employee data - make sure it's in list format
        X, _ = self.prepare_data([employee_data])
        
        # Make prediction
        prediction_proba = self.best_model.predict_proba(X)[0, 1]
        prediction = self.best_model.predict(X)[0]
        
        return {
            'prediction': bool(prediction),
            'probability': float(prediction_proba),
            'confidence': float(abs(prediction_proba - 0.5) * 2)  # Distance from decision boundary
        }
    
    def get_feature_importance(self):
        """
        Get feature importance from the best model
        """
        if self.best_model is None:
            return None
        
        # Get the actual classifier from the pipeline
        classifier = self.best_model.named_steps[list(self.best_model.named_steps.keys())[-1]]
        
        if hasattr(classifier, 'feature_importances_'):
            importance_dict = dict(zip(self.feature_names, classifier.feature_importances_))
            # Sort by importance
            return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        
        return None
    
    def save_model(self, filepath):
        """
        Save the trained model
        """
        if self.best_model is None:
            raise ValueError("No model to save. Please train the model first.")
        
        model_data = {
            'model': self.best_model,
            'feature_names': self.feature_names,
            'scaler': self.scaler
        }
        
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath):
        """
        Load a trained model
        """
        if os.path.exists(filepath):
            try:
                model_data = joblib.load(filepath)
                self.best_model = model_data['model']
                self.feature_names = model_data['feature_names']
                self.scaler = model_data['scaler']
                return True
            except Exception as e:
                print(f"[ERROR] Failed to load model from {filepath}: {e}")
                return False
        else:
            print(f"[ERROR] Model file not found at: {filepath}")
            return False

# Utility functions for Django integration
def get_model_save_path(model_name):
    """
    Get the path to save ML models
    """
    models_dir = os.path.join(settings.BASE_DIR, 'backend', 'ml_models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    return os.path.join(models_dir, f"{model_name}.joblib")

def prepare_employee_data_for_ml(employee):
    """
    Convert Django Employee model instance to format suitable for ML
    """
    return {
        'satisfaction_level': employee.satisfaction_level,
        'last_evaluation': employee.last_evaluation,
        'number_project': employee.number_project,
        'average_monthly_hours': employee.average_monthly_hours,
        'time_spend_company': employee.time_spend_company,
        'work_accident': int(employee.work_accident),
        'promotion_last_5years': int(employee.promotion_last_5years),
        'salary': employee.salary,
        'department': employee.department.name,
        'left': int(employee.left)
    }
