def _parser(resp: SyncPageT) -> SyncPageT:
            resp._set_private_attributes(
                client=self,
                model=model,
                options=options,
            )
            return resp