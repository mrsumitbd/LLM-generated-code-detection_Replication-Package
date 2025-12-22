import anthropic
import json
import time
from datetime import datetime
from typing import Optional


class SchedulerService:
    """Service for managing scheduled tasks and automatic execution"""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.scheduled_tasks = {}
        self.task_counter = 0

    def schedule_task(
        self,
        task_description: str,
        schedule_time: Optional[str] = None,
        recurring: bool = False,
        recurring_interval: Optional[str] = None,
    ) -> dict:
        """Schedule a new task using Claude to understand and plan execution"""
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"

        # Use Claude to understand the task and create an execution plan
        prompt = f"""You are a task scheduler assistant. Analyze the following task and create an execution plan.

Task: {task_description}
Scheduled Time: {schedule_time or 'ASAP'}
Recurring: {recurring}
Recurring Interval: {recurring_interval or 'N/A'}

Please provide:
1. A clear understanding of what needs to be done
2. Steps to execute the task
3. Estimated duration
4. Any dependencies or prerequisites
5. Success criteria

Format your response as JSON with keys: understanding, steps, estimated_duration, dependencies, success_criteria"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Parse the response
        try:
            # Try to extract JSON from the response
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                execution_plan = json.loads(json_str)
            else:
                execution_plan = {
                    "understanding": response_text,
                    "steps": ["Execute task"],
                    "estimated_duration": "Unknown",
                    "dependencies": [],
                    "success_criteria": ["Task completed"],
                }
        except json.JSONDecodeError:
            execution_plan = {
                "understanding": response_text,
                "steps": ["Execute task"],
                "estimated_duration": "Unknown",
                "dependencies": [],
                "success_criteria": ["Task completed"],
            }

        # Store the scheduled task
        self.scheduled_tasks[task_id] = {
            "id": task_id,
            "description": task_description,
            "scheduled_time": schedule_time,
            "recurring": recurring,
            "recurring_interval": recurring_interval,
            "execution_plan": execution_plan,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
            "executions": [],
        }

        return {
            "task_id": task_id,
            "status": "scheduled",
            "execution_plan": execution_plan,
        }

    def execute_task(self, task_id: str) -> dict:
        """Execute a scheduled task"""
        if task_id not in self.scheduled_tasks:
            return {"error": f"Task {task_id} not found"}

        task = self.scheduled_tasks[task_id]

        # Use Claude to execute the task based on the plan
        prompt = f"""You are a task execution assistant. Execute the following task based on the plan provided.

Task Description: {task['description']}
Execution Plan: {json.dumps(task['execution_plan'], indent=2)}

Please:
1. Execute each step in the plan
2. Document the results
3. Verify success criteria
4. Report any issues encountered

Format your response as JSON with keys: execution_results, steps_completed, issues, success"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Parse the response
        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                execution_result = json.loads(json_str)
            else:
                execution_result = {
                    "execution_results": response_text,
                    "steps_completed": len(task["execution_plan"].get("steps", [])),
                    "issues": [],
                    "success": True,
                }
        except json.JSONDecodeError:
            execution_result = {
                "execution_results": response_text,
                "steps_completed": len(task["execution_plan"].get("steps", [])),
                "issues": [],
                "success": True,
            }

        # Record the execution
        execution_record = {
            "executed_at": datetime.now().isoformat(),
            "result": execution_result,
            "status": "completed" if execution_result.get("success", True) else "failed",
        }

        task["executions"].append(execution_record)
        task["status"] = "completed"

        return {
            "task_id": task_id,
            "execution_result": execution_result,
            "status": execution_record["status"],
        }

    def get_task_status(self, task_id: str) -> dict:
        """Get the status of a scheduled task"""
        if task_id not in self.scheduled_tasks:
            return {"error": f"Task {task_id} not found"}

        task = self.scheduled_tasks[task_id]
        return {
            "task_id": task_id,
            "description": task["description"],
            "status": task["status"],
            "created_at": task["created_at"],
            "executions_count": len(task["executions"]),
            "last_execution": (
                task["executions"][-1]["executed_at"]
                if task["executions"]
                else None
            ),
        }

    def list_tasks(self) -> dict:
        """List all scheduled tasks"""
        tasks_summary = []
        for task_id, task in self.scheduled_tasks.items():
            tasks_summary.append(
                {
                    "task_id": task_id,
                    "description": task["description"],
                    "status": task["status"],
                    "recurring": task["recurring"],
                    "created_at": task["created_at"],
                }
            )

        return {"tasks": tasks_summary, "total_tasks": len(tasks_summary)}

    def cancel_task(self, task_id: str) -> dict:
        """Cancel a scheduled task"""
        if task_id not in self.scheduled_tasks:
            return {"error": f"Task {task_id} not found"}

        self.scheduled_tasks[task_id]["status"] = "cancelled"
        return {"task_id": task_id, "status": "cancelled"}

    def get_task_details(self, task_id: str) -> dict:
        """Get detailed information about a task"""
        if task_id not in self.scheduled_tasks:
            return {"error": f"Task {task_id} not found"}

        task = self.scheduled_tasks[task_id]
        return {
            "task_id": task_id,
            "description": task["description"],
            "scheduled_time": task["scheduled_time"],
            "recurring": task["recurring"],
            "recurring_interval": task["recurring_interval"],
            "status": task["status"],
            "execution_plan": task["execution_plan"],
            "executions": task["executions"],
            "created_at": task["created_at"],
        }

    def analyze_task_performance(self, task_id: str) -> dict:
        """Analyze the performance of a task using Claude"""
        if task_id not in self.scheduled_tasks:
            return {"error": f"Task {task_id} not found"}

        task = self.scheduled_tasks[task_id]

        if not task["executions"]:
            return {"analysis": "No executions recorded yet"}

        # Use Claude to analyze task performance
        prompt = f"""Analyze the performance of the following task based on its execution history.

Task Description: {task['description']}
Execution Plan: {json.dumps(task['execution_plan'], indent=2)}
Execution History: {json.dumps(task['executions'], indent=2)}

Please provide:
1. Overall performance assessment
2. Success rate
3. Average execution time
4. Common issues or patterns
5. Recommendations for improvement

Format your response as JSON with keys: assessment, success_rate, avg_execution_time, patterns, recommendations"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text

        # Parse the response
        try:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                analysis = json.loads(json_str)
            else:
                analysis = {"assessment": response_text}
        except json.JSONDecodeError:
            analysis = {"assessment": response_text}

        return {"task_id": task_id, "analysis": analysis}


def main():
    """Main function to demonstrate the SchedulerService"""
    service = SchedulerService()

    # Schedule a task
    print("Scheduling a task...")
    result = service.schedule_task(
        task_description="Generate a weekly report on project progress",
        schedule_time="2024-01-15 09:00 AM",
        recurring=True,
        recurring_interval="weekly",
    )
    print(f"Task scheduled: {result['task_id']}")
    print(f"Execution plan: {result['execution_plan']}\n")

    task_id = result["task_id"]

    # Get task status
    print("Getting task status...")
    status = service.get_task_status(task_id)
    print(f"Task status: {status}\n")

    # Execute the task
    print("Executing task...")
    execution = service.execute_task(task_id)
    print(f"Execution result: {execution}\n")

    # Get task details
    print("Getting task details...")
    details = service.get_task_details(task_id)
    print(f"Task details: {details}\n")

    # List all tasks
    print("Listing all tasks...")
    tasks = service.list_tasks()
    print(f"Total tasks: {tasks['total_tasks']}")
    for task in tasks["tasks"]:
        print(f"  - {task['task_id']}: {task['description']} ({task['status']})")

    # Analyze task performance
    print("\nAnalyzing task performance...")
    analysis = service.analyze_task_performance(task_id)
    print(f"Performance analysis: {analysis}")


if __name__ == "__main__":
    main()