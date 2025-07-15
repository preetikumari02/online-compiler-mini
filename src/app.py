from flask import Flask, render_template, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code')
    user_input = request.form.get('input', '')  # Get user input
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    # Create temporary files with unique names
    filename = f"temp_{uuid.uuid4().hex}.cpp"
    executable = f"temp_{uuid.uuid4().hex}"
    input_file = f"temp_input_{uuid.uuid4().hex}.txt"
    
    try:
        # Write code to file
        with open(filename, 'w') as f:
            f.write(code)
        
        # Write input to file if provided
        if user_input:
            with open(input_file, 'w') as f:
                f.write(user_input)
        
        # Compile the code
        compile_result = subprocess.run(
            ['g++', filename, '-o', executable],
            capture_output=True,
            text=True
        )
        
        if compile_result.returncode != 0:
            return jsonify({
                'error': 'Compilation failed',
                'output': compile_result.stderr
            })
        
        # Run the executable with input if provided
        if user_input:
            with open(input_file, 'r') as input_f:
                run_result = subprocess.run(
                    [f'./{executable}'],
                    stdin=input_f,
                    capture_output=True,
                    text=True
                )
        else:
            run_result = subprocess.run(
                [f'./{executable}'],
                capture_output=True,
                text=True
            )
        
        output = run_result.stdout
        if run_result.stderr:
            output += "\n" + run_result.stderr
        
        return jsonify({
            'output': output
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up
        for file in [filename, executable, input_file]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)