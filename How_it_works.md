# How It Works

## Overview

Propella is a Django-based platform for exam preparation and user management. It includes features for user registration, authentication, exam profiles, subscriptions, referrals, and admin access. The API uses Django REST Framework with JWT authentication.

## API Endpoints

### 1. Register User
**Method:** POST  
**URL:** /api/accounts/register/  
**Description:** Registers a new user account.  
**Authentication:** None  
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
**Description:** Verifies user email with a code.  
**Authentication:** None  
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
**Description:** Resends verification code to email.  
**Authentication:** None  
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
**Description:** Authenticates user and returns JWT tokens.  
**Authentication:** None  
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

### 5. Refresh Token
**Method:** POST  
**URL:** /api/accounts/token/refresh/  
**Description:** Refreshes access token using refresh token.  
**Authentication:** None  
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
**Description:** Changes user password.  
**Authentication:** JWT (access token)  
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
**Description:** Retrieves list of all users (admin only).  
**Authentication:** JWT (admin)  
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
**Description:** Updates user profile.  
**Authentication:** JWT  
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
**Description:** Creates an exam profile for the user.  
**Authentication:** JWT  
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
**Description:** Updates exam profile.  
**Authentication:** JWT  
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

### 11. My Referrals
**Method:** GET  
**URL:** /api/accounts/my-referrals/  
**Description:** Gets user's referrals.  
**Authentication:** JWT  
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
**Description:** Retrieves available subscription plans.  
**Authentication:** JWT  
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
**Description:** Subscribes user to a plan.  
**Authentication:** JWT  
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
**Description:** Verifies payment and activates subscription.  
**Authentication:** JWT  
**Parameters:**  
- Body: `{"reference": "string"}`  
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

### 15. Forgot Password
**Method:** POST  
**URL:** /api/accounts/forgot-password/  
**Description:** Sends password reset email.  
**Authentication:** None  
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
**Description:** Resets password with token.  
**Authentication:** None  
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
**Description:** Logs in admin user.  
**Authentication:** None  
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
**Description:** Logs out admin.  
**Authentication:** JWT  
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
**Description:** Displays API documentation page.  
**Authentication:** None  
**Parameters:** None  
**Response:** HTML page with API docs.