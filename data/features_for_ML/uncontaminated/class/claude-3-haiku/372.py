class AgentsDesignDesignNodeTemplates:
    """Design 节点提示词模板类"""

    @staticmethod
    def get_design_zh() -> str:
        return "请设计一个{task}的{type}。请考虑以下几点:\n1. {point1}\n2. {point2}\n3. {point3}"

    @staticmethod
    def get_design_en() -> str:
        return "Please design a {type} for {task}. Consider the following points:\n1. {point1}\n2. {point2}\n3. {point3}"

    @staticmethod
    def get_design_ja() -> str:
        return "{task}の{type}を設計してください。以下の点を考慮してください:\n1. {point1}\n2. {point2}\n3. {point3}"

    @staticmethod
    def get_design_es() -> str:
        return "Por favor, diseña un {type} para {task}. Considera los siguientes puntos:\n1. {point1}\n2. {point2}\n3. {point3}"

    @staticmethod
    def get_design_fr() -> str:
        return "Veuillez concevoir un {type} pour {task}. Prenez en compte les points suivants :\n1. {point1}\n2. {point2}\n3. {point3}"