# How It Works

## Overview

Propella is a Django-based platform for exam preparation and user management. It includes features for user registration, authentication, exam profiles, subscriptions, referrals, and admin access. The API uses Django REST Framework with JWT authentication.

## Authentication Flows

Propella uses JWT (JSON Web Tokens) for secure authentication. Here's a guide for frontend developers on how authentication works:

### JWT Basics
- **Access Token**: Short-lived token (15-30 minutes) used for API requests.
- **Refresh Token**: Long-lived token used to get new access tokens without re-login.
- **Storage**: Store tokens securely (localStorage for web apps, secure storage for mobile).

#### Common HTTP Headers
- `Content-Type: application/json` for request bodies.
- `Authorization: Bearer <access_token>` for authenticated endpoints.

#### Token Storage Tips (Frontend)
- Store the **access token** in memory (state) for best security; refresh it before it expires.
- Store the **refresh token** in a secure place (e.g., HttpOnly cookie or secure storage) and never expose it to JavaScript if possible.
- If using localStorage, check for XSS protection (sanitize inputs, use CSP headers).

### User Registration and Login Flow

1. **User Signs Up**
   - Call: POST /api/accounts/register/
   - User receives email verification code.

2. **Verify Email**
   - Call: POST /api/accounts/verify-email/
   - User enters code to activate account.

3. **User Logs In**
   - Call: POST /api/accounts/token/
   - Receive access and refresh tokens.
   - Store tokens for future requests.

4. **Making Authenticated Requests**
   - Add header: `Authorization: Bearer <access_token>`
   - Include `Content-Type: application/json` for POST/PUT requests.

5. **Token Refresh**
   - When access token expires, call POST /api/accounts/token/refresh/ with refresh token.
   - Get new access token, update storage.

6. **Logout**
   - Clear stored tokens from storage.
   - Optional: Call logout endpoint if needed.

### Admin Authentication
- Admins use separate login: POST /api/core/login-admin/
- Same JWT flow applies.

### Error Handling
- 401 Unauthorized: Token expired or invalid → refresh token or re-login.
- 403 Forbidden: Insufficient permissions.
- 400 Bad Request: Validation errors.

## API Endpoints

### 1. Register User
**Method:** POST  
**URL:** /api/accounts/register/  
**Description:** Registers a new user account. Call this when user submits signup form.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string", "password": "string", "referral_code": "string (optional)"}`  
**Success Response (201):**  
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "is_verified": false,
    "referral_code": "ABC123"
  }
}
```  
**Error Response (400):**  
```json
{
  "error": "Email already exists"
}
```

### 2. Verify Email
**Method:** POST  
**URL:** /api/accounts/verify-email/  
**Description:** Verifies user email with verification code. Call after user receives email.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string", "code": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Email verified successfully"
}
```  
**Error Response (400):**  
```json
{
  "error": "Invalid verification code"
}
```

### 3. Resend Verification Code
**Method:** POST  
**URL:** /api/accounts/resend-code/  
**Description:** Resends verification code if user didn't receive it. Call on "Resend Code" button.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Verification code sent"
}
```  
**Error Response (400):**  
```json
{
  "error": "User not found"
}
```

### 4. Login (Token)
**Method:** POST  
**URL:** /api/accounts/token/  
**Description:** Authenticates user and returns JWT tokens. Call on login form submit.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string", "password": "string"}`  
**Success Response (200):**  
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```  
**Error Response (401):**  
```json
{
  "detail": "No active account found with the given credentials"
}
```

### 4b. Login (User Info)
**Method:** POST  
**URL:** /api/accounts/login/  
**Description:** Authenticates user and returns JWT tokens plus basic user info. Call on login form submit when you need the authenticated user's ID and username along with tokens.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string", "password": "string"}`  
**Success Response (200):**  
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "user"
    }
  }
}
```  
**Error Response (400):**  
```json
{
  "success": false,
  "errors": {
    "non_field_errors": ["Invalid email or password"]
  }
}
```

### 5. Refresh Token
**Method:** POST  
**URL:** /api/accounts/token/refresh/  
**Description:** Gets new access token using refresh token. Call automatically when access token expires.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"refresh": "string"}`  
**Success Response (200):**  
```json
{
  "access": "new_jwt_access_token"
}
```  
**Error Response (401):**  
```json
{
  "detail": "Token is invalid or expired"
}
```

### 6. Change Password
**Method:** POST  
**URL:** /api/accounts/change-password/  
**Description:** Changes user password. Call from password change form.  
**Authentication:** JWT (access token)  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"old_password": "string", "new_password": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Password changed successfully"
}
```  
**Error Response (400):**  
```json
{
  "error": "Old password is incorrect"
}
```

### 7. Get All Users
**Method:** GET  
**URL:** /api/accounts/all-users/  
**Description:** Retrieves list of all users (admin only). Call for admin dashboard.  
**Authentication:** JWT (admin)  
**Headers:** Authorization: Bearer {token}  
**Parameters:** None  
**Success Response (200):**  
```json
[
  {
    "id": 1,
    "email": "user@example.com",
    "is_verified": true
  }
]
```  
**Error Response (403):**  
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 8. Edit User
**Method:** PUT  
**URL:** /api/accounts/edit-user/  
**Description:** Updates user profile. Call from profile edit form.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"email": "string", "first_name": "string", etc.}`  
**Success Response (200):**  
```json
{
  "message": "User updated successfully",
  "user": { ... }
}
```  
**Error Response (400):**  
```json
{
  "error": "Validation error"
}
```

### 9. Create Exam Profile
**Method:** POST  
**URL:** /api/accounts/create-exam-profile/  
**Description:** Creates an exam profile for the user. Call after user selects exam type and subjects.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"exam_type": "string", "subjects": ["string"]}`  
**Success Response (201):**  
```json
{
  "message": "Exam profile created",
  "profile": { ... }
}
```  
**Error Response (400):**  
```json
{
  "error": "Profile already exists"
}
```

### 10. Edit Exam Profile
**Method:** PUT  
**URL:** /api/accounts/edit-exam-profile/  
**Description:** Updates exam profile. Call when user modifies their exam preferences.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"exam_type": "string", "subjects": ["string"]}`  
**Success Response (200):**  
```json
{
  "message": "Profile updated",
  "profile": { ... }
}
```  
**Error Response (400):**  
```json
{
  "error": "Validation error"
}
```

### 10b. Get Current Exam Profile
**Method:** GET  
**URL:** /api/accounts/current_exam_profile/  
**Description:** Retrieves the current user's exam profile. Call to pre-populate profile forms or display the user's current exam settings.  
**Authentication:** JWT  
**Headers:** Authorization: Bearer {token}  
**Parameters:** None  
**Success Response (200):**  
```json
{
  "id": 1,
  "user": 1,
  "exam_date": "2024-12-31",
  "daily_hours": 3,
  "personality": "Focused",
  "learning_format": "text",
  "voice_pref": "female"
}
```  
**Error Response (404):**  
```json
{
  "error": "Exam profile not found"
}
```

### 11. My Referrals
**Method:** GET  
**URL:** /api/accounts/my-referrals/  
**Description:** Gets user's referrals. Call to display referral list in user dashboard.  
**Authentication:** JWT  
**Headers:** Authorization: Bearer {token}  
**Parameters:** None  
**Success Response (200):**  
```json
{
  "referrals": [
    {
      "email": "ref@example.com",
      "joined_at": "2023-01-01"
    }
  ]
}
```  
**Error Response (401):**  
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 12. Get Plans
**Method:** GET  
**URL:** /api/accounts/plans/  
**Description:** Retrieves available subscription plans. Call to show pricing options.  
**Authentication:** JWT  
**Headers:** Authorization: Bearer {token}  
**Parameters:** None  
**Success Response (200):**  
```json
[
  {
    "id": 1,
    "name": "Basic",
    "price": 10.00
  }
]
```  
**Error Response (401):**  
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 13. Subscribe
**Method:** POST  
**URL:** /api/accounts/subscribe/  
**Description:** Subscribes user to a plan. Call after user selects a plan. Returns payment URL.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"plan_id": 1}`  
**Success Response (200):**  
```json
{
  "message": "Subscription initiated",
  "payment_url": "https://..."
}
```  
**Error Response (400):**  
```json
{
  "error": "Invalid plan"
}
```

### 14. Verify Subscription
**Method:** POST  
**URL:** /api/accounts/verify-subscription/  
**Description:** Verifies payment and activates subscription. Call after payment completion.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"transaction_id": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Subscription activated"
}
```  
**Error Response (400):**  
```json
{
  "error": "Payment verification failed"
}
```

### 14b. Subscription Status
**Method:** GET  
**URL:** /api/accounts/subscription-status/  
**Description:** Check whether the current user has an active subscription and returns plan status + subscription details if active. Call to display subscription status on user dashboard.  
**Authentication:** JWT  
**Headers:** Authorization: Bearer {token}  
**Parameters:** None  
**Success Response (active subscription, 200):**  
```json
{
  "active": true,
  "plan": "Basic",
  "expires_at": "2024-12-31T23:59:59Z",
  "days_remaining": 20,
  "subscription": {
    "id": 1,
    "user": 1,
    "plan": 1,
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-12-31T23:59:59Z",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```  
**Success Response (no active subscription or expired, 200):**  
```json
{
  "active": false
}
```

### 15. Forgot Password
**Method:** POST  
**URL:** /api/accounts/forgot-password/  
**Description:** Sends password reset email. Call from forgot password form.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"email": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Password reset email sent"
}
```  
**Error Response (400):**  
```json
{
  "error": "User not found"
}
```

### 16. Reset Password
**Method:** POST  
**URL:** /api/accounts/reset-password/  
**Description:** Resets password with reset token. Call from reset password form.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"token": "string", "new_password": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Password reset successfully"
}
```  
**Error Response (400):**  
```json
{
  "error": "Invalid token"
}
```

### 17. Admin Login
**Method:** POST  
**URL:** /api/core/login-admin/  
**Description:** Logs in admin user. Call for admin login.  
**Authentication:** None  
**Headers:** Content-Type: application/json  
**Parameters:**  
- Body: `{"username": "string", "password": "string"}`  
**Success Response (200):**  
```json
{
  "access": "jwt_token",
  "refresh": "jwt_refresh"
}
```  
**Error Response (401):**  
```json
{
  "detail": "Invalid credentials"
}
```

### 18. Admin Logout
**Method:** POST  
**URL:** /api/core/logout-admin/  
**Description:** Logs out admin. Call on admin logout.  
**Authentication:** JWT  
**Headers:** Content-Type: application/json, Authorization: Bearer {token}  
**Parameters:**  
- Body: `{"refresh": "string"}`  
**Success Response (200):**  
```json
{
  "message": "Logged out"
}
```  
**Error Response (400):**  
```json
{
  "error": "Invalid token"
}
```

### 19. API Documentation
**Method:** GET  
**URL:** /api/docs/  
**Description:** Displays API documentation page. Call to view interactive docs.  
**Authentication:** None  
**Parameters:** None  
**Response:** HTML page with API docs.