from .views import DOMElementNode

def process_node(node: DOMBaseNode, depth: int) -> None:
			if isinstance(node, DOMElementNode):
				# Add element with highlight_index
				if node.highlight_index is not None:
					attributes_str = ''
					text = node.get_all_text_till_next_clickable_element()
					if include_attributes:
						attributes = list(
							set(
								[
									f"{str(key)}={str(value)}"
									for key, value in node.attributes.items()
									if key in include_attributes and value != node.tag_name
								]
							)
						)
						if text in attributes:
							attributes.remove(text)
						attributes_str = ';'.join(attributes)
					line = f'[{node.highlight_index}]<{node.tag_name} '
					if attributes_str:
						line += f'{attributes_str}'
					if text:
						if attributes_str:
							line += f'>{text}'
						else:
							line += f'{text}'
					line += '/>'
					formatted_text.append(line)

				# Process children regardless
				for child in node.children:
					process_node(child, depth + 1)

			elif isinstance(node, DOMTextNode):
				# Add text only if it doesn't have a highlighted parent
				if not node.has_parent_with_highlight_index() and node.is_visible:  # and node.is_parent_top_element()
					formatted_text.append(f'{node.text}')