from flask import Flask, request, render_template

app = Flask(__name__)

# A "secret" configuration value that should not be exposed.
app.config['SECRET_KEY'] = 'a_very_secret_key_that_should_not_be_leaked'

@app.route('/')
def index():
    return render_template('index.html')

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
