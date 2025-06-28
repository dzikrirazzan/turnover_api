#!/usr/bin/env python3
"""
Auto-activate ML Model Script
Jalanin ini setiap kali server restart atau model jadi inactive
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turnover_prediction.settings')
django.setup()

from predictions.models import MLModel

def auto_activate_model():
    """Automatically activate the best available model"""
    print("🔍 Checking ML Model Status...")
    
    # Check if any model is active
    active_model = MLModel.objects.filter(is_active=True).first()
    
    if active_model:
        print(f"✅ Model already active: {active_model.name}")
        print(f"   📊 Accuracy: {active_model.accuracy:.1%}")
        print(f"   🤖 Type: {active_model.model_type}")
        return active_model
    
    # No active model, find the best one
    print("❌ No active model found. Finding best model...")
    
    # Get model with highest accuracy
    best_model = MLModel.objects.all().order_by('-accuracy').first()
    
    if not best_model:
        print("💥 ERROR: No ML models found in database!")
        print("🚨 You need to train a model first:")
        print("   python manage.py shell -c \"from predictions.models import Employee; print('Employee count:', Employee.objects.count())\"")
        print("   python manage.py train_model")
        return None
    
    # Activate the best model
    print(f"🎯 Activating best model: {best_model.name}")
    print(f"   📊 Accuracy: {best_model.accuracy:.1%}")
    print(f"   🤖 Type: {best_model.model_type}")
    
    # Deactivate all others and activate this one
    MLModel.objects.filter(is_active=True).update(is_active=False)
    best_model.is_active = True
    best_model.save()
    
    print("✅ Model activated successfully!")
    return best_model

def check_model_file(model):
    """Check if model file exists"""
    if not model:
        return False
        
    model_path = model.model_file_path
    if os.path.exists(model_path):
        print(f"✅ Model file exists: {model_path}")
        return True
    else:
        print(f"❌ Model file missing: {model_path}")
        print("🚨 Model file not found! You may need to retrain the model.")
        return False

def test_prediction(model):
    """Test if model can make predictions"""
    if not model:
        return False
        
    try:
        import requests
        import base64
        
        # Test data
        test_data = {
            "satisfaction_level": 0.8,
            "last_evaluation": 0.85,
            "number_project": 4,
            "average_monthly_hours": 180,
            "time_spend_company": 3,
            "work_accident": False,
            "promotion_last_5years": True,
            "salary": "high",
            "department": "IT"
        }
        
        # Try to make a prediction
        auth_header = {
            'Authorization': f'Basic {base64.b64encode(b"admin:admin123").decode()}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'http://127.0.0.1:8000/api/predictions/predict/',
            json=test_data,
            headers=auth_header,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction test successful!")
            print(f"   🎯 Result: {'Will Leave' if data['prediction'] else 'Will Stay'}")
            print(f"   📈 Probability: {data['probability']:.3f}")
            print(f"   💡 Recommendations: {len(data.get('recommendations', []))} items")
            return True
        else:
            print(f"❌ Prediction test failed: {response.status_code}")
            if response.status_code == 400:
                error = response.json()
                print(f"   🔥 Error: {error.get('error', response.text)}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Django server not running. Start with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Prediction test error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 AUTO ML MODEL ACTIVATOR")
    print("=" * 50)
    
    # Step 1: Auto-activate model
    model = auto_activate_model()
    
    # Step 2: Check model file
    if model:
        file_ok = check_model_file(model)
        
        # Step 3: Test prediction (only if server is running)
        if file_ok:
            print("\n🧪 Testing prediction...")
            test_prediction(model)
    
    print("\n" + "=" * 50)
    if model:
        print("🎉 ML MODEL READY FOR USE!")
        print(f"✅ Active Model: {model.name}")
        print(f"📊 Accuracy: {model.accuracy:.1%}")
        print("\n💡 To keep model always active, add this to your startup:")
        print("   python auto_activate_ml.py")
    else:
        print("❌ NO ML MODEL AVAILABLE")
        print("\n🔧 To fix this:")
        print("1. python manage.py shell -c \"from predictions.models import Employee; print('Records:', Employee.objects.count())\"")
        print("2. If records < 100: python load_csv_data.py")
        print("3. python manage.py train_model")
        print("4. python auto_activate_ml.py")
