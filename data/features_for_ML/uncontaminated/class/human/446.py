from typing import Dict, Any, Optional, List
import logging

class AdaptiveResponseFormatter:
    """Format responses based on available data and context quality."""
    
    def __init__(self):
        """Initialize the adaptive response formatter."""
        self.logger = logging.getLogger(__name__)
        
        # Define formatting strategies by quality level
        self.quality_formatters = {
            'excellent': self._comprehensive_format,
            'good': self._comprehensive_format,
            'fair': self._partial_format_with_gaps,
            'poor': self._minimal_format_with_guidance,
            'critical': self._minimal_format_with_guidance
        }
    
    def format_response(self, data: Any, quality_assessment: Dict[str, Any]) -> Any:
        """
        Format response based on data quality assessment.
        
        Args:
            data: Original response data
            quality_assessment: Quality assessment from DataAvailabilityDetector
            
        Returns:
            Formatted response with adaptive structure
        """
        if not quality_assessment:
            return self._minimal_format_with_guidance(data)
        
        quality_level = quality_assessment.get('quality_level', 'critical')
        completeness = quality_assessment.get('completeness', 0)
        confidence = quality_assessment.get('confidence', 0)
        
        # Select appropriate formatter
        formatter = self.quality_formatters.get(quality_level, self._minimal_format_with_guidance)
        
        # Format the response
        formatted_data = formatter(data)
        
        # Enhance with quality metadata
        enhanced_response = self._add_quality_indicators(
            formatted_data, quality_assessment
        )
        
        return enhanced_response
    
    def _comprehensive_format(self, data: Any) -> Any:
        """Format response for high-quality data (>75% completeness)."""
        if not isinstance(data, dict):
            return data
        
        # For high-quality data, provide rich formatting with detailed analysis
        formatted = {
            'analysis': {
                'summary': self._generate_executive_summary(data),
                'detailed_findings': self._extract_detailed_findings(data),
                'risk_assessment': self._perform_risk_assessment(data),
                'recommendations': self._generate_actionable_recommendations(data)
            },
            'data_insights': {
                'trends': self._identify_trends(data),
                'anomalies': self._highlight_anomalies(data),
                'correlations': self._identify_correlations(data)
            },
            'context': {
                'timeline': self._build_timeline(data),
                'scope': self._assess_impact_scope(data),
                'priority': self._calculate_priority_score(data)
            },
            'raw_data': data
        }
        
        return formatted
    
    def _partial_format_with_gaps(self, data: Any) -> Any:
        """Format response for partial data (50-75% completeness) with identified gaps."""
        if not isinstance(data, dict):
            return data
        
        # For partial data, provide focused analysis with gap acknowledgment
        formatted = {
            'available_analysis': {
                'summary': self._generate_partial_summary(data),
                'key_findings': self._extract_key_findings(data),
                'preliminary_assessment': self._perform_preliminary_assessment(data)
            },
            'data_limitations': {
                'incomplete_areas': self._identify_incomplete_areas(data),
                'confidence_levels': self._assess_confidence_levels(data),
                'recommended_actions': self._suggest_data_gathering_actions(data)
            },
            'progressive_disclosure': {
                'immediate_actions': self._identify_immediate_actions(data),
                'follow_up_investigations': self._suggest_follow_up_investigations(data)
            },
            'available_data': data
        }
        
        return formatted
    
    def _minimal_format_with_guidance(self, data: Any) -> Any:
        """Format response for minimal data (<50% completeness) with guidance."""
        if not isinstance(data, dict):
            return {
                'limited_data': data,
                'guidance': {
                    'message': 'Limited data available for comprehensive analysis',
                    'recommendations': [
                        'Enable additional data collection',
                        'Check system connectivity',
                        'Verify agent status and configuration'
                    ]
                }
            }
        
        # For minimal data, provide basic information with clear guidance
        formatted = {
            'basic_information': {
                'available_data': self._extract_basic_info(data),
                'initial_observations': self._make_initial_observations(data)
            },
            'guidance': {
                'data_quality_notice': 'Analysis limited due to insufficient data',
                'next_steps': self._suggest_next_steps(data),
                'data_requirements': self._specify_data_requirements(data),
                'troubleshooting': self._provide_troubleshooting_tips(data)
            },
            'progressive_enhancement': {
                'enable_features': self._suggest_feature_enablement(),
                'configuration_tips': self._provide_configuration_guidance()
            },
            'raw_data': data
        }
        
        return formatted
    
    def _add_quality_indicators(self, formatted_data: Any, quality_assessment: Dict[str, Any]) -> Any:
        """Add quality indicators to the formatted response."""
        if not isinstance(formatted_data, dict):
            return formatted_data
        
        # Add quality metadata
        formatted_data['_quality_indicators'] = {
            'completeness_score': quality_assessment.get('completeness', 0),
            'confidence_score': quality_assessment.get('confidence', 0),
            'quality_level': quality_assessment.get('quality_level', 'unknown'),
            'data_freshness': quality_assessment.get('freshness', 'unknown'),
            'data_gaps': quality_assessment.get('gaps', []),
            'recommendations': quality_assessment.get('recommendations', []),
            'assessment_timestamp': quality_assessment.get('assessment_timestamp', ''),
            'data_sources': quality_assessment.get('data_sources_available', [])
        }
        
        return formatted_data
    
    # Helper methods for comprehensive formatting
    def _generate_executive_summary(self, data: Dict[str, Any]) -> str:
        """Generate executive summary for high-quality data."""
        key_metrics = self._extract_key_metrics(data)
        return f"Analysis based on {len(data)} data sources with comprehensive coverage."
    
    def _extract_detailed_findings(self, data: Dict[str, Any]) -> List[str]:
        """Extract detailed findings from high-quality data."""
        findings = []
        for key, value in data.items():
            if isinstance(value, dict) and value.get('data'):
                findings.append(f"{key}: {self._summarize_data_source(value['data'])}")
        return findings
    
    def _perform_risk_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform risk assessment on high-quality data."""
        return {
            'overall_risk': self._calculate_overall_risk(data),
            'critical_issues': self._identify_critical_issues(data),
            'risk_factors': self._analyze_risk_factors(data)
        }
    
    def _generate_actionable_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        for source, source_data in data.items():
            if isinstance(source_data, dict) and source_data.get('data'):
                recommendations.extend(self._get_source_recommendations(source, source_data['data']))
        return recommendations[:10]  # Limit to top 10
    
    # Helper methods for partial formatting
    def _generate_partial_summary(self, data: Dict[str, Any]) -> str:
        """Generate summary for partial data."""
        available_sources = len(data)
        return f"Partial analysis based on {available_sources} available data sources."
    
    def _extract_key_findings(self, data: Dict[str, Any]) -> List[str]:
        """Extract key findings from partial data."""
        findings = []
        for key, value in data.items():
            if isinstance(value, dict) and value.get('data'):
                findings.append(f"{key}: {self._get_key_insight(value['data'])}")
        return findings
    
    def _perform_preliminary_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform preliminary assessment on partial data."""
        return {
            'preliminary_findings': self._get_preliminary_findings(data),
            'confidence_note': 'Assessment based on partial data - additional verification recommended'
        }
    
    # Helper methods for minimal formatting
    def _extract_basic_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic information from minimal data."""
        basic_info = {}
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                basic_info[key] = value
            elif isinstance(value, dict) and 'data' in value:
                basic_info[key] = f"Data available ({type(value['data']).__name__})"
        return basic_info
    
    def _make_initial_observations(self, data: Dict[str, Any]) -> List[str]:
        """Make initial observations from minimal data."""
        observations = []
        if data:
            observations.append(f"Found {len(data)} data sources")
            for key in data.keys():
                observations.append(f"{key} data is available")
        return observations
    
    def _suggest_next_steps(self, data: Dict[str, Any]) -> List[str]:
        """Suggest next steps for minimal data scenarios."""
        return [
            'Enable comprehensive data collection',
            'Check agent connectivity and health',
            'Verify system configuration',
            'Consider expanding time range for analysis'
        ]
    
    def _specify_data_requirements(self, data: Dict[str, Any]) -> List[str]:
        """Specify what data would improve analysis."""
        return [
            'Recent alert data for security analysis',
            'Agent health metrics for system assessment',
            'Vulnerability scan results for risk evaluation',
            'Process and network data for threat detection'
        ]
    
    def _provide_troubleshooting_tips(self, data: Dict[str, Any]) -> List[str]:
        """Provide troubleshooting tips."""
        return [
            'Verify Wazuh agent connectivity',
            'Check log collection configuration',
            'Ensure API permissions are correct',
            'Review time synchronization across systems'
        ]
    
    def _suggest_feature_enablement(self) -> List[str]:
        """Suggest features to enable for better analysis."""
        return [
            'Enable context aggregation: ENABLE_CONTEXT_AGGREGATION=true',
            'Enable adaptive responses: ENABLE_ADAPTIVE_RESPONSES=true',
            'Increase context cache TTL for better performance'
        ]
    
    def _provide_configuration_guidance(self) -> List[str]:
        """Provide configuration guidance."""
        return [
            'Configure comprehensive log collection',
            'Enable vulnerability scanning',
            'Set up proper alert rules',
            'Configure agent monitoring intervals'
        ]
    
    # Utility methods (simplified implementations)
    def _extract_key_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {'sources': len(data), 'quality': 'high'}
    
    def _summarize_data_source(self, source_data: Any) -> str:
        if isinstance(source_data, dict):
            return f"Dictionary with {len(source_data)} items"
        elif isinstance(source_data, list):
            return f"List with {len(source_data)} items"
        return str(type(source_data).__name__)
    
    def _calculate_overall_risk(self, data: Dict[str, Any]) -> str:
        # Simplified risk calculation
        if 'alerts' in data:
            return 'medium'
        return 'low'
    
    def _identify_critical_issues(self, data: Dict[str, Any]) -> List[str]:
        issues = []
        if 'alerts' in data:
            issues.append('Security alerts detected')
        return issues
    
    def _analyze_risk_factors(self, data: Dict[str, Any]) -> List[str]:
        factors = []
        for source in data.keys():
            factors.append(f"{source} analysis pending")
        return factors
    
    def _get_source_recommendations(self, source: str, source_data: Any) -> List[str]:
        return [f"Review {source} data for anomalies"]
    
    def _get_key_insight(self, source_data: Any) -> str:
        return f"Data available for analysis ({type(source_data).__name__})"
    
    def _get_preliminary_findings(self, data: Dict[str, Any]) -> List[str]:
        return [f"Found data from {len(data)} sources"]
    
    def _identify_trends(self, data: Dict[str, Any]) -> List[str]:
        return ["Trend analysis available with comprehensive data"]
    
    def _highlight_anomalies(self, data: Dict[str, Any]) -> List[str]:
        return ["Anomaly detection available with comprehensive data"]
    
    def _identify_correlations(self, data: Dict[str, Any]) -> List[str]:
        return ["Correlation analysis available with comprehensive data"]
    
    def _build_timeline(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"timeline": "Available with timestamp data"}
    
    def _assess_impact_scope(self, data: Dict[str, Any]) -> str:
        return "Comprehensive scope assessment available"
    
    def _calculate_priority_score(self, data: Dict[str, Any]) -> int:
        return 5  # Default medium priority
    
    def _identify_incomplete_areas(self, data: Dict[str, Any]) -> List[str]:
        return ["Some data sources unavailable"]
    
    def _assess_confidence_levels(self, data: Dict[str, Any]) -> Dict[str, int]:
        return {"overall": 75}
    
    def _suggest_data_gathering_actions(self, data: Dict[str, Any]) -> List[str]:
        return ["Enable additional monitoring"]
    
    def _identify_immediate_actions(self, data: Dict[str, Any]) -> List[str]:
        return ["Review available data"]
    
    def _suggest_follow_up_investigations(self, data: Dict[str, Any]) -> List[str]:
        return ["Gather additional context"]