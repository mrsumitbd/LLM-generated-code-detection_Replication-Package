class LiteAvatarWorkerManager:
    def __init__(self, concurrent_limit: int, handler_root: str, config: Tts2FaceConfigModel):
        self.concurrent_limit = concurrent_limit
        self.handler_root = handler_root
        self.config = config
        self.workers = []
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False

    def start_worker(self):
        with self.lock:
            if self.running:
                return
            self.running = True
            
        for i in range(self.concurrent_limit):
            worker = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name=f"LiteAvatarWorker-{i}"
            )
            worker.start()
            self.workers.append(worker)

    def _worker_loop(self):
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task is None:
                    break
                self._execute_task(task)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Worker error: {e}")

    def _execute_task(self, task):
        try:
            handler_name = task.get('handler')
            handler_path = os.path.join(self.handler_root, handler_name)
            
            if os.path.exists(handler_path):
                spec = importlib.util.spec_from_file_location(handler_name, handler_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'handle'):
                    module.handle(task, self.config)
        except Exception as e:
            logger.error(f"Task execution error: {e}")

    def submit_task(self, task: dict):
        if self.running:
            self.task_queue.put(task)

    def destroy(self):
        with self.lock:
            self.running = False
        
        for _ in range(self.concurrent_limit):
            self.task_queue.put(None)
        
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()