import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_directory_abs, file_path))

        if os.path.commonpath([working_directory_abs, file_path_abs]) != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(working_directory_abs), exist_ok=True)
        with open(file_path_abs,"w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as E:
        return f'Error: writing to file: {E}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory (overwriting if the file exists)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
