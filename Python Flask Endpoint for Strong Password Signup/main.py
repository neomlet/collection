from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Common passwords list (for demonstration - should be more comprehensive in production)
COMMON_PASSWORDS = {
    'password', '123456', '123456789', 'qwerty', 'abc123',
    'password1', 'admin', 'letmein', 'welcome', 'monkey'
}

def validate_password(password):
    """Validate password against strong security requirements"""
    errors = []
    
    # Minimum length check
    if len(password) < 12:
        errors.append("Password must be at least 12 characters long")
        
    # Character diversity checks
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    if not re.search(r'[@$!%*?&#]', password):
        errors.append("Password must contain at least one special character (@$!%*?&#)")
        
    # Check against common passwords
    if password.lower() in COMMON_PASSWORDS:
        errors.append("Password is too common and insecure")
        
    return errors

@app.route('/signup', methods=['POST'])
def signup():
    # Validate request format
    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Request must be in JSON format"
        }), 400
        
    data = request.get_json()
    
    # Check required fields
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": "Email and password are required fields"
        }), 400
    
    email = data['email']
    password = data['password']
    
    # Validate password strength
    if password_errors := validate_password(password):
        return jsonify({
            "success": False,
            "message": "Password validation failed",
            "errors": password_errors
        }), 400
        
    # TODO: In production, add email validation and proper password hashing
    # Example: hashed_password = generate_password_hash(password)
    # save_to_database(email, hashed_password)
    
    return jsonify({
        "success": True,
        "message": "User created successfully",
        "email": email
    }), 201

if __name__ == '__main__':
    app.run(debug=True)