from markitdown import MarkItDown

def convert(path: str) -> None:
        converter = MarkItDown()
        result = converter.convert_local(path)
        print("TITLE:" + (result.title or ""))
        print("CONTENT:" + result.text_content)