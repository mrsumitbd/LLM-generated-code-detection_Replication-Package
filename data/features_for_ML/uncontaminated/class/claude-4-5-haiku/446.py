from typing import Any, Dict, List
from datetime import datetime

class AdaptiveResponseFormatter:
    """Format responses based on available data and context quality."""

    def __init__(self):
        pass

    def format_response(self, data: Any, quality_assessment: Dict[str, Any]) -> Any:
        quality_score = quality_assessment.get('quality_score', 0)
        
        if quality_score >= 0.8:
            formatted = self._comprehensive_format(data)
        elif quality_score >= 0.5:
            formatted = self._partial_format_with_gaps(data)
        else:
            formatted = self._minimal_format_with_guidance(data)
        
        return self._add_quality_indicators(formatted, quality_assessment)

    def _comprehensive_format(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                'executive_summary': self._generate_executive_summary(data),
                'detailed_findings': self._extract_detailed_findings(data),
                'risk_assessment': self._perform_risk_assessment(data),
                'recommendations': self._generate_actionable_recommendations(data),
                'key_metrics': self._extract_key_metrics(data),
                'timeline': self._build_timeline(data)
            }
        return data

    def _partial_format_with_gaps(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                'summary': self._generate_partial_summary(data),
                'key_findings': self._extract_key_findings(data),
                'preliminary_assessment': self._perform_preliminary_assessment(data),
                'incomplete_areas': self._identify_incomplete_areas(data),
                'confidence_levels': self._assess_confidence_levels(data),
                'next_steps': self._suggest_data_gathering_actions(data)
            }
        return data

    def _minimal_format_with_guidance(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {
                'basic_info': self._extract_basic_info(data),
                'initial_observations': self._make_initial_observations(data),
                'data_requirements': self._specify_data_requirements(data),
                'troubleshooting_tips': self._provide_troubleshooting_tips(data),
                'feature_enablement': self._suggest_feature_enablement(),
                'configuration_guidance': self._provide_configuration_guidance()
            }
        return data

    def _add_quality_indicators(self, formatted_data: Any, quality_assessment: Dict[str, Any]) -> Any:
        if isinstance(formatted_data, dict):
            formatted_data['quality_indicators'] = {
                'quality_score': quality_assessment.get('quality_score', 0),
                'completeness': quality_assessment.get('completeness', 0),
                'reliability': quality_assessment.get('reliability', 0),
                'timestamp': datetime.now().isoformat()
            }
        return formatted_data

    def _generate_executive_summary(self, data: Dict[str, Any]) -> str:
        summary_parts = []
        if 'title' in data:
            summary_parts.append(f"Overview: {data['title']}")
        if 'status' in data:
            summary_parts.append(f"Status: {data['status']}")
        if 'metrics' in data:
            summary_parts.append(f"Key metrics identified: {len(data['metrics'])} items")
        return " | ".join(summary_parts) if summary_parts else "Comprehensive analysis completed"

    def _extract_detailed_findings(self, data: Dict[str, Any]) -> List[str]:
        findings = []
        if 'findings' in data:
            findings.extend(data['findings'] if isinstance(data['findings'], list) else [str(data['findings'])])
        if 'analysis' in data:
            findings.append(f"Analysis: {data['analysis']}")
        if 'results' in data:
            findings.append(f"Results: {data['results']}")
        return findings if findings else ["No detailed findings available"]

    def _perform_risk_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'overall_risk': self._calculate_overall_risk(data),
            'critical_issues': self._identify_critical_issues(data),
            'risk_factors': self._analyze_risk_factors(data),
            'impact_scope': self._assess_impact_scope(data),
            'priority_score': self._calculate_priority_score(data)
        }

    def _generate_actionable_recommendations(self, data: Dict[str, Any]) -> List[str]:
        recommendations = []
        if 'issues' in data:
            recommendations.append("Address identified issues systematically")
        if 'improvements' in data:
            recommendations.extend(data['improvements'] if isinstance(data['improvements'], list) else [data['improvements']])
        recommendations.extend(self._identify_immediate_actions(data))
        return recommendations if recommendations else ["Continue monitoring"]

    def _generate_partial_summary(self, data: Dict[str, Any]) -> str:
        parts = []
        if 'title' in data:
            parts.append(f"Partial analysis: {data['title']}")
        parts.append("Some data gaps detected")
        if 'status' in data:
            parts.append(f"Current status: {data['status']}")
        return " | ".join(parts) if parts else "Partial analysis with data gaps"

    def _extract_key_findings(self, data: Dict[str, Any]) -> List[str]:
        findings = []
        if 'findings' in data:
            findings.extend(data['findings'] if isinstance(data['findings'], list) else [str(data['findings'])])
        findings.extend(self._identify_trends(data))
        findings.extend(self._highlight_anomalies(data))
        return findings if findings else ["Limited findings due to data gaps"]

    def _perform_preliminary_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'preliminary_findings': self._get_preliminary_findings(data),
            'trends': self._identify_trends(data),
            'anomalies': self._highlight_anomalies(data),
            'correlations': self._identify_correlations(data)
        }

    def _extract_basic_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        basic = {}
        for key in ['title', 'status', 'type', 'source', 'timestamp']:
            if key in data:
                basic[key] = data[key]
        return basic if basic else {'status': 'Data received'}

    def _make_initial_observations(self, data: Dict[str, Any]) -> List[str]:
        observations = []
        if 'status' in data:
            observations.append(f"Current status: {data['status']}")
        if 'type' in data:
            observations.append(f"Data type: {data['type']}")
        observations.append("Initial assessment in progress")
        return observations

    def _suggest_next_steps(self, data: Dict[str, Any]) -> List[str]:
        steps = []
        steps.append("Gather additional data points")
        steps.append("Validate current information")
        if 'issues' in data:
            steps.append("Investigate identified issues")
        steps.append("Schedule follow-up review")
        return steps

    def _specify_data_requirements(self, data: Dict[str, Any]) -> List[str]:
        requirements = []
        requirements.append("Complete historical data")
        requirements.append("Real-time metrics")
        requirements.append("Contextual information")
        requirements.append("Comparative benchmarks")
        return requirements

    def _provide_troubleshooting_tips(self, data: Dict[str, Any]) -> List[str]:
        tips = []
        tips.append("Verify data source connectivity")
        tips.append("Check data format compliance")
        tips.append("Validate timestamp accuracy")
        tips.append("Review access permissions")
        return tips

    def _suggest_feature_enablement(self) -> List[str]:
        return [
            "Enable advanced analytics",
            "Activate real-time monitoring",
            "Configure automated alerts",
            "Enable data export functionality"
        ]

    def _provide_configuration_guidance(self) -> List[str]:
        return [
            "Configure data collection parameters",
            "Set up notification preferences",
            "Define custom metrics",
            "Establish baseline thresholds"
        ]

    def _extract_key_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        metrics = {}
        if 'metrics' in data:
            if isinstance(data['metrics'], dict):
                metrics.update(data['metrics'])
            elif isinstance(data['metrics'], list):
                metrics['count'] = len(data['metrics'])
        if 'values' in data:
            metrics['values'] = data['values']
        return metrics if metrics else {'status': 'No metrics available'}

    def _summarize_data_source(self, source_data: Any) -> str:
        if isinstance(source_data, dict):
            return f"Source data with {len(source_data)} fields"
        elif isinstance(source_data, list):
            return f"Source data with {len(source_data)} items"
        return "Source data received"

    def _calculate_overall_risk(self, data: Dict[str, Any]) -> str:
        if 'risk_level' in data:
            return str(data['risk_level']).lower()
        if 'issues' in data and len(data.get('issues', [])) > 5:
            return "high"
        if 'issues' in data and len(data.get('issues', [])) > 2:
            return "medium"
        return "low"

    def _identify_critical_issues(self, data: Dict[str, Any]) -> List[str]:
        issues = []
        if 'critical_issues' in data:
            issues.extend(data['critical_issues'] if isinstance(data['critical_issues'], list) else [data['critical_issues']])
        if 'errors' in data:
            issues.extend(data['errors'] if isinstance(data['errors'], list) else [data['errors']])
        return issues if issues else ["No critical issues identified"]

    def _analyze_risk_factors(self, data: Dict[str, Any]) -> List[str]:
        factors = []
        if 'risk_factors' in data:
            factors.extend(data['risk_factors'] if isinstance(data['risk_factors'], list) else [data['risk_factors']])
        if 'vulnerabilities' in data:
            factors.extend(data['vulnerabilities'] if isinstance(data['vulnerabilities'], list) else [data['vulnerabilities']])
        return factors if factors else ["Standard risk profile"]

    def _get_source_recommendations(self, source: str, source_data: Any) -> List[str]:
        recommendations = []
        recommendations.append(f"Optimize {source} data collection")
        recommendations.append(f"Increase {source} data frequency")
        recommendations.append(f"Validate {source} data quality")
        return recommendations

    def _get_key_insight(self, source_data: Any) -> str:
        if isinstance(source_data, dict) and 'insight' in source_data:
            return source_data['insight']
        return "Key insight: Data analysis in progress"

    def _get_preliminary_findings(self, data: Dict[str, Any]) -> List[str]:
        findings = []
        if 'findings' in data:
            findings.extend(data['findings'] if isinstance(data['findings'], list) else [str(data['findings'])])
        findings.append("Preliminary analysis completed")
        return findings

    def _identify_trends(self, data: Dict[str, Any]) -> List[str]:
        trends = []
        if 'trends' in data:
            trends.extend(data['trends'] if isinstance(data['trends'], list) else [data['trends']])
        if 'patterns' in data:
            trends.append(f"Pattern detected: {data['patterns']}")
        return trends if trends else ["Trend analysis pending"]

    def _highlight_anomalies(self, data: Dict[str, Any]) -> List[str]:
        anomalies = []
        if 'anomalies' in data:
            anomalies.extend(data['anomalies'] if isinstance(data['anomalies'], list) else [data['anomalies']])
        if 'outliers' in data:
            anomalies.append(f"Outliers detected: {data['outliers']}")
        return anomalies if anomalies else ["No anomalies detected"]

    def _identify_correlations(self, data: Dict[str, Any]) -> List[str]:
        correlations = []
        if 'correlations' in data:
            correlations.extend(data['correlations'] if isinstance(data['correlations'], list) else [data['correlations']])
        if len(data) > 2:
            correlations.append("Multiple data relationships identified")
        return correlations if correlations else ["Correlation analysis pending"]

    def _build_timeline(self, data: Dict[str, Any]) -> Dict[str, Any]:
        timeline = {}
        if 'events' in data:
            timeline['events'] = data['events']
        if 'timestamps' in data:
            timeline['timestamps'] = data['timestamps']
        timeline['generated_at'] = datetime.now().isoformat()
        return timeline

    def _assess_impact_scope(self, data: Dict[str, Any]) -> str:
        if 'scope' in data:
            return str(data['scope']).lower()
        if 'affected_items' in data and len(data['affected_items']) > 10:
            return "widespread"
        if 'affected_items' in data and len(data['affected_items']) > 3:
            return "moderate"
        return "limited"

    def _calculate_priority_score(self, data: Dict[str, Any]) -> int:
        score = 5
        if 'priority' in data:
            score = int(data['priority']) if isinstance(data['priority'], (int, float)) else 5
        if 'critical_issues' in data:
            score += len(data['critical_issues']) if isinstance(data['critical_issues'], list) else 1
        return min(score, 10)

    def _identify_incomplete_areas(self, data: Dict[str, Any]) -> List[str]:
        incomplete = []
        if 'missing_fields' in data:
            incomplete.extend(data['missing_fields'] if isinstance(data['missing_fields'], list) else [data['missing_fields']])
        incomplete.append("Data validation in progress")
        return incomplete

    def _assess_confidence_levels(self, data: Dict[str, Any]) -> Dict[str, int]:
        confidence = {}
        if 'confidence' in data:
            confidence.update(data['confidence'] if isinstance(data['confidence'], dict) else {'overall': data['confidence']})
        else:
            confidence['overall'] = 60
        return confidence

    def _suggest_data_gathering_actions(self, data: Dict[str, Any]) -> List[str]:
        actions = []
        actions.append("Collect missing data points")
        actions.append("Validate existing information")
        if 'missing_fields' in data:
            actions.append(f"Obtain {len(data['missing_fields'])} missing fields")
        actions.append("Schedule data review")
        return actions

    def _identify_immediate_actions(self, data: Dict[str, Any]) -> List[str]:
        actions = []
        if 'critical_issues' in data and data['critical_issues']:
            actions.append("Address critical issues immediately")
        actions.append("Escalate to relevant team")
        actions.append("Document findings")
        return actions

    def _suggest_follow_up_investigations(self, data: Dict[str, Any]) -> List[str]:
        investigations = []
        investigations.append("Conduct root cause analysis")
        investigations.append("Review historical data")
        investigations.append("Interview stakeholders")
        investigations.append("Perform comparative analysis")
        return investigations