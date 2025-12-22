def get_nothink_str(llm: LLM):
    result = ""
    current = llm.head
    while current is not None:
        result += str(current.data)
        current = current.next
    return result