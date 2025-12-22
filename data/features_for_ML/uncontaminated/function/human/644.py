import torch

def full_load_to_vram(self) -> int:
        """Load all weights into VRAM (if supported by the model).
        Returns:
            The number of bytes loaded into VRAM.
        """
        if self._is_in_vram:
            # Already in VRAM.
            return 0

        if not hasattr(self._model, "to"):
            # Model doesn't support moving to a device.
            return 0

        if self._cpu_state_dict is not None:
            new_state_dict: dict[str, torch.Tensor] = {}
            for k, v in self._cpu_state_dict.items():
                new_state_dict[k] = v.to(self._compute_device, copy=True)
            self._model.load_state_dict(new_state_dict, assign=True)
        self._model.to(self._compute_device)

        self._is_in_vram = True
        return self._total_bytes