from langchain.tools import Tool

class ReverseTextTool(Tool):
    def __init__(self):
        super().__init__(name="ReverseTextTool", description="A tool that reverses the input text.")

    def run(self, input_text):
        # Custom logic for the tool: reversing the input text
        return input_text[::-1]