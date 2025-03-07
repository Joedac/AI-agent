import os
from smolagents import tool

FILES_DIR = "files"

if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)


class FileTool:
    @staticmethod
    @tool
    def write_to_file(
        content: str, file_name: str = "output.txt", append: bool = False
    ) -> str:
        """Writes content to a specified file inside the 'files/' directory.
        Args:
            content: The text content to write to the file
            file_name: The name of the file to write to. Defaults to 'output.txt'
            append: If True, appends the content instead of overwriting
        Returns:
            Message indicating if the write operation was successful
        """
        file_path = os.path.join(FILES_DIR, file_name)

        try:
            if append:
                try:
                    with open(file_path, "r") as f:
                        existing_content = f.read()
                    if content in existing_content:
                        return f"Content already exists in {file_name}"
                except FileNotFoundError:
                    pass

                mode = "a"
            else:
                mode = "w"

            with open(file_path, mode) as f:
                f.write(content if not append else f"\n{content}")

            return f"Content written to {file_name} in {FILES_DIR}/"

        except Exception as e:
            return f"Error writing to file: {e}"

    @staticmethod
    @tool
    def read_from_file(file_name: str) -> str:
        """Reads content from a specified file inside the 'files/' directory.
        Args:
            file_name: The name of the file to read from
        Returns:
            Content of the file or error message
        """
        file_path = os.path.join(FILES_DIR, file_name)

        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
