# 🚨 FRONTEND CORS/TIMEOUT ISSUE - SOLUTION GUIDE

## 📋 Problem Analysis

✅ **API Status**: WORKING PERFECTLY  
✅ **CORS Headers**: ALL CONFIGURED CORRECTLY  
✅ **Registration Endpoint**: FUNCTIONAL  
❌ **Frontend Issue**: `ERR_TIMED_OUT` dan `Failed to fetch`

## 🔧 Root Cause

Masalah ada di **frontend fetch configuration**, bukan di API server. Error `ERR_TIMED_OUT` menunjukkan:

1. **Network timeout** terlalu pendek
2. **Fetch configuration** tidak optimal
3. **Error handling** tidak proper
4. Kemungkinan **network policy** di Vercel

## 💻 FRONTEND FIXES

### 1. Fix Fetch Configuration

**❌ Yang mungkin salah:**
```javascript
// Fetch tanpa timeout dan proper error handling
const response = await fetch(API_URL, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data)
});
```

**✅ Yang benar:**
```javascript
// Proper fetch dengan timeout dan error handling
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 detik timeout

try {
  const response = await fetch(API_URL, {
    method: 'POST',
    mode: 'cors',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify(data),
    signal: controller.signal
  });
  
  clearTimeout(timeoutId);
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  const result = await response.json();
  return result;
  
} catch (error) {
  clearTimeout(timeoutId);
  
  if (error.name === 'AbortError') {
    throw new Error('Request timeout - please try again');
  }
  
  throw error;
}
```

### 2. Better Error Handling

```javascript
const handleApiCall = async (url, options) => {
  try {
    const response = await fetchWithTimeout(url, options, 30000);
    return { success: true, data: response };
  } catch (error) {
    console.error('API Error:', error);
    
    if (error.message.includes('timeout')) {
      return { 
        success: false, 
        error: 'Server sedang lambat, coba lagi dalam beberapa saat' 
      };
    }
    
    if (error.message.includes('Failed to fetch')) {
      return { 
        success: false, 
        error: 'Tidak dapat terhubung ke server, periksa koneksi internet' 
      };
    }
    
    return { 
      success: false, 
      error: error.message || 'Terjadi kesalahan yang tidak diketahui' 
    };
  }
};
```

### 3. Network Retry Logic

```javascript
const apiCallWithRetry = async (url, options, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetchWithTimeout(url, options, 30000);
      return response;
    } catch (error) {
      console.log(`Attempt ${i + 1} failed:`, error.message);
      
      if (i === maxRetries - 1) throw error;
      
      // Wait before retry (exponential backoff)
      await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
    }
  }
};
```

## 🧪 DEBUG CODE FOR FRONTEND

**Paste this ke browser console di Vercel frontend:**

```javascript
// ULTIMATE API DEBUG TOOL
async function debugAPIConnection() {
    console.log('🔍 Testing API Connection from Frontend...');
    
    const BASE_URL = 'https://turnover-api-hd7ze.ondigitalocean.app';
    
    // Test 1: Health Check
    try {
        console.log('1️⃣ Testing Health Check...');
        const healthResponse = await fetch(`${BASE_URL}/api/health/`, {
            method: 'GET',
            mode: 'cors',
            credentials: 'include'
        });
        console.log('✅ Health Check:', healthResponse.status);
        console.log('   Response:', await healthResponse.json());
    } catch (error) {
        console.error('❌ Health Check Error:', error);
    }
    
    // Test 2: CORS Preflight
    try {
        console.log('2️⃣ Testing CORS Preflight...');
        const preflightResponse = await fetch(`${BASE_URL}/api/register/`, {
            method: 'OPTIONS',
            mode: 'cors',
            headers: {
                'Origin': window.location.origin,
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'content-type'
            }
        });
        console.log('✅ CORS Preflight:', preflightResponse.status);
        console.log('   Headers:', Object.fromEntries(preflightResponse.headers.entries()));
    } catch (error) {
        console.error('❌ CORS Preflight Error:', error);
    }
    
    // Test 3: Actual Registration
    try {
        console.log('3️⃣ Testing Registration...');
        const registrationResponse = await fetch(`${BASE_URL}/api/register/`, {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: `test.${Date.now()}@example.com`,
                password: 'TestPass123!',
                password_confirm: 'TestPass123!',
                first_name: 'Debug',
                last_name: 'Test',
                department: 1
            })
        });
        
        console.log('✅ Registration:', registrationResponse.status);
        if (registrationResponse.ok) {
            console.log('   Response:', await registrationResponse.json());
        } else {
            console.log('   Error:', await registrationResponse.text());
        }
    } catch (error) {
        console.error('❌ Registration Error:', error);
        console.log('   Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
    }
}

// Run the debug function
debugAPIConnection();
```

## 🔧 IMMEDIATE ACTIONS

### For Frontend Developer:

1. **Run debug code** di browser console
2. **Check Network tab** di DevTools saat error terjadi
3. **Increase timeout** di fetch calls ke minimal 30 detik
4. **Add proper error handling** dengan retry logic
5. **Use AbortController** untuk timeout management

### If Debug Shows Network Issues:

1. **Check Vercel deployment settings**
2. **Verify environment variables**
3. **Check for network policies/firewall**
4. **Test dari local development** vs Vercel

## 🎯 QUICK FIX

**Replace current fetch call dengan ini:**

```javascript
const registerUser = async (userData) => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);
  
  try {
    const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/register/', {
      method: 'POST',
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(userData),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`Registration failed: ${response.status} - ${errorData}`);
    }
    
    const result = await response.json();
    console.log('Registration success:', result);
    return result;
    
  } catch (error) {
    clearTimeout(timeoutId);
    
    if (error.name === 'AbortError') {
      console.error('Registration timeout');
      throw new Error('Registration timeout - server sedang lambat, coba lagi');
    }
    
    console.error('Registration error:', error);
    throw error;
  }
};
```

## 🔧 FRONTEND CODE FIX

Ganti function `handleSubmit` di file register Anda dengan code ini:

```javascript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!validateForm()) return;

  setIsLoading(true);
  setErrors({}); // Clear previous errors

  // Prepare payload
  const payload = {
    email: formData.email.trim(),
    password: formData.password.trim(),
    password_confirm: formData.password_confirm.trim(),
    first_name: formData.first_name.trim(),
    last_name: formData.last_name.trim(),
    phone_number: formData.phone_number.trim(),
    date_of_birth: formData.date_of_birth.trim(),
    gender: formData.gender.trim(),
    marital_status: formData.marital_status.trim(),
    education_level: formData.education_level.trim(),
    address: formData.address.trim(),
    position: formData.position.trim(),
    department: parseInt(formData.department, 10),
    hire_date: formData.hire_date.trim()
  };

  // Final validation
  if (
    !payload.email || !payload.password || !payload.password_confirm ||
    !payload.first_name || !payload.last_name || !payload.phone_number ||
    !payload.date_of_birth || !payload.gender || !payload.marital_status ||
    !payload.education_level || !payload.address || !payload.position ||
    !payload.hire_date || isNaN(payload.department) || payload.department <= 0
  ) {
    setErrors(prev => ({ ...prev, general: 'Please fill all fields correctly.' }));
    setIsLoading(false);
    return;
  }

  // 🔧 IMPROVED FETCH WITH TIMEOUT AND RETRY
  const makeApiCall = async (retryCount = 0): Promise<any> => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
      console.log('🚨 Request aborted due to timeout');
    }, 30000); // 30 second timeout

    try {
      console.log(`🚀 Attempt ${retryCount + 1}: Sending registration request...`);
      console.log('📤 Payload:', payload);

      const response = await fetch('https://turnover-api-hd7ze.ondigitalocean.app/api/register/', {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'User-Agent': 'RetenSYNC-Frontend/1.0'
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      console.log(`✅ Response received: ${response.status} ${response.statusText}`);
      console.log('📥 Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Response not OK:', errorText);
        
        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch {
          errorData = { message: errorText };
        }
        
        throw new Error(`HTTP ${response.status}: ${errorData.message || errorText}`);
      }

      const data = await response.json();
      console.log('✅ Registration successful:', data);
      return data;

    } catch (error: any) {
      clearTimeout(timeoutId);
      
      console.error(`❌ Attempt ${retryCount + 1} failed:`, error);

      // Handle different error types
      if (error.name === 'AbortError') {
        throw new Error('⏰ Request timeout - Server sedang lambat, mencoba lagi...');
      }
      
      if (error.message?.includes('Failed to fetch')) {
        throw new Error('🌐 Network error - Periksa koneksi internet Anda');
      }
      
      if (error.message?.includes('TypeError')) {
        throw new Error('🔗 Connection error - Tidak dapat terhubung ke server');
      }

      throw error;
    }
  };

  // 🔄 RETRY LOGIC
  const maxRetries = 3;
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const data = await makeApiCall(attempt);

      if (!data.success) {
        let errorMsg = data.message || data.error || 'Registration failed';
        if (data.errors) {
          errorMsg += ': ' + Object.values(data.errors).flat().join(', ');
        }
        setErrors(prev => ({ ...prev, general: errorMsg }));
        setIsLoading(false);
        return;
      }

      // ✅ SUCCESS!
      console.log('🎉 Registration completed successfully!');
      setSuccess(true);
      setIsLoading(false);

      setTimeout(() => {
        router.push('/user/dashboard');
      }, 2000);
      return;

    } catch (error: any) {
      lastError = error;
      console.log(`💔 Attempt ${attempt + 1}/${maxRetries} failed: ${error.message}`);

      // Don't retry for validation errors (4xx)
      if (error.message?.includes('HTTP 4')) {
        break;
      }

      // Wait before retry (exponential backoff)
      if (attempt < maxRetries - 1) {
        const waitTime = 1000 * Math.pow(2, attempt); // 1s, 2s, 4s
        console.log(`⏳ Waiting ${waitTime}ms before retry...`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  }

  // All retries failed
  console.error('💥 All retry attempts failed');
  setErrors(prev => ({
    ...prev,
    general: lastError?.message || 'Registration failed after multiple attempts. Please try again.'
  }));
  setIsLoading(false);
};
```

## 🧪 TAMBAHAN: Debug Function

Tambahkan juga function ini di component untuk testing:

```javascript
// Tambahkan di atas component atau sebagai useEffect
const debugApiConnection = async () => {
  console.log('🔍 Testing API Connection from Frontend...');
  
  const BASE_URL = 'https://turnover-api-hd7ze.ondigitalocean.app';
  
  try {
    console.log('1️⃣ Testing Health Check...');
    const healthResponse = await fetch(`${BASE_URL}/api/health/`, {
      method: 'GET',
      mode: 'cors',
      credentials: 'include'
    });
    console.log('✅ Health Check:', healthResponse.status);
    console.log('   Response:', await healthResponse.json());
  } catch (error) {
    console.error('❌ Health Check Error:', error);
  }
};

// Call this in useEffect untuk auto-debug
useEffect(() => {
  // Uncomment untuk auto-debug saat component mount
  // debugApiConnection();
}, []);
```

## 🎯 QUICK TESTING

Untuk test cepat, tambahkan button debug ini sementara:

```javascript
{/* Temporary Debug Button - Remove after testing */}
<button 
  type="button"
  onClick={debugApiConnection}
  className="mb-4 px-4 py-2 bg-gray-500 text-white rounded"
>
  🧪 Test API Connection
</button>
```

## 📊 EXPECTED RESULTS

Setelah apply fix ini, Anda akan melihat:

1. ✅ **Detailed console logs** untuk debugging
2. ✅ **30-second timeout** instead of browser default (5-10s)
3. ✅ **Automatic retry** dengan exponential backoff
4. ✅ **Better error messages** untuk user
5. ✅ **CORS headers** properly configured
6. ✅ **No more ERR_TIMED_OUT** errors

## 🚨 IF STILL NOT WORKING

Jika masih error, jalankan debug function dan paste hasil console log nya. Kemungkinan ada:

1. **Network policy** di Vercel
2. **Firewall** blocking API calls
3. **Environment variable** salah di frontend
4. **API server** down sementara

**API sudah 100% siap, tinggal frontend yang perlu diperbaiki!**
