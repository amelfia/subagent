import os

from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))
        if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        for filename in os.listdir(target_directory):
            filepath = os.path.join(target_directory, filename)
            size = os.path.getsize(filepath)
            is_directory = os.path.isdir(filepath)
            files_info.append(f"- {filename}: file_size={size} bytes, is_dir={is_directory}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)









