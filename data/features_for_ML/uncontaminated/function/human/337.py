from decimal import Decimal

def get_weight(self) -> float:
        """Get current weight reading (读数)
        
        Returns:
            float: Weight value
        """
        try:
            self._ensure_connected()
            self._status = "Reading"
            
            self.logger.info("Getting weight...")
            reply = self.weighing_svc.GetWeight(self.session_id)
            
            if reply.Outcome != Outcome.SUCCESS.value:
                error_msg = getattr(reply, 'ErrorMessage', 'Unknown error')
                self.logger.error(f"GetWeight failed: {error_msg}")
                self._error_message = f"GetWeight failed: {error_msg}"
                self._status = "Error"
                return 0.0
            
            # Handle different response structures
            if hasattr(reply, 'WeightSample'):
                # Handle WeightSample structure (most common for XPR)
                weight_sample = reply.WeightSample
                if hasattr(weight_sample, 'NetWeight'):
                    weight_val = float(Decimal(weight_sample.NetWeight.Value))
                    weight_unit = weight_sample.NetWeight.Unit
                elif hasattr(weight_sample, 'GrossWeight'):
                    weight_val = float(Decimal(weight_sample.GrossWeight.Value))
                    weight_unit = weight_sample.GrossWeight.Unit
                else:
                    weight_val = 0.0
                    weight_unit = 'g'
                is_stable = getattr(weight_sample, 'Stable', True)
            elif hasattr(reply, 'Weight'):
                weight_val = float(Decimal(reply.Weight.Value))
                weight_unit = reply.Weight.Unit
                is_stable = getattr(reply.Weight, 'IsStable', True)
            elif hasattr(reply, 'Value'):
                weight_val = float(Decimal(reply.Value))
                weight_unit = getattr(reply, 'Unit', 'g')
                is_stable = getattr(reply, 'IsStable', True)
            else:
                # Try to extract from reply attributes
                weight_val = float(Decimal(getattr(reply, 'WeightValue', getattr(reply, 'Value', '0'))))
                weight_unit = getattr(reply, 'WeightUnit', getattr(reply, 'Unit', 'g'))
                is_stable = getattr(reply, 'IsStable', True)
            
            # Convert to grams for consistent output (ROS2 requirement)
            if weight_unit.lower() in ['milligram', 'mg']:
                weight_val_grams = weight_val / 1000.0
            elif weight_unit.lower() in ['kilogram', 'kg']:
                weight_val_grams = weight_val * 1000.0
            elif weight_unit.lower() in ['gram', 'g']:
                weight_val_grams = weight_val
            else:
                # Default to assuming grams if unit is unknown
                weight_val_grams = weight_val
                self.logger.warning(f"Unknown weight unit: {weight_unit}, assuming grams")
            
            # Update internal state (keep original values for reference)
            self._last_weight = weight_val
            self._last_unit = weight_unit
            self._is_stable = is_stable
            
            self.logger.info(f"Weight: {weight_val_grams} g (original: {weight_val} {weight_unit})")
            self._status = "Connected"
            self._error_message = ""
            
            return weight_val_grams
            
        except Exception as e:
            self.logger.error(f"Get weight failed: {e}")
            self._error_message = str(e)
            self._status = "Error"
            return 0.0