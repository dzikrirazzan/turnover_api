#!/usr/bin/env python3
"""
Script untuk menganalisis dan memperbaiki konsistensi response API
Mengidentifikasi semua endpoint dan struktur response yang ada
"""

import os
import re
import ast
from pathlib import Path

def analyze_views_file(file_path):
    """Analisis file views.py untuk menemukan struktur response"""
    responses = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cari semua return Response
        response_pattern = r'return Response\((.*?)\)'
        matches = re.finditer(response_pattern, content, re.DOTALL)
        
        for match in matches:
            response_content = match.group(1).strip()
            
            # Cari konteks function
            start_pos = match.start()
            lines_before = content[:start_pos].split('\n')
            
            # Cari function definition terdekat
            function_name = "unknown"
            for i in range(len(lines_before) - 1, -1, -1):
                line = lines_before[i].strip()
                if line.startswith('def ') or line.startswith('class '):
                    function_name = line.split('(')[0].replace('def ', '').replace('class ', '')
                    break
            
            responses.append({
                'file': file_path,
                'function': function_name,
                'response': response_content,
                'line': len(lines_before)
            })
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return responses

def find_all_views():
    """Temukan semua file views.py dalam proyek"""
    views_files = []
    backend_path = Path("backend")
    
    if backend_path.exists():
        for views_file in backend_path.rglob("views.py"):
            views_files.append(str(views_file))
    
    return views_files

def analyze_response_structure(response_str):
    """Analisis struktur response untuk kategorisasi"""
    response_str = response_str.strip()
    
    # Kategorisasi berdasarkan pola
    if response_str.startswith('{'):
        return "dict_response"
    elif response_str.startswith('serializer.data'):
        return "serializer_response"
    elif response_str.startswith('serializer.errors'):
        return "error_response"
    elif 'status=' in response_str:
        return "status_specified"
    else:
        return "other"

def generate_response_report():
    """Generate laporan lengkap tentang struktur response API"""
    print("🔍 ANALISIS STRUKTUR RESPONSE API")
    print("=" * 60)
    
    all_responses = []
    views_files = find_all_views()
    
    print(f"📁 Found {len(views_files)} views files:")
    for views_file in views_files:
        print(f"   • {views_file}")
    
    print("\n📊 ANALYZING RESPONSES...")
    print("=" * 60)
    
    for views_file in views_files:
        responses = analyze_views_file(views_file)
        all_responses.extend(responses)
        
        print(f"\n📄 File: {views_file}")
        print(f"   Found {len(responses)} response statements")
    
    # Kategorisasi responses
    categories = {}
    inconsistencies = []
    
    for response in all_responses:
        category = analyze_response_structure(response['response'])
        if category not in categories:
            categories[category] = []
        categories[category].append(response)
    
    print(f"\n📈 RESPONSE CATEGORIES:")
    print("=" * 60)
    
    for category, responses in categories.items():
        print(f"\n🏷️  {category.upper()}: {len(responses)} instances")
        for response in responses[:3]:  # Show first 3 examples
            print(f"   • {response['function']} → {response['response'][:80]}...")
    
    # Analisis inkonsistensi
    print(f"\n❌ INKONSISTENSI YANG DITEMUKAN:")
    print("=" * 60)
    
    # 1. Response tanpa struktur standar
    non_standard_responses = []
    for response in all_responses:
        resp_str = response['response'].strip()
        if not (resp_str.startswith('{') or resp_str.startswith('serializer')):
            non_standard_responses.append(response)
    
    if non_standard_responses:
        print(f"\n🚨 Response tanpa struktur standar: {len(non_standard_responses)}")
        for resp in non_standard_responses[:5]:
            print(f"   • {resp['function']}: {resp['response'][:100]}...")
    
    # 2. Response success tanpa message
    success_without_message = []
    for response in all_responses:
        resp_str = response['response'].lower()
        if (resp_str.startswith('{') and 
            'status.http_201_created' in resp_str or 'status.http_200_ok' in resp_str):
            if "'message'" not in resp_str and '"message"' not in resp_str:
                success_without_message.append(response)
    
    if success_without_message:
        print(f"\n📝 Success response tanpa message: {len(success_without_message)}")
        for resp in success_without_message[:5]:
            print(f"   • {resp['function']}: {resp['response'][:100]}...")
    
    # 3. Error handling tidak konsisten
    error_responses = [r for r in all_responses if 'errors' in r['response']]
    inconsistent_errors = []
    
    for response in error_responses:
        resp_str = response['response']
        if not ('status.HTTP_400_BAD_REQUEST' in resp_str):
            inconsistent_errors.append(response)
    
    if inconsistent_errors:
        print(f"\n🔴 Error response tidak konsisten: {len(inconsistent_errors)}")
        for resp in inconsistent_errors[:5]:
            print(f"   • {resp['function']}: {resp['response'][:100]}...")
    
    print(f"\n📋 SUMMARY:")
    print("=" * 60)
    print(f"Total response statements found: {len(all_responses)}")
    print(f"Response categories: {len(categories)}")
    print(f"Potential inconsistencies: {len(non_standard_responses + success_without_message + inconsistent_errors)}")
    
    return all_responses, categories

def generate_improvement_plan():
    """Generate rencana perbaikan untuk konsistensi API"""
    print(f"\n🎯 RENCANA PERBAIKAN API RESPONSE")
    print("=" * 60)
    
    improvements = {
        "1_standardize_success": {
            "title": "Standardisasi Success Response",
            "description": "Semua success response harus memiliki struktur: {success: true, message: '...', data: {...}}",
            "examples": [
                "✅ {'success': true, 'message': 'Data berhasil dibuat', 'data': {...}}",
                "✅ {'success': true, 'message': 'Data berhasil diperbarui', 'data': {...}}"
            ]
        },
        "2_standardize_error": {
            "title": "Standardisasi Error Response", 
            "description": "Semua error response harus memiliki struktur: {success: false, message: '...', errors: {...}}",
            "examples": [
                "❌ {'success': false, 'message': 'Validasi gagal', 'errors': {...}}",
                "❌ {'success': false, 'message': 'Data tidak ditemukan', 'errors': {'detail': 'Not found'}}"
            ]
        },
        "3_standardize_list": {
            "title": "Standardisasi List Response",
            "description": "Semua list response harus memiliki struktur: {success: true, message: '...', data: [...], count: N}",
            "examples": [
                "📋 {'success': true, 'message': 'Data berhasil diambil', 'data': [...], 'count': 25}",
                "📋 {'success': true, 'message': 'Data berhasil diambil', 'data': [...], 'count': 0, 'pagination': {...}}"
            ]
        },
        "4_consistent_status": {
            "title": "Konsistensi HTTP Status Code",
            "description": "Gunakan status code yang tepat untuk setiap operasi",
            "examples": [
                "📝 POST (Create): 201 CREATED",
                "📖 GET: 200 OK",
                "📝 PUT/PATCH (Update): 200 OK",
                "🗑️ DELETE: 204 NO CONTENT",
                "❌ Validation Error: 400 BAD REQUEST",
                "🔒 Authentication Error: 401 UNAUTHORIZED",
                "🚫 Permission Error: 403 FORBIDDEN",
                "🔍 Not Found: 404 NOT FOUND"
            ]
        }
    }
    
    for key, improvement in improvements.items():
        print(f"\n{improvement['title']}")
        print("-" * len(improvement['title']))
        print(improvement['description'])
        print("\nContoh:")
        for example in improvement['examples']:
            print(f"  {example}")
    
    return improvements

if __name__ == "__main__":
    print("🚀 Starting API Response Analysis...")
    
    # Change to project directory
    os.chdir("/Users/dzikrirazzan/Documents/code/turnover_api")
    
    # Generate analysis report
    responses, categories = generate_response_report()
    
    # Generate improvement plan
    improvements = generate_improvement_plan()
    
    print(f"\n✅ Analysis complete! Check the output above for detailed findings.")
