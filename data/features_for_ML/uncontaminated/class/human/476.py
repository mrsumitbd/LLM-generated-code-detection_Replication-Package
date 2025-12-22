import time
import os
import json
from typing import Dict, TypedDict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import re
import re
import re
from agentops.sdk.decorators import agent, trace, operation

class RecruiterAgent:
    """Recruitment agent: generates descriptions for work agents"""
    def __init__(self, agent_id: str, model_name: str = None, num_agents: int = 3):
        self.agent_id = agent_id
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.num_agents = num_agents
        self.system_prompt = (
            "You are the leader of a group of experts who needs to recruit the right team configuration to solve complex problems.\n\n"
            "Your responsibilities:\n"
            "1. Analyze the problem and identify necessary expertise areas\n"
            "2. Generate diverse expert descriptions with complementary specializations\n"
            "3. Ensure each expert has clearly defined roles and responsibilities\n"
            "4. Adapt team composition based on feedback when provided\n\n"
            "Each expert should have specialized knowledge directly relevant to the problem, "
            "and the team should collectively be capable of solving the complete problem."
        )
        # Initialize LLM with structured output
        self.llm = ChatOpenAI(
            model=self.model_name
        )
        
    def _create_prompt(self, problem: str, feedback: str = None) -> str:
        feedback_section = ""
        if feedback:
            feedback_section = f"""
            Previous evaluation feedback:
            {feedback}
            
            Please consider this feedback when forming your new team of experts.
            """
            
        return f"""
            Generate the configuration of {self.num_agents} expert agents based on the following problem:

            Problem:
            {problem}
            
            {feedback_section}

            What experts will you recruit to better solve this problem?

            For each expert, provide:
            1. Agent ID (starting from 1)
            2. Expert name reflecting their expertise area  
            3. Detailed description of their role and responsibilities


            Agent ID: {self.agent_id}
        """

    @operation
    async def describe(self, problem: str, feedback: str = None):
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=self._create_prompt(problem, feedback))
        ]

        start_time = time.time()
        end_time = start_time  # Initialize end_time to prevent undefined errors
        
        try:
            # Use structured output to call LLM
            llm_with_schema = self.llm.with_structured_output(schema=ExpertTeam, include_raw=True)
            response = await llm_with_schema.ainvoke(messages)
            end_time = time.time()  # Update end_time
            
            # Extract content from structured response
            structured_data = response["parsed"]
            raw_response = response["raw"]
            
            # Validate structured data
            if not isinstance(structured_data, dict) or "agents" not in structured_data or not structured_data["agents"]:
                print(f"Warning: Invalid or empty response from recruiter. Raw content: {raw_response.content[:200]}...")
                # Try to extract expert information from raw response
                try:
                    # Try to parse JSON
                    import re
                    # Look for possible JSON objects
                    json_match = re.search(r'(\{.*\})', raw_response.content.replace('\n', ' '), re.DOTALL)
                    if json_match:
                        potential_json = json_match.group(1)
                        parsed_data = json.loads(potential_json)
                        if "agents" in parsed_data and parsed_data["agents"]:
                            structured_data = parsed_data
                        else:
                            # Create default expert team
                            structured_data = {"agents": self._create_default_experts()}
                    else:
                        structured_data = {"agents": self._create_default_experts()}
                except Exception as parse_err:
                    print(f"Error parsing recruiter response: {str(parse_err)}")
                    structured_data = {"agents": self._create_default_experts()}
            
            
            # Set name
            raw_response.name = f"recruiter_{self.agent_id}"
            
            return {
                "agent_id": self.agent_id,
                "solution": structured_data,
                "message": raw_response,  # Save original message to preserve usage_metadata
                "latency_ms": (end_time - start_time) * 1000,
            }
            
        except Exception as e:
            # If structured output fails, fall back to standard mode
            print(f"Structured output failed for recruiter: {str(e)}. Falling back to standard output.")
            
            # Re-invoke model without structured output
            response = await self.llm.ainvoke(messages)
            end_time = time.time()
            
            # Set name
            response.name = f"recruiter_{self.agent_id}"
            
            # Try to extract JSON from response content
            try:
                # Try to parse directly as JSON
                content_text = response.content
                try:
                    content_json = json.loads(content_text)
                    if "agents" in content_json and content_json["agents"]:
                        structured_data = content_json
                    else:
                        structured_data = {"agents": self._create_default_experts()}
                except json.JSONDecodeError:
                    # Try to find JSON part in text
                    import re
                    json_match = re.search(r'(\{.*\})', content_text.replace('\n', ' '), re.DOTALL)
                    if json_match:
                        potential_json = json_match.group(1)
                        try:
                            parsed_json = json.loads(potential_json)
                            if "agents" in parsed_json and parsed_json["agents"]:
                                structured_data = parsed_json
                            else:
                                structured_data = {"agents": self._create_default_experts()}
                        except Exception as e:
                            print(f"[WARNING] Error parsing recruiter content: {str(e)}")
                            structured_data = {"agents": self._create_default_experts()}
                    else:
                        # If no valid JSON found, create default experts
                        structured_data = {"agents": self._create_default_experts()}
            except Exception as parse_error:
                print(f"[WARNING] Error parsing recruiter content: {str(parse_error)}")
                structured_data = {"agents": self._create_default_experts()}
            
            return {
                "agent_id": self.agent_id,
                "solution": structured_data,
                "message": response,
                "latency_ms": (end_time - start_time) * 1000,
            }
    
    def _create_default_experts(self) -> List[Dict[str, Any]]:
        """Create default expert team when structured output fails"""
        default_experts = []
        expert_types = [
            {"name": "Mathematics Expert", "describe": "Expert specialized in mathematical problems, calculations and proofs."},
            {"name": "Problem Analysis Expert", "describe": "Expert responsible for analyzing problem structure and breaking down complex problems."},
            {"name": "Solution Expert", "describe": "Expert who integrates analysis results and provides complete solutions."}
        ]
        
        # Create experts based on configured number
        for i in range(1, min(self.num_agents + 1, len(expert_types) + 1)):
            expert = expert_types[i-1].copy()
            expert["agent_id"] = i
            default_experts.append(expert)
        
        return default_experts