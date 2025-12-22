def async_wrapper(page):

            try:
                self._loop_manager.run_until_complete(self._async_main(page))
                self.attach_on_shutdown_hooks()
            except Exception as e:
                self.logger.error(f'Error when trying to run App: {e}')
            # finally:
            #     if self.on_shutdown:
            #         self._loop_manager.run_until_complete(
            #             self._execute_hooks(self.on_shutdown, "shutdown")
            #         )
                # self._loop_manager.close_loop()