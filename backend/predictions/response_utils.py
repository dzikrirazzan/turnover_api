"""
Utility class untuk standardisasi response API
Memastikan semua endpoint menggunakan struktur response yang konsisten
"""

from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import QuerySet


class StandardResponse:
    """
    Class untuk membuat response API yang konsisten
    
    Struktur standar:
    - Success: {success: true, message: "...", data: {...}}
    - Error: {success: false, message: "...", errors: {...}}
    - List: {success: true, message: "...", data: [...], count: N, pagination: {...}}
    """
    
    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK, extra_data=None):
        """
        Response untuk operasi berhasil
        
        Args:
            message: Pesan sukses
            data: Data yang dikembalikan
            status_code: HTTP status code (default: 200)
            extra_data: Data tambahan (pagination, metadata, dll)
        """
        response_data = {
            'success': True,
            'message': message
        }
        
        if data is not None:
            response_data['data'] = data
        
        if extra_data:
            response_data.update(extra_data)
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(message, data=None, extra_data=None):
        """Response untuk data yang berhasil dibuat (POST)"""
        return StandardResponse.success(
            message=message, 
            data=data, 
            status_code=status.HTTP_201_CREATED,
            extra_data=extra_data
        )
    
    @staticmethod
    def error(message, errors=None, status_code=status.HTTP_400_BAD_REQUEST, extra_data=None):
        """
        Response untuk error
        
        Args:
            message: Pesan error
            errors: Detail error (validation errors, dll)
            status_code: HTTP status code (default: 400)
            extra_data: Data tambahan
        """
        response_data = {
            'success': False,
            'message': message
        }
        
        if errors is not None:
            response_data['errors'] = errors
        
        if extra_data:
            response_data.update(extra_data)
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error(message, errors, extra_data=None):
        """Response untuk validation error"""
        return StandardResponse.error(
            message=message,
            errors=errors,
            status_code=status.HTTP_400_BAD_REQUEST,
            extra_data=extra_data
        )
    
    @staticmethod
    def not_found(message="Data tidak ditemukan", extra_data=None):
        """Response untuk data tidak ditemukan"""
        return StandardResponse.error(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            extra_data=extra_data
        )
    
    @staticmethod
    def unauthorized(message="Authentication credentials were not provided", extra_data=None):
        """Response untuk unauthorized access"""
        return StandardResponse.error(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            extra_data=extra_data
        )
    
    @staticmethod
    def forbidden(message="You do not have permission to perform this action", extra_data=None):
        """Response untuk forbidden access"""
        return StandardResponse.error(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            extra_data=extra_data
        )
    
    @staticmethod
    def paginated_list(queryset_or_data, message, request=None, page_size=20, extra_data=None):
        """
        Response untuk list data dengan pagination
        
        Args:
            queryset_or_data: QuerySet Django atau list data
            message: Pesan sukses
            request: Request object untuk pagination
            page_size: Ukuran halaman (default: 20)
            extra_data: Data tambahan
        """
        if isinstance(queryset_or_data, QuerySet):
            # Jika QuerySet, lakukan pagination
            if request and 'page' in request.GET:
                paginator = Paginator(queryset_or_data, page_size)
                page_number = request.GET.get('page', 1)
                
                try:
                    page_obj = paginator.get_page(page_number)
                    data = list(page_obj.object_list.values()) if hasattr(page_obj.object_list, 'values') else list(page_obj.object_list)
                    
                    pagination_data = {
                        'pagination': {
                            'current_page': page_obj.number,
                            'total_pages': paginator.num_pages,
                            'total_items': paginator.count,
                            'has_next': page_obj.has_next(),
                            'has_previous': page_obj.has_previous(),
                            'page_size': page_size
                        }
                    }
                except Exception:
                    # Fallback jika pagination gagal
                    data = list(queryset_or_data.values()) if hasattr(queryset_or_data, 'values') else list(queryset_or_data)
                    pagination_data = {}
            else:
                # Tanpa pagination
                data = list(queryset_or_data.values()) if hasattr(queryset_or_data, 'values') else list(queryset_or_data)
                pagination_data = {}
        else:
            # Jika sudah list/array
            data = queryset_or_data
            pagination_data = {}
        
        response_data = {
            'success': True,
            'message': message,
            'data': data,
            'count': len(data)
        }
        
        if pagination_data:
            response_data.update(pagination_data)
        
        if extra_data:
            response_data.update(extra_data)
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @staticmethod
    def list_response(data, message, count=None, extra_data=None):
        """
        Response untuk list data sederhana tanpa pagination
        
        Args:
            data: List data
            message: Pesan sukses
            count: Jumlah data (optional, akan dihitung otomatis jika None)
            extra_data: Data tambahan
        """
        if count is None:
            count = len(data) if data else 0
        
        response_data = {
            'success': True,
            'message': message,
            'data': data,
            'count': count
        }
        
        if extra_data:
            response_data.update(extra_data)
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    @staticmethod
    def no_content(message="Operation completed successfully"):
        """Response untuk operasi berhasil tanpa data (DELETE)"""
        return Response({
            'success': True,
            'message': message
        }, status=status.HTTP_204_NO_CONTENT)


class ResponseMessages:
    """Kumpulan pesan standar untuk konsistensi"""
    
    # Success messages
    DATA_RETRIEVED = "Data berhasil diambil"
    DATA_CREATED = "Data berhasil dibuat"
    DATA_UPDATED = "Data berhasil diperbarui"
    DATA_DELETED = "Data berhasil dihapus"
    OPERATION_SUCCESS = "Operasi berhasil"
    
    # Authentication messages
    LOGIN_SUCCESS = "Login berhasil"
    LOGOUT_SUCCESS = "Logout berhasil"
    REGISTRATION_SUCCESS = "Registrasi berhasil"
    TOKEN_REFRESHED = "Token berhasil diperbarui"
    
    # Error messages
    VALIDATION_ERROR = "Validasi data gagal"
    NOT_FOUND = "Data tidak ditemukan"
    UNAUTHORIZED = "Anda tidak memiliki akses"
    FORBIDDEN = "Anda tidak memiliki izin untuk melakukan aksi ini"
    INTERNAL_ERROR = "Terjadi kesalahan internal server"
    
    # Specific messages
    INVALID_CREDENTIALS = "Email atau password salah"
    ACCOUNT_INACTIVE = "Akun tidak aktif"
    PERMISSION_DENIED = "Akses ditolak"
    DUPLICATE_DATA = "Data sudah ada"
    
    # List messages
    EMPLOYEES_RETRIEVED = "Data karyawan berhasil diambil"
    DEPARTMENTS_RETRIEVED = "Data departemen berhasil diambil"
    PERFORMANCE_DATA_RETRIEVED = "Data performa berhasil diambil"
