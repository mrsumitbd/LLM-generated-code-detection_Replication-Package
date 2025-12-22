class _Node:

    @staticmethod
    def analyze_knowledge(state: State) -> dict:
        """Analyze the knowledge base and extract relevant information."""
        knowledge_base = state.get("knowledge_base", {})
        query = state.get("query", "")
        
        analysis_result = {
            "analyzed_knowledge": knowledge_base,
            "query_context": query,
            "relevant_topics": [],
            "confidence_score": 0.0
        }
        
        if knowledge_base and query:
            # Extract relevant topics from knowledge base based on query
            for key in knowledge_base.keys():
                if any(word in key.lower() for word in query.lower().split()):
                    analysis_result["relevant_topics"].append(key)
            
            analysis_result["confidence_score"] = min(1.0, len(analysis_result["relevant_topics"]) / max(1, len(query.split())))
        
        return analysis_result

    @staticmethod
    def call_tools(state: State) -> dict:
        """Call external tools based on the current state."""
        tools = state.get("tools", [])
        tool_inputs = state.get("tool_inputs", {})
        
        tool_results = {
            "tool_calls": [],
            "tool_outputs": [],
            "execution_status": "pending"
        }
        
        if tools:
            for tool in tools:
                try:
                    if callable(tool):
                        result = tool(**tool_inputs)
                        tool_results["tool_calls"].append(tool.__name__)
                        tool_results["tool_outputs"].append(result)
                except Exception as e:
                    tool_results["tool_outputs"].append({"error": str(e)})
            
            tool_results["execution_status"] = "completed"
        
        return tool_results

    @staticmethod
    def select_files(state: State) -> dict:
        """Select relevant files based on the current state."""
        available_files = state.get("available_files", [])
        selection_criteria = state.get("selection_criteria", {})
        
        selected_files = {
            "selected": [],
            "rejected": [],
            "selection_method": "criteria_based"
        }
        
        if available_files:
            for file in available_files:
                is_selected = True
                
                if "file_type" in selection_criteria:
                    if not file.endswith(selection_criteria["file_type"]):
                        is_selected = False
                
                if "keywords" in selection_criteria and is_selected:
                    keywords = selection_criteria["keywords"]
                    if not any(keyword in file.lower() for keyword in keywords):
                        is_selected = False
                
                if is_selected:
                    selected_files["selected"].append(file)
                else:
                    selected_files["rejected"].append(file)
        
        return selected_files