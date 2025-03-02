from smolagents import tool


class FileTool:
    @staticmethod
    @tool
    def write_to_file(content: str, file_name: str = "output.txt", append: bool = False) -> str:
        """Writes content to a specified file.
        Args:
            content: The text content to write to the file
            file_name: The name of the file to write to. Defaults to 'output.txt'
            append: If True, appends the content instead of overwriting
        Returns:
            Message indicating if the write operation was successful
        """
        try:
            if append:
                try:
                    with open(file_name, "r") as f:
                        existing_content = f.read()
                    if content in existing_content:
                        return f"Content already exists in {file_name}"
                except FileNotFoundError:
                    pass

                mode = "a"
            else:
                mode = "w"

            with open(file_name, mode) as f:
                f.write(content if not append else f"\n{content}")

        except Exception as e:
            return f"Error writing to file: {e}"

    @staticmethod
    @tool
    def read_from_file(file_name: str) -> str:
        """Reads content from a specified file.
        Args:
            file_name: The name of the file to read from
        Returns:
            Content of the file or error message
        """
        try:
            with open(file_name, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
