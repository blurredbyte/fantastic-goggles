from flask import Flask, request

app = Flask(__name__)

# A "secret" configuration value that should not be exposed.
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_not_be_leaked'

@app.route('/')
def index():
    return '<h1>Insecure Error Handling Demo</h1><p>This application is running in debug mode.</p><p>Try to trigger an error by visiting a non-existent page like <a href="/divide?a=10&b=0">/divide?a=10&b=0</a>.</p>'

@app.route('/divide')
def divide():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    # This will raise a ZeroDivisionError if b is 0
    result = a / b
    return f'The result is {result}'

# This is the VULNERABLE part. Running with debug=True in a production
# environment is a major security risk. When an unhandled exception occurs,
# Flask's debug mode will show an interactive debugger in the browser,
# which can leak sensitive information about the code, configuration, and environment.
if __name__ == '__main__':
    # NEVER run with debug=True in production!
    app.run(debug=True, port=5003)
