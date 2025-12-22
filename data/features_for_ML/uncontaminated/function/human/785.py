def model_matrix(self):
        """
        Returns:
            (torch.Tensor): a 4x4 model matrix which encodes the complete transform of the object from local
            coordinates to world coordinates.
        """
        # Transformations applied in order of
        # Translation @ Rotation @ Scale
        scale_mat = self._scale_mat(self._scale)
        rotation_rads = self._rotation.div(180.0).mul(PI)
        rotation_mat = self._rotation_mat(*rotation_rads)
        translation_mat = self._translation_mat(self._translation)
        model_mat = translation_mat @ rotation_mat @ scale_mat @ self._permutation
        return model_mat