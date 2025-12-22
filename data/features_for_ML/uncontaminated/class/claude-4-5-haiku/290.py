class SokakuAdditionalAbilityIBRecord:

    def __init__(self):
        self.id = None
        self.ability_id = None
        self.ability_name = None
        self.ability_description = None
        self.ability_type = None
        self.ability_level = None
        self.ability_cost = None
        self.ability_cooldown = None
        self.ability_duration = None
        self.ability_range = None
        self.ability_damage = None
        self.ability_healing = None
        self.ability_status_effect = None
        self.ability_requirement = None
        self.ability_unlock_condition = None
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return (f"SokakuAdditionalAbilityIBRecord("
                f"id={self.id}, "
                f"ability_id={self.ability_id}, "
                f"ability_name={self.ability_name}, "
                f"ability_description={self.ability_description}, "
                f"ability_type={self.ability_type}, "
                f"ability_level={self.ability_level}, "
                f"ability_cost={self.ability_cost}, "
                f"ability_cooldown={self.ability_cooldown}, "
                f"ability_duration={self.ability_duration}, "
                f"ability_range={self.ability_range}, "
                f"ability_damage={self.ability_damage}, "
                f"ability_healing={self.ability_healing}, "
                f"ability_status_effect={self.ability_status_effect}, "
                f"ability_requirement={self.ability_requirement}, "
                f"ability_unlock_condition={self.ability_unlock_condition}, "
                f"created_at={self.created_at}, "
                f"updated_at={self.updated_at})")

    def __str__(self):
        return self.__repr__()

    def to_dict(self):
        return {
            'id': self.id,
            'ability_id': self.ability_id,
            'ability_name': self.ability_name,
            'ability_description': self.ability_description,
            'ability_type': self.ability_type,
            'ability_level': self.ability_level,
            'ability_cost': self.ability_cost,
            'ability_cooldown': self.ability_cooldown,
            'ability_duration': self.ability_duration,
            'ability_range': self.ability_range,
            'ability_damage': self.ability_damage,
            'ability_healing': self.ability_healing,
            'ability_status_effect': self.ability_status_effect,
            'ability_requirement': self.ability_requirement,
            'ability_unlock_condition': self.ability_unlock_condition,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        record = cls()
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        return record