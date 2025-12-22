def decorator(kernel_fn):
            if op_name not in self._registry:
                self._registry[op_name] = {}
            # Ensure that operators of the same backend are not registered repeatedly
            if backend in self._registry[op_name]:
                raise RuntimeError(f"Kernel {op_name} already registered for backend {backend}")
            self._registry[op_name][backend] = kernel_fn