import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))
        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]
        if args:
            command.extend(args)

        results = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = []
        if results.returncode != 0:
            output.append(f"Process exited with {results.returncode}")
        if not results.stderr and not results.stdout:
            output.append("No output produced")
        if results.stderr:
            output.append(f"STDERR:\n{results.stderr}")
        if results.stdout:
            output.append(f"STDOUT:\n{results.stdout}")
        return "\n".join(output)

    except Exception as E:
        return f'Error: executing Python file: {E}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)



