create-env:
create-env:
    @echo "Creating Conda environment..."
    conda create --name social_media --file requirements.txt
    @echo "Activating the environment..."
    conda activate     conda create --name social_media --file requirements.txt
    @echo "Setting up Visual Studio Code Interpreter..."
    python -c "import json, os; settings = {'python.pythonPath': os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')}; open('.vscode/settings.json', 'w').write(json.dumps(settings))"
