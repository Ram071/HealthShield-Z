import json
import os

with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()
with open('src/__init__.py', 'r', encoding='utf-8') as f:
    init_code = f.read()
with open('src/model.py', 'r', encoding='utf-8') as f:
    model_code = f.read()

files_dict = {
    'app.py': app_code,
    'src/__init__.py': init_code,
    'src/model.py': model_code
}

files_json = json.dumps(files_dict)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
  <title>HealthShield Z — Privacy-Preserving AI Healthcare Risk Analytics</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.59.0/build/stlite.css" />
  <style>
    body {
      margin: 0;
      padding: 0;
      background: #0e1117;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    #loading {
      color: #fafafa;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: system-ui, -apple-system, sans-serif;
      text-align: center;
      padding: 20px;
    }
    .spinner {
      width: 50px;
      height: 50px;
      border: 5px solid rgba(255,255,255,0.2);
      border-radius: 50%;
      border-top-color: #ff4b4b;
      animation: spin 1s ease-in-out infinite;
      margin-bottom: 20px;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div id="root">
    <div id="loading">
      <div class="spinner"></div>
      <h2>🛡️ HealthShield Z is Loading...</h2>
      <p>Initializing in-browser WebAssembly Python environment & Scikit-Learn ML engine.<br>First load may take ~10-15 seconds.</p>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.59.0/build/stlite.js"></script>
  <script>
    const files = __FILES_JSON__;
    stlite.mount({
      requirements: ["pandas", "numpy", "scikit-learn"],
      entrypoint: "app.py",
      files: files
    }, document.getElementById("root"));
  </script>
</body>
</html>
"""

html_content = html_template.replace("__FILES_JSON__", files_json)

os.makedirs('docs', exist_ok=True)
with open('docs/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated docs/index.html successfully, size: {os.path.getsize('docs/index.html')} bytes")
