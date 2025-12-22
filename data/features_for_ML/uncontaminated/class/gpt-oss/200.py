import sys
import traceback
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Callable
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr


@dataclass
class Exercise:
    name: str
    path: Path
    status: str = "pending"          # pending, passed, failed
    output: str = ""
    solution: str = ""
    hint_enabled: bool = False
    original_source: str = field(default="", init=False)

    def __post_init__(self):
        # Cache the original source for reset
        self.original_source = self.path.read_text(encoding="utf-8")


class ExerciseManager:
    """Manages the lifecycle of exercises in Pylings."""

    def __init__(self, exercises_dir: Optional[Path] = None):
        """
        Initialize the manager.

        Parameters
        ----------
        exercises_dir : Optional[Path]
            Directory containing exercise files. If None, defaults to
            a subdirectory named 'exercises' in the current working directory.
        """
        self.exercises_dir = exercises_dir or Path.cwd() / "exercises"
        self.exercises: List[Exercise] = []
        self.current_index: int = 0
        self._initialize_exercises()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _initialize_exercises(self):
        """Scan the exercises directory and populate the exercise list."""
        if not self.exercises_dir.exists():
            raise FileNotFoundError(f"Exercises directory not found: {self.exercises_dir}")

        for file in sorted(self.exercises_dir.glob("*.py")):
            name = file.stem
            solution_file = file.with_suffix(".sol")
            solution = solution_file.read_text(encoding="utf-8") if solution_file.exists() else ""
            exercise = Exercise(name=name, path=file, solution=solution)
            self.exercises.append(exercise)

    def _evaluate_exercises_ordered(self, exercise_paths: List[Path]) -> List[bool]:
        """Run a list of exercises in order and return a list of success flags."""
        results = []
        for path in exercise_paths:
            result = self.run_exercise(path)
            results.append(result)
        return results

    def _store_result(self, path: Path, result: bool, output: str):
        """Store the result and output for the exercise at the given path."""
        exercise = next((e for e in self.exercises if e.path == path), None)
        if exercise:
            exercise.output = output
            exercise.status = "passed" if result else "failed"

    def _update_exercise_status(self, name: str, result: bool):
        """Update the status of the exercise with the given name."""
        exercise = next((e for e in self.exercises if e.name == name), None)
        if exercise:
            exercise.status = "passed" if result else "failed"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run_exercise(self, path: Path, source: str = "workspace") -> bool:
        """
        Execute the exercise at the given path.

        Parameters
        ----------
        path : Path
            Path to the exercise file.
        source : str, optional
            Source of the exercise ('workspace' or 'package'). Currently unused.

        Returns
        -------
        bool
            True if the exercise executed without exception, False otherwise.
        """
        if not path.exists():
            raise FileNotFoundError(f"Exercise file not found: {path}")

        code = path.read_text(encoding="utf-8")
        local_ns = {}
        stdout = StringIO()
        stderr = StringIO()
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, {}, local_ns)
            success = True
        except Exception:
            success = False
            stderr.write(traceback.format_exc())

        output = stdout.getvalue() + stderr.getvalue()
        self._store_result(path, success, output)
        return success

    def _format_output(self, output: str) -> str:
        """Format the output string for display."""
        return output.strip()

    def update_exercise_output(self):
        """Re-run the current exercise and update its output."""
        if not self.exercises:
            return
        exercise = self.exercises[self.current_index]
        self.run_exercise(exercise.path)

    def check_all_exercises(self, progress_callback: Optional[Callable[[int, int], None]] = None):
        """
        Run all exercises sequentially, updating their status.

        Parameters
        ----------
        progress_callback : Callable[[int, int], None], optional
            Called with (completed, total) after each exercise.
        """
        total = len(self.exercises)
        for idx, exercise in enumerate(self.exercises, start=1):
            self.run_exercise(exercise.path)
            if progress_callback:
                progress_callback(idx, total)

    def next_exercise(self):
        """Advance to the next exercise, if any."""
        if self.current_index + 1 < len(self.exercises):
            self.current_index += 1

    def reset_exercise(self):
        """Reset the current exercise to its original source."""
        if not self.exercises:
            return
        exercise = self.exercises[self.current_index]
        exercise.path.write_text(exercise.original_source, encoding="utf-8")
        exercise.status = "pending"
        exercise.output = ""

    def get_solution(self) -> str:
        """Return the solution text for the current exercise."""
        if not self.exercises:
            return ""
        return self.exercises[self.current_index].solution

    def get_exercise_path(self, path: Path, source: str = "workspace") -> Path:
        """
        Resolve the full path to an exercise.

        Parameters
        ----------
        path : Path
            Relative or absolute path to the exercise.
        source : str, optional
            'workspace' or 'package'. For 'package', the path is resolved
            relative to the exercises directory.

        Returns
        -------
        Path
            Absolute path to the exercise file.
        """
        if source == "package":
            return (self.exercises_dir / path).resolve()
        return path.resolve()

    def run_and_print(self, path: Path, source: str = "workspace", type: str = "d"):
        """
        Run an exercise and print its output.

        Parameters
        ----------
        path : Path
            Path to the exercise file.
        source : str, optional
            Source of the exercise.
        type : str, optional
            Output type: 'd' for detailed (stdout+stderr), 's' for stdout only.
        """
        full_path = self.get_exercise_path(path, source)
        success = self.run_exercise(full_path)
        exercise = next((e for e in self.exercises if e.path == full_path), None)
        if exercise:
            output = exercise.output
            if type == "s":
                # Attempt to extract only stdout (everything before first error)
                output = output.split("Traceback")[0]
            print(self._format_output(output))
            print(f"Result: {'PASS' if success else 'FAIL'}")

    def print_root_solution(self, path: Path, source: str = "package"):
        """
        Print the solution for the root exercise (first in the list).

        Parameters
        ----------
        path : Path
            Path to the root exercise file.
        source : str, optional
            Source of the exercise.
        """
        if not self.exercises:
            return
        root = self.exercises[0]
        print(f"Solution for {root.name}:\n{root.solution}")

    def reset_exercise_by_path(self, path: Path):
        """Reset the exercise identified by the given path."""
        full_path = self.get_exercise_path(path)
        exercise = next((e for e in self.exercises if e.path == full_path), None)
        if exercise:
            exercise.path.write_text(exercise.original_source, encoding="utf-8")
            exercise.status = "pending"
            exercise.output = ""

    def toggle_hint(self):
        """Toggle the hint flag for the current exercise."""
        if not self.exercises:
            return
        exercise = self.exercises[self.current_index]
        exercise.hint_enabled = not exercise.hint_enabled