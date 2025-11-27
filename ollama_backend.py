import subprocess

def ask_ollama(prompt):
    """
    Sends a question to Ollama CLI and returns the answer as text.
    Works reliably on Windows.
    """
    try:
        # Run Ollama CLI command
        result = subprocess.run(
            ["ollama", "run", "llama3.1-8b", "--prompt", prompt],
            capture_output=True,
            text=True,
            shell=True  # Important for Windows
        )
        
        # Check for errors
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        
        # Return the AI's response
        return result.stdout.strip()
    
    except Exception as e:
        return f"Exception: {str(e)}"
