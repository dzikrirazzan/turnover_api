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
import warnings
warnings.filterwarnings('ignore')

class TurnoverPredictor:
    def __init__(self):
        self.models = {
            'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
            'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000)
        }
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.best_model = None
        self.best_model_name = None
        
    def prepare_data(self, data):
        """Prepare data for training"""
        if not data:
            return None, None
            
        df = pd.DataFrame(data)
        
        # Handle missing values
        numeric_columns = ['satisfaction_level', 'last_evaluation', 'number_project', 
                          'average_montly_hours', 'time_spend_company']  # Note: montly not monthly in CSV
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Normalize column names to match expected format
        if 'average_montly_hours' in df.columns:
            df['average_monthly_hours'] = df['average_montly_hours']
        if 'Work_accident' in df.columns:
            df['work_accident'] = df['Work_accident']
        if 'sales' in df.columns:
            df['department'] = df['sales']  # Map sales column to department
        
        # Encode categorical variables
        categorical_columns = ['salary', 'department']
        for col in categorical_columns:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
        
        # Prepare features (only use columns that exist)
        base_features = ['satisfaction_level', 'last_evaluation', 'number_project',
                        'average_monthly_hours', 'time_spend_company', 'work_accident',
                        'promotion_last_5years']
        
        feature_columns = []
        for col in base_features:
            if col in df.columns:
                feature_columns.append(col)
        
        if 'salary' in df.columns:
            feature_columns.append('salary')
        if 'department' in df.columns:
            feature_columns.append('department')
            
        X = df[feature_columns].values
        
        # Scale features
        X = self.scaler.fit_transform(X)
        
        # Prepare target variable
        if 'left' in df.columns:
            y = df['left'].values
        else:
            # If no target variable, create synthetic one based on satisfaction and evaluation
            y = ((df['satisfaction_level'] < 0.4) | (df['last_evaluation'] < 0.4)).astype(int)
        
        return X, y
    
    def train_models(self, X, y):
        """Train multiple models and select the best one"""
        if X is None or y is None:
            raise ValueError("Invalid training data")
            
        results = {}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train each model
        for name, model in self.models.items():
            try:
                # Train model
                model.fit(X_train, y_train)
                
                # Make predictions
                y_pred = model.predict(X_test)
                y_pred_proba = model.predict_proba(X_test)[:, 1]
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                auc = roc_auc_score(y_test, y_pred_proba)
                
                results[name] = {
                    'model': model,
                    'accuracy': accuracy,
                    'f1_score': f1,
                    'auc_score': auc,
                    'predictions': y_pred,
                    'probabilities': y_pred_proba
                }
                
            except Exception as e:
                print(f"Error training {name}: {str(e)}")
                continue
        
        # Select best model based on F1 score
        if results:
            self.best_model_name = max(results.keys(), key=lambda k: results[k]['f1_score'])
            self.best_model = results[self.best_model_name]['model']
        
        return results, self.best_model_name
    
    def predict(self, features):
        """Make prediction using the best model"""
        if self.best_model is None:
            raise ValueError("No trained model available")
        
        # Ensure features are in the right format
        if isinstance(features, dict):
            # Convert dict to array
            feature_array = np.array([[
                features.get('satisfaction_level', 0.5),
                features.get('last_evaluation', 0.5),
                features.get('number_project', 2),
                features.get('average_monthly_hours', 160),
                features.get('time_spend_company', 2),
                features.get('work_accident', 0),
                features.get('promotion_last_5years', 0)
            ]])
        else:
            feature_array = np.array(features).reshape(1, -1)
        
        # Scale features
        feature_array = self.scaler.transform(feature_array)
        
        # Make prediction
        prediction = self.best_model.predict(feature_array)[0]
        probability = self.best_model.predict_proba(feature_array)[0, 1]
        
        return prediction, probability
    
    def save_model(self, file_path):
        """Save the trained model and preprocessing objects"""
        if self.best_model is None:
            raise ValueError("No trained model to save")
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'best_model_name': self.best_model_name,
            'feature_names': ['satisfaction_level', 'last_evaluation', 'number_project',
                            'average_monthly_hours', 'time_spend_company', 'work_accident',
                            'promotion_last_5years']
        }
        
        joblib.dump(model_data, file_path)
        print(f"Model saved to {file_path}")
    
    def load_model(self, file_path):
        """Load a trained model"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Model file not found: {file_path}")
        
        model_data = joblib.load(file_path)
        self.best_model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.best_model_name = model_data['best_model_name']
        
        return model_data

class PerformanceAnalyzer:
    """Analyze employee performance patterns"""
    
    def __init__(self):
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.7,
            'high': 1.0
        }
    
    def analyze_performance_trends(self, performance_data_list):
        """Analyze performance trends across employees"""
        if not performance_data_list:
            return {}
        
        df = pd.DataFrame(performance_data_list)
        
        analysis = {
            'total_employees': len(df),
            'average_satisfaction': df['satisfaction_level'].mean(),
            'average_evaluation': df['last_evaluation'].mean(),
            'average_projects': df['number_project'].mean(),
            'average_hours': df['average_monthly_hours'].mean(),
            'average_tenure': df['time_spend_company'].mean(),
            'accident_rate': df['work_accident'].mean(),
            'promotion_rate': df['promotion_last_5years'].mean(),
            'turnover_rate': df['left'].mean() if 'left' in df.columns else 0,
            'risk_distribution': self._calculate_risk_distribution(df),
            'department_analysis': self._analyze_by_department(df),
            'salary_analysis': self._analyze_by_salary(df)
        }
        
        return analysis
    
    def _calculate_risk_distribution(self, df):
        """Calculate risk distribution based on performance metrics"""
        # Calculate risk score based on multiple factors
        risk_scores = []
        
        for _, row in df.iterrows():
            risk_score = 0
            
            # Low satisfaction increases risk
            if row['satisfaction_level'] < 0.4:
                risk_score += 0.3
            elif row['satisfaction_level'] < 0.6:
                risk_score += 0.1
            
            # Low evaluation increases risk
            if row['last_evaluation'] < 0.4:
                risk_score += 0.3
            elif row['last_evaluation'] < 0.6:
                risk_score += 0.1
            
            # High hours can increase risk
            if row['average_monthly_hours'] > 200:
                risk_score += 0.2
            elif row['average_monthly_hours'] > 180:
                risk_score += 0.1
            
            # Long tenure without promotion increases risk
            if row['time_spend_company'] > 4 and row['promotion_last_5years'] == 0:
                risk_score += 0.2
            
            # Work accidents increase risk
            if row['work_accident'] == 1:
                risk_score += 0.1
            
            risk_scores.append(min(risk_score, 1.0))
        
        df['risk_score'] = risk_scores
        
        # Categorize risk levels
        risk_distribution = {
            'low': len(df[df['risk_score'] < 0.3]),
            'medium': len(df[(df['risk_score'] >= 0.3) & (df['risk_score'] < 0.7)]),
            'high': len(df[df['risk_score'] >= 0.7])
        }
        
        return risk_distribution
    
    def _analyze_by_department(self, df):
        """Analyze performance by department"""
        if 'department' not in df.columns:
            return {}
        
        dept_analysis = {}
        for dept in df['department'].unique():
            dept_data = df[df['department'] == dept]
            dept_analysis[dept] = {
                'employee_count': len(dept_data),
                'avg_satisfaction': dept_data['satisfaction_level'].mean(),
                'avg_evaluation': dept_data['last_evaluation'].mean(),
                'avg_projects': dept_data['number_project'].mean(),
                'avg_hours': dept_data['average_monthly_hours'].mean(),
                'accident_rate': dept_data['work_accident'].mean(),
                'promotion_rate': dept_data['promotion_last_5years'].mean()
            }
        
        return dept_analysis
    
    def _analyze_by_salary(self, df):
        """Analyze performance by salary level"""
        if 'salary' not in df.columns:
            return {}
        
        salary_analysis = {}
        for salary in df['salary'].unique():
            salary_data = df[df['salary'] == salary]
            salary_analysis[salary] = {
                'employee_count': len(salary_data),
                'avg_satisfaction': salary_data['satisfaction_level'].mean(),
                'avg_evaluation': salary_data['last_evaluation'].mean(),
                'avg_projects': salary_data['number_project'].mean(),
                'avg_hours': salary_data['average_monthly_hours'].mean(),
                'accident_rate': salary_data['work_accident'].mean(),
                'promotion_rate': salary_data['promotion_last_5years'].mean()
            }
        
        return salary_analysis

class TurnoverRiskCalculator:
    """Calculate turnover risk based on multiple factors"""
    
    def __init__(self):
        self.risk_factors = {
            'satisfaction_level': {
                'weight': 0.25,
                'thresholds': {'low': 0.4, 'medium': 0.6}
            },
            'last_evaluation': {
                'weight': 0.20,
                'thresholds': {'low': 0.4, 'medium': 0.6}
            },
            'number_project': {
                'weight': 0.15,
                'thresholds': {'low': 2, 'high': 6}
            },
            'average_monthly_hours': {
                'weight': 0.15,
                'thresholds': {'low': 160, 'high': 200}
            },
            'time_spend_company': {
                'weight': 0.10,
                'thresholds': {'low': 2, 'high': 5}
            },
            'work_accident': {
                'weight': 0.05,
                'thresholds': {'risk': 1}
            },
            'promotion_last_5years': {
                'weight': 0.10,
                'thresholds': {'risk': 0}
            }
        }
    
    def calculate_risk_score(self, performance_data):
        """Calculate comprehensive risk score"""
        risk_score = 0
        risk_details = {}
        
        for factor, config in self.risk_factors.items():
            value = getattr(performance_data, factor, 0)
            weight = config['weight']
            thresholds = config['thresholds']
            
            factor_risk = 0
            
            if factor == 'satisfaction_level':
                if value < thresholds['low']:
                    factor_risk = 1.0
                elif value < thresholds['medium']:
                    factor_risk = 0.5
                else:
                    factor_risk = 0.0
                    
            elif factor == 'last_evaluation':
                if value < thresholds['low']:
                    factor_risk = 1.0
                elif value < thresholds['medium']:
                    factor_risk = 0.5
                else:
                    factor_risk = 0.0
                    
            elif factor == 'number_project':
                if value < thresholds['low']:
                    factor_risk = 0.3
                elif value > thresholds['high']:
                    factor_risk = 0.7
                else:
                    factor_risk = 0.0
                    
            elif factor == 'average_monthly_hours':
                if value < thresholds['low']:
                    factor_risk = 0.3
                elif value > thresholds['high']:
                    factor_risk = 0.8
                else:
                    factor_risk = 0.0
                    
            elif factor == 'time_spend_company':
                if value < thresholds['low']:
                    factor_risk = 0.2
                elif value > thresholds['high']:
                    factor_risk = 0.6
                else:
                    factor_risk = 0.0
                    
            elif factor == 'work_accident':
                if value == thresholds['risk']:
                    factor_risk = 0.3
                else:
                    factor_risk = 0.0
                    
            elif factor == 'promotion_last_5years':
                if value == thresholds['risk']:
                    factor_risk = 0.4
                else:
                    factor_risk = 0.0
            
            risk_score += factor_risk * weight
            risk_details[factor] = {
                'value': value,
                'risk': factor_risk,
                'weight': weight,
                'contribution': factor_risk * weight
            }
        
        # Determine risk level
        if risk_score < 0.3:
            risk_level = 'low'
        elif risk_score < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'overall_risk_score': risk_score,
            'risk_level': risk_level,
            'risk_details': risk_details
        }
    
    def get_risk_recommendations(self, risk_analysis):
        """Get recommendations based on risk analysis"""
        recommendations = []
        risk_details = risk_analysis['risk_details']
        
        if risk_details['satisfaction_level']['risk'] > 0.5:
            recommendations.append({
                'category': 'Employee Satisfaction',
                'issue': 'Low satisfaction level detected',
                'recommendation': 'Conduct one-on-one meetings to understand concerns and improve work environment',
                'priority': 'high'
            })
        
        if risk_details['last_evaluation']['risk'] > 0.5:
            recommendations.append({
                'category': 'Performance',
                'issue': 'Low performance evaluation',
                'recommendation': 'Provide additional training and support to improve performance',
                'priority': 'high'
            })
        
        if risk_details['average_monthly_hours']['risk'] > 0.5:
            recommendations.append({
                'category': 'Workload',
                'issue': 'Excessive working hours detected',
                'recommendation': 'Review workload distribution and consider hiring additional staff',
                'priority': 'medium'
            })
        
        if risk_details['promotion_last_5years']['risk'] > 0.3:
            recommendations.append({
                'category': 'Career Growth',
                'issue': 'No promotion in the last 5 years',
                'recommendation': 'Review career progression opportunities and create development plans',
                'priority': 'medium'
            })
        
        if risk_details['work_accident']['risk'] > 0.2:
            recommendations.append({
                'category': 'Safety',
                'issue': 'Work accident recorded',
                'recommendation': 'Review safety protocols and provide additional training',
                'priority': 'medium'
            })
        
        return recommendations

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
