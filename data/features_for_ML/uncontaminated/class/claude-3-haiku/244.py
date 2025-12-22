from pathlib import Path
from typing import Dict, Any
import json

class ConversationQualityAnalyzer:
    """Analyze code quality patterns in conversations."""

    def analyze_conversation_file(self, jsonl_path: Path) -> Dict[str, Any]:
        quality_metrics = self._default_quality()
        with open(jsonl_path, 'r') as file:
            for line in file:
                conversation = json.loads(line)
                quality_metrics = self._analyze_conversation(conversation, quality_metrics)
        return quality_metrics

    def _default_quality(self) -> Dict[str, Any]:
        return {
            'total_messages': 0,
            'avg_message_length': 0.0,
            'num_questions': 0,
            'num_code_blocks': 0,
            'num_links': 0,
            'num_emojis': 0
        }

    def _analyze_conversation(self, conversation: Dict[str, Any], quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        quality_metrics['total_messages'] += len(conversation['messages'])
        total_length = 0
        num_questions = 0
        num_code_blocks = 0
        num_links = 0
        num_emojis = 0

        for message in conversation['messages']:
            total_length += len(message['text'])
            num_questions += message['text'].count('?')
            num_code_blocks += len(message['code_blocks'])
            num_links += len(message['links'])
            num_emojis += len(message['emojis'])

        quality_metrics['avg_message_length'] = total_length / quality_metrics['total_messages']
        quality_metrics['num_questions'] += num_questions
        quality_metrics['num_code_blocks'] += num_code_blocks
        quality_metrics['num_links'] += num_links
        quality_metrics['num_emojis'] += num_emojis

        return quality_metrics

    def analyze_project(self, project_path: Path, limit: int = 5) -> Dict[str, Any]:
        quality_metrics = self._default_quality()
        conversation_files = [f for f in project_path.glob('*.jsonl')][:limit]
        for file in conversation_files:
            quality_metrics = self.analyze_conversation_file(file)
        return quality_metrics