"""
Utility class untuk standardisasi response API Performance App
Memastikan semua endpoint performance menggunakan struktur response yang konsisten
"""

# Import utility yang sama dari predictions app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from predictions.response_utils import StandardResponse, ResponseMessages
