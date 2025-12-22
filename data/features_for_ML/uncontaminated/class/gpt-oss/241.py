import cairo
from typing import Callable, Tuple, Optional
from dataclasses import dataclass
from enum import Enum, auto


# ----------------------------------------------------------------------
# Helper types
# ----------------------------------------------------------------------
class DrawingMode(Enum):
    NORMAL = auto()
    SHADOW = auto()
    SELECTED = auto()


@dataclass
class QuadBounds:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def contains_point(self, x: float, y: float) -> bool:
        return self.x_min <= x <= self.x_max and self.y_min <= y <= self.y_max

    def translate(self, dx: float, dy: float) -> None:
        self.x_min += dx
        self.x_max += dx
        self.y_min += dy
        self.y_max += dy

    def get_bounds(self) -> "QuadBounds":
        return self


# ----------------------------------------------------------------------
# Main class
# ----------------------------------------------------------------------
class DrawingAction:
    """
    Base class for drawable actions. Subclasses should override `draw` to
    implement specific shapes. The base implementation provides common
    utilities such as bounds handling, point containment, and shadow
    colour calculation.
    """

    def __init__(
        self,
        bounds: QuadBounds,
        color: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0),
        drawing_mode: DrawingMode = DrawingMode.NORMAL,
    ) -> None:
        """
        Parameters
        ----------
        bounds : QuadBounds
            The bounding rectangle of the action in image coordinates.
        color : tuple[float, float, float, float], optional
            RGBA colour of the action. Defaults to black.
        drawing_mode : DrawingMode, optional
            The drawing mode for this action. Defaults to NORMAL.
        """
        self._bounds = bounds
        self._color = color
        self._drawing_mode = drawing_mode

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def draw(
        self,
        cr: cairo.Context,
        image_to_widget_coords: Callable[[int, int], Tuple[float, float]],
        scale: float,
    ) -> None:
        """
        Draw the action onto the given Cairo context.

        The default implementation draws a simple rectangle representing
        the bounds. Subclasses should override this method to provide
        custom drawing logic.

        Parameters
        ----------
        cr : cairo.Context
            The Cairo context to draw on.
        image_to_widget_coords : Callable[[int, int], tuple[float, float]]
            Function that converts image coordinates to widget coordinates.
        scale : float
            Current scale factor applied to the image.
        """
        # Convert bounds to widget coordinates
        x0, y0 = image_to_widget_coords(int(self._bounds.x_min), int(self._bounds.y_min))
        x1, y1 = image_to_widget_coords(int(self._bounds.x_max), int(self._bounds.y_max))

        # Apply scale
        x0 *= scale
        y0 *= scale
        x1 *= scale
        y1 *= scale

        # Set colour
        cr.set_source_rgba(*self._color)

        # Draw rectangle
        cr.rectangle(x0, y0, x1 - x0, y1 - y0)
        cr.stroke()

    def get_bounds(self) -> QuadBounds:
        """
        Return the bounding rectangle of the action.

        Returns
        -------
        QuadBounds
            The bounds in image coordinates.
        """
        return self._bounds

    def contains_point(self, x_img: int, y_img: int) -> bool:
        """
        Test whether the given image coordinate lies inside the action.

        Parameters
        ----------
        x_img : int
            X coordinate in image space.
        y_img : int
            Y coordinate in image space.

        Returns
        -------
        bool
            True if the point is inside the bounds, False otherwise.
        """
        return self._bounds.contains_point(float(x_img), float(y_img))

    def _calculate_shadow_color(self, color: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """
        Calculate a darker shadow colour from the given colour.

        The shadow is produced by reducing the RGB components by 30%
        while keeping the alpha unchanged.

        Parameters
        ----------
        color : tuple[float, float, float, float]
            Original RGBA colour.

        Returns
        -------
        tuple[float, float, float, float]
            Darkened colour suitable for shadows.
        """
        r, g, b, a = color
        factor = 0.7
        return (r * factor, g * factor, b * factor, a)

    def translate(self, dx: int, dy: int) -> None:
        """
        Translate the action by the given offset.

        Parameters
        ----------
        dx : int
            Offset in the X direction (image coordinates).
        dy : int
            Offset in the Y direction (image coordinates).
        """
        self._bounds.translate(float(dx), float(dy))

    def get_drawing_mode(self) -> DrawingMode:
        """
        Return the drawing mode of the action.

        Returns
        -------
        DrawingMode
            The current drawing mode.
        """
        return self._drawing_mode