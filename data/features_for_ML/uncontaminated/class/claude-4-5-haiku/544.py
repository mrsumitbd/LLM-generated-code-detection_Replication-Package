import anthropic
import json


class ComplianceRequirement:
    """Individual compliance requirement."""

    def __init__(self, requirement_id: str, title: str, description: str, category: str, severity: str):
        """Initialize a compliance requirement.
        
        Args:
            requirement_id: Unique identifier for the requirement
            title: Short title of the requirement
            description: Detailed description of the requirement
            category: Category of compliance (e.g., "Data Protection", "Security")
            severity: Severity level (e.g., "Critical", "High", "Medium", "Low")
        """
        self.requirement_id = requirement_id
        self.title = title
        self.description = description
        self.category = category
        self.severity = severity
        self.implementation_status = "Not Started"
        self.evidence = []
        self.notes = ""

    def to_dict(self) -> dict:
        """Convert requirement to dictionary representation."""
        return {
            "requirement_id": self.requirement_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "severity": self.severity,
            "implementation_status": self.implementation_status,
            "evidence": self.evidence,
            "notes": self.notes
        }

    def update_status(self, status: str) -> None:
        """Update the implementation status of the requirement.
        
        Args:
            status: New status (e.g., "Not Started", "In Progress", "Completed")
        """
        self.implementation_status = status

    def add_evidence(self, evidence: str) -> None:
        """Add evidence of compliance.
        
        Args:
            evidence: Description of evidence supporting compliance
        """
        self.evidence.append(evidence)

    def add_note(self, note: str) -> None:
        """Add a note about the requirement.
        
        Args:
            note: Note to add
        """
        self.notes = note

    def get_ai_recommendations(self) -> str:
        """Get AI-powered recommendations for implementing this requirement using Claude.
        
        Returns:
            AI-generated recommendations for implementing the requirement
        """
        client = anthropic.Anthropic()
        
        prompt = f"""You are a compliance expert. Provide specific, actionable recommendations for implementing the following compliance requirement:

Requirement ID: {self.requirement_id}
Title: {self.title}
Description: {self.description}
Category: {self.category}
Severity: {self.severity}
Current Status: {self.implementation_status}

Please provide:
1. Key steps to implement this requirement
2. Common pitfalls to avoid
3. Best practices for maintaining compliance
4. Estimated timeline for implementation
5. Resources or tools that might help

Keep the response concise and practical."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

    def get_compliance_assessment(self) -> str:
        """Get an AI assessment of the current compliance status using Claude.
        
        Returns:
            AI-generated assessment of compliance status
        """
        client = anthropic.Anthropic()
        
        evidence_text = "\n".join(self.evidence) if self.evidence else "No evidence provided"
        
        prompt = f"""You are a compliance auditor. Assess the compliance status of the following requirement:

Requirement ID: {self.requirement_id}
Title: {self.title}
Description: {self.description}
Category: {self.category}
Severity: {self.severity}
Implementation Status: {self.implementation_status}
Evidence Provided:
{evidence_text}
Notes: {self.notes if self.notes else "No notes"}

Please provide:
1. Current compliance level (0-100%)
2. Gap analysis - what's missing
3. Risk assessment if not fully compliant
4. Recommended next steps
5. Timeline for full compliance

Be objective and specific in your assessment."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text


def main():
    """Demonstrate the ComplianceRequirement class."""
    # Create a sample compliance requirement
    req = ComplianceRequirement(
        requirement_id="SEC-001",
        title="Data Encryption at Rest",
        description="All sensitive data must be encrypted using AES-256 or equivalent when stored",
        category="Security",
        severity="Critical"
    )
    
    # Update status and add evidence
    req.update_status("In Progress")
    req.add_evidence("Implemented AES-256 encryption for database")
    req.add_evidence("Encryption keys stored in secure vault")
    req.add_note("Waiting for security audit approval")
    
    # Display requirement details
    print("Compliance Requirement Details:")
    print(json.dumps(req.to_dict(), indent=2))
    print("\n" + "="*50 + "\n")
    
    # Get AI recommendations
    print("AI Recommendations for Implementation:")
    print("-" * 50)
    recommendations = req.get_ai_recommendations()
    print(recommendations)
    print("\n" + "="*50 + "\n")
    
    # Get compliance assessment
    print("Compliance Assessment:")
    print("-" * 50)
    assessment = req.get_compliance_assessment()
    print(assessment)


if __name__ == "__main__":
    main()