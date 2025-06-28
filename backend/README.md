# Employee Turnover Prediction API

Django REST API backend untuk sistem prediksi turnover karyawan menggunakan machine learning.

## Fitur Utama

- **Manajemen Karyawan**: CRUD operations untuk data karyawan
- **Prediksi Turnover**: Machine learning model untuk prediksi turnover
- **Multiple ML Models**: Support untuk Random Forest, Gradient Boosting, SVM, dll.
- **Admin Dashboard**: Interface admin untuk manajemen data
- **REST API**: Endpoints lengkap untuk integrasi frontend
- **Statistics**: Dashboard statistik turnover

## Teknologi yang Digunakan

- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **scikit-learn**: Machine learning
- **pandas & numpy**: Data processing
- **SQLite**: Database (development)
- **PostgreSQL**: Database (production)

## Machine Learning Model

Berdasarkan penelitian dari [artikel Medium](https://medium.com/data-science/predicting-employee-turnover-7ab2b9ecf47e), sistem ini menggunakan:

### Features yang Digunakan:

1. **satisfaction_level**: Tingkat kepuasan karyawan (0-1)
2. **last_evaluation**: Evaluasi terakhir (0-1)
3. **number_project**: Jumlah proyek yang dikerjakan
4. **average_monthly_hours**: Rata-rata jam kerja per bulan
5. **time_spend_company**: Lama bekerja di perusahaan (tahun)
6. **work_accident**: Apakah pernah mengalami kecelakaan kerja
7. **promotion_last_5years**: Apakah mendapat promosi dalam 5 tahun terakhir
8. **salary**: Tingkat gaji (low, medium, high)
9. **department**: Departemen tempat bekerja

### Models yang Tersedia:

- **Random Forest** (Best performer menurut penelitian)
- **Gradient Boosting Trees**
- **Logistic Regression**
- **Support Vector Machine**
- **K-Nearest Neighbors**

## Setup dan Instalasi

### 1. Clone Repository

```bash
cd backend
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env file dengan konfigurasi yang sesuai
```

### 5. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Seed Sample Data

```bash
python manage.py seed_data --employees 500
```

### 8. Train ML Model

```bash
python manage.py shell
```

```python
from predictions.ml_utils import TurnoverPredictor
from predictions.models import Employee, MLModel
from predictions.ml_utils import prepare_employee_data_for_ml, get_model_save_path

# Ambil data karyawan
employees = Employee.objects.all()
employee_data = [prepare_employee_data_for_ml(emp) for emp in employees]

# Train model
predictor = TurnoverPredictor()
X, y = predictor.prepare_data(employee_data)
results, best_model_name = predictor.train_models(X, y)

# Simpan model
model_path = get_model_save_path('turnover_model_v1')
predictor.save_model(model_path)

# Simpan ke database
MLModel.objects.create(
    name='turnover_model_v1',
    model_type=best_model_name,
    model_file_path=model_path,
    accuracy=results[best_model_name]['accuracy'],
    f1_score=results[best_model_name]['f1_score'],
    auc_score=results[best_model_name]['auc_score'],
    is_active=True
)
```

### 9. Run Server

```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Departments

- `GET /api/departments/` - List departments
- `POST /api/departments/` - Create department
- `GET /api/departments/{id}/` - Get department
- `PUT /api/departments/{id}/` - Update department
- `DELETE /api/departments/{id}/` - Delete department

### Employees

- `GET /api/employees/` - List employees
- `POST /api/employees/` - Create employee
- `GET /api/employees/{id}/` - Get employee
- `PUT /api/employees/{id}/` - Update employee
- `DELETE /api/employees/{id}/` - Delete employee
- `GET /api/employees/statistics/` - Get employee statistics
- `POST /api/employees/{id}/predict_turnover/` - Predict turnover for employee

### Predictions

- `GET /api/predictions/` - List predictions
- `POST /api/predictions/predict/` - Make single prediction
- `POST /api/predictions/bulk_predict/` - Make bulk predictions

### ML Models

- `GET /api/models/` - List ML models
- `POST /api/models/train/` - Train new model
- `POST /api/models/{id}/activate/` - Activate model
- `GET /api/models/active/` - Get active model

## Contoh Penggunaan API

### 1. Prediksi Turnover untuk Karyawan Baru

```bash
curl -X POST http://localhost:8000/api/predictions/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "satisfaction_level": 0.4,
    "last_evaluation": 0.6,
    "number_project": 5,
    "average_monthly_hours": 280,
    "time_spend_company": 3,
    "work_accident": false,
    "promotion_last_5years": false,
    "salary": "low",
    "department": "IT"
  }'
```

### 2. Bulk Prediction

```bash
curl -X POST http://localhost:8000/api/predictions/bulk_predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "employees": [
      {
        "employee_id": "EMP001",
        "satisfaction_level": 0.8,
        "last_evaluation": 0.9,
        "number_project": 3,
        "average_monthly_hours": 180,
        "time_spend_company": 2,
        "work_accident": false,
        "promotion_last_5years": true,
        "salary": "high",
        "department": "IT"
      }
    ]
  }'
```

### 3. Train Model Baru

```bash
curl -X POST http://localhost:8000/api/models/train/ \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "turnover_model_v2",
    "use_existing_data": true
  }'
```

## Response Format

### Prediction Response

```json
{
  "prediction": true,
  "probability": 0.75,
  "confidence": 0.85,
  "risk_level": "High",
  "recommendations": ["Consider conducting a satisfaction survey and addressing concerns", "Employee may be overworked - consider workload redistribution"]
}
```

### Statistics Response

```json
{
  "total_employees": 500,
  "total_left": 125,
  "turnover_rate": 25.0,
  "avg_satisfaction": 0.62,
  "avg_monthly_hours": 201.5,
  "department_stats": {
    "IT": {
      "total": 75,
      "left": 15,
      "turnover_rate": 20.0
    }
  },
  "salary_distribution": {
    "low": 200,
    "medium": 250,
    "high": 50
  }
}
```

## Model Performance

Berdasarkan testing dengan data sample:

- **Random Forest**: F1-score ~99.4%, AUC ~99.8%
- **Gradient Boosting**: F1-score ~98.8%, AUC ~99.2%
- **Logistic Regression**: F1-score ~78.5%, AUC ~82.1%

## Feature Importance

Top 5 fitur paling penting untuk prediksi:

1. **satisfaction_level** - Tingkat kepuasan (paling penting)
2. **time_spend_company** - Lama bekerja
3. **average_monthly_hours** - Jam kerja rata-rata
4. **number_project** - Jumlah proyek
5. **last_evaluation** - Evaluasi terakhir

## Deployment

### Using Docker

```bash
# Build image
docker build -t turnover-api .

# Run container
docker run -p 8000:8000 turnover-api
```

### Using Gunicorn

```bash
gunicorn turnover_prediction.wsgi:application --bind 0.0.0.0:8000
```

## Testing

```bash
# Run tests
python manage.py test

# Run specific test
python manage.py test predictions.tests.test_views
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License

This project is licensed under the MIT License.

## Contact

Untuk pertanyaan atau support, silakan hubungi tim development.
