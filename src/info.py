# Email Info

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_HOST_USER = 'jesikamaraj@gmail.com'
EMAIL_HOST_PASSWORD = 'cavEq1HhCGXsAP3p'
EMAIL_PORT = 587

#  Social Auth Configuration

SOCIAL_LOGIN_BOOL = True

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

SOCIAL_AUTH_GITHUB_KEY = 'c9527e0e2deaaa91a62b'
SOCIAL_AUTH_GITHUB_SECRET = 'aa64200e0f77651730044994a1f593bd7a6564a4'

SOCIAL_AUTH_TWITTER_KEY = 'MGpWRUotbWoxRlJNRnZfOUN2WkE6MTpjaQ'
SOCIAL_AUTH_TWITTER_SECRET = 'w0TSkK5jA-DKCEwybNhcTx7hZf3iAySr5tPMaukv3u4-A0M-fK'

SOCIAL_AUTH_FACEBOOK_KEY = '2516052301859285'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'c1764627ebbd4631d68056a6d7f4bb70'  # App Secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '860410036745-puf0m3e4scnejr3ljvtrocb2kegkekqe.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# Redirect Fields

REDIRECT_AFTER_LOGIN = 'home'
REDIRECT_AFTER_LOGOUT = 'login'
REDIRECT_AFTER_SIGNUP = 'login'

# Couldinary fields
CLOUDINARY = {
  'cloud_name': 'kevinnadar',  
  'api_key': '392621114285936',  
  'api_secret': '2h4qbdlIwx6cDgNtmtXWlv5PdYg',  
}

# Crispy Fields

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# 2 Factor Authentication

TWOFACTORIN_API = "2d11b81d-e8f5-11ec-9c12-0200cd936042"


# Razor Pay Api

RAZORPAY_API = "rzp_test_3ajxrW0egvrWbK"
RAZORPAY_API_SECRET = "cNJQ4kfETFUTt0DTsPixWbzP"