class ConversationQualityAnalyzer:
    """Analyze code quality patterns in conversations."""

    def analyze_conversation_file(self, jsonl_path: Path) -> Dict[str, Any]:
        """Analyze a single conversation file for code quality patterns."""
        if not jsonl_path.exists():
            return self._default_quality()
        
        quality_metrics = {
            "file": str(jsonl_path),
            "total_messages": 0,
            "code_blocks": 0,
            "code_quality_score": 0.0,
            "patterns": {
                "has_error_handling": False,
                "has_type_hints": False,
                "has_docstrings": False,
                "has_tests": False,
                "has_comments": False,
            },
            "code_languages": {},
            "issues": [],
        }
        
        try:
            with open(jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    
                    try:
                        message = json.loads(line)
                        quality_metrics["total_messages"] += 1
                        
                        content = message.get("content", "")
                        
                        # Check for code blocks
                        code_blocks = re.findall(r'```(\w*)\n(.*?)\n```', content, re.DOTALL)
                        quality_metrics["code_blocks"] += len(code_blocks)
                        
                        # Analyze code patterns
                        if "try:" in content or "except" in content:
                            quality_metrics["patterns"]["has_error_handling"] = True
                        if "def " in content and ":" in content:
                            if re.search(r'def\s+\w+\([^)]*:\s*\w+', content):
                                quality_metrics["patterns"]["has_type_hints"] = True
                        if '"""' in content or "'''" in content:
                            quality_metrics["patterns"]["has_docstrings"] = True
                        if "test" in content.lower() or "assert" in content:
                            quality_metrics["patterns"]["has_tests"] = True
                        if "#" in content:
                            quality_metrics["patterns"]["has_comments"] = True
                        
                        # Track code languages
                        for lang, code in code_blocks:
                            lang = lang if lang else "plaintext"
                            quality_metrics["code_languages"][lang] = quality_metrics["code_languages"].get(lang, 0) + 1
                    
                    except json.JSONDecodeError:
                        quality_metrics["issues"].append(f"Invalid JSON in line")
        
        except Exception as e:
            quality_metrics["issues"].append(str(e))
        
        # Calculate quality score
        pattern_score = sum(1 for v in quality_metrics["patterns"].values() if v) / len(quality_metrics["patterns"])
        code_score = min(quality_metrics["code_blocks"] / max(1, quality_metrics["total_messages"]), 1.0)
        quality_metrics["code_quality_score"] = (pattern_score * 0.6 + code_score * 0.4)
        
        return quality_metrics

    def _default_quality(self) -> Dict[str, Any]:
        """Return default quality metrics structure."""
        return {
            "file": None,
            "total_messages": 0,
            "code_blocks": 0,
            "code_quality_score": 0.0,
            "patterns": {
                "has_error_handling": False,
                "has_type_hints": False,
                "has_docstrings": False,
                "has_tests": False,
                "has_comments": False,
            },
            "code_languages": {},
            "issues": ["File not found or unable to read"],
        }

    def analyze_project(self, project_path: Path, limit: int = 5) -> Dict[str, Any]:
        """Analyze multiple conversation files in a project."""
        import json
        import re
        
        project_path = Path(project_path)
        
        if not project_path.exists():
            return {
                "project": str(project_path),
                "status": "error",
                "message": "Project path does not exist",
                "files_analyzed": 0,
                "results": [],
            }
        
        results = []
        jsonl_files = list(project_path.glob("**/*.jsonl"))[:limit]
        
        for jsonl_file in jsonl_files:
            analysis = self.analyze_conversation_file(jsonl_file)
            results.append(analysis)
        
        # Calculate aggregate metrics
        total_messages = sum(r.get("total_messages", 0) for r in results)
        total_code_blocks = sum(r.get("code_blocks", 0) for r in results)
        avg_quality_score = (
            sum(r.get("code_quality_score", 0) for r in results) / len(results)
            if results
            else 0.0
        )
        
        return {
            "project": str(project_path),
            "status": "success",
            "files_analyzed": len(results),
            "total_messages": total_messages,
            "total_code_blocks": total_code_blocks,
            "average_quality_score": avg_quality_score,
            "results": results,
        }