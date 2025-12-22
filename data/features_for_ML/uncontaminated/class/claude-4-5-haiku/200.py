from pathlib import Path
from typing import Optional, Callable, Dict, Any
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum


class ExerciseStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class ExerciseMetadata:
    name: str
    path: Path
    status: ExerciseStatus = ExerciseStatus.PENDING
    output: str = ""
    hint_visible: bool = False


class ExerciseManager:
    """Manages the lifecycle of exercises in Pylings.

    Responsibilities include:
    - Initializing exercise metadata and tracking state.
    - Executing exercises and retrieving output.
    - Resetting exercises to their original form.
    - Moving to the next exercise.
    - Checking completion status and tracking progress.
    - Providing access to matching solutions.
    """

    def __init__(self):
        self.exercises: Dict[str, ExerciseMetadata] = {}
        self.current_exercise_index: int = 0
        self.workspace_root: Path = Path.cwd()
        self.package_root: Path = Path(__file__).parent
        self._initialize_exercises()

    def _initialize_exercises(self):
        """Initialize exercise metadata from the exercises directory."""
        exercises_dir = self.package_root / "exercises"
        if not exercises_dir.exists():
            return

        exercise_files = sorted(exercises_dir.glob("*.py"))
        for idx, exercise_file in enumerate(exercise_files):
            name = exercise_file.stem
            self.exercises[name] = ExerciseMetadata(
                name=name,
                path=exercise_file,
                status=ExerciseStatus.PENDING
            )

    def _evaluate_exercises_ordered(self, exercise_paths: list) -> list:
        """Evaluate exercises in the given order."""
        results = []
        for path in exercise_paths:
            result = self.run_exercise(path, source="workspace")
            results.append(result)
        return results

    def _store_result(self, path: Path, result: str):
        """Store the result of an exercise execution."""
        exercise_name = path.stem
        if exercise_name in self.exercises:
            self.exercises[exercise_name].output = result

    def _update_exercise_status(self, name: str, result: str):
        """Update the status of an exercise based on execution result."""
        if name in self.exercises:
            if "passed" in result.lower() or "success" in result.lower():
                self.exercises[name].status = ExerciseStatus.PASSED
            else:
                self.exercises[name].status = ExerciseStatus.FAILED

    def run_exercise(self, path: Path, source: str = "workspace") -> str:
        """Execute an exercise and return the output."""
        exercise_path = self.get_exercise_path(path, source)
        
        if not exercise_path.exists():
            return f"Error: Exercise file not found at {exercise_path}"

        try:
            result = subprocess.run(
                [sys.executable, str(exercise_path)],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout + result.stderr
            formatted_output = self._format_output(output)
            self._store_result(exercise_path, formatted_output)
            self._update_exercise_status(exercise_path.stem, formatted_output)
            return formatted_output
        except subprocess.TimeoutExpired:
            return "Error: Exercise execution timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def _format_output(self, output: str) -> str:
        """Format the output from exercise execution."""
        return output.strip()

    def update_exercise_output(self):
        """Update output for the current exercise."""
        if self.current_exercise_index < len(self.exercises):
            exercise_names = list(self.exercises.keys())
            current_name = exercise_names[self.current_exercise_index]
            current_exercise = self.exercises[current_name]
            self.run_exercise(current_exercise.path, source="workspace")

    def check_all_exercises(self, progress_callback: Optional[Callable] = None) -> Dict[str, ExerciseStatus]:
        """Check all exercises and return their statuses."""
        exercise_paths = [ex.path for ex in self.exercises.values()]
        self._evaluate_exercises_ordered(exercise_paths)
        
        if progress_callback:
            progress_callback(len(self.exercises), len(self.exercises))
        
        return {name: ex.status for name, ex in self.exercises.items()}

    def next_exercise(self) -> Optional[ExerciseMetadata]:
        """Move to the next exercise."""
        exercise_names = list(self.exercises.keys())
        if self.current_exercise_index < len(exercise_names) - 1:
            self.current_exercise_index += 1
            return self.exercises[exercise_names[self.current_exercise_index]]
        return None

    def reset_exercise(self):
        """Reset the current exercise to its original form."""
        exercise_names = list(self.exercises.keys())
        if self.current_exercise_index < len(exercise_names):
            current_name = exercise_names[self.current_exercise_index]
            self.reset_exercise_by_path(self.exercises[current_name].path)

    def get_solution(self) -> Optional[str]:
        """Get the solution for the current exercise."""
        exercise_names = list(self.exercises.keys())
        if self.current_exercise_index < len(exercise_names):
            current_name = exercise_names[self.current_exercise_index]
            solution_path = self.package_root / "solutions" / f"{current_name}.py"
            if solution_path.exists():
                return solution_path.read_text()
        return None

    def get_exercise_path(self, path: Path, source: str = "workspace") -> Path:
        """Get the full path to an exercise based on source."""
        if source == "workspace":
            return self.workspace_root / path
        elif source == "package":
            return self.package_root / path
        return path

    def run_and_print(self, path: Path, source: str = "workspace", type: str = "d"):
        """Run an exercise and print its output."""
        output = self.run_exercise(path, source)
        print(output)

    def print_root_solution(self, path: Path, source: str = "package"):
        """Print the solution for an exercise."""
        solution_path = self.get_exercise_path(path, source)
        if solution_path.exists():
            print(solution_path.read_text())
        else:
            print(f"Solution not found at {solution_path}")

    def reset_exercise_by_path(self, path: Path):
        """Reset a specific exercise by its path."""
        exercise_name = path.stem
        if exercise_name in self.exercises:
            self.exercises[exercise_name].status = ExerciseStatus.PENDING
            self.exercises[exercise_name].output = ""

    def toggle_hint(self):
        """Toggle hint visibility for the current exercise."""
        exercise_names = list(self.exercises.keys())
        if self.current_exercise_index < len(exercise_names):
            current_name = exercise_names[self.current_exercise_index]
            self.exercises[current_name].hint_visible = not self.exercises[current_name].hint_visible