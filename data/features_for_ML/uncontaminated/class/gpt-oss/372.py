class AgentsDesignDesignNodeTemplates:
    """Design 节点提示词模板类"""

    @staticmethod
    def get_design_zh() -> str:
        return (
            "请根据以下需求设计一个系统架构：\n"
            "1. 目标用户：中小企业的财务人员。\n"
            "2. 核心功能：自动生成财务报表、预算预测、成本分析。\n"
            "3. 技术栈：Python、Django、PostgreSQL、React。\n"
            "4. 需要考虑的安全性：数据加密、权限管理、审计日志。\n"
            "请给出详细的模块划分、接口设计和数据库表结构。"
        )

    @staticmethod
    def get_design_en() -> str:
        return (
            "Design a system architecture based on the following requirements:\n"
            "1. Target users: finance staff in small and medium enterprises.\n"
            "2. Core features: automated financial statement generation, budget forecasting, cost analysis.\n"
            "3. Technology stack: Python, Django, PostgreSQL, React.\n"
            "4. Security considerations: data encryption, access control, audit logging.\n"
            "Provide a detailed module breakdown, API design, and database schema."
        )

    @staticmethod
    def get_design_ja() -> str:
        return (
            "以下の要件に基づいてシステムアーキテクチャを設計してください。\n"
            "1. 対象ユーザー：中小企業の財務担当者。\n"
            "2. コア機能：財務諸表の自動生成、予算予測、コスト分析。\n"
            "3. 技術スタック：Python、Django、PostgreSQL、React。\n"
            "4. セキュリティ要件：データ暗号化、権限管理、監査ログ。\n"
            "詳細なモジュール分割、API設計、データベーススキーマを提示してください。"
        )

    @staticmethod
    def get_design_es() -> str:
        return (
            "Diseña una arquitectura de sistema basada en los siguientes requisitos:\n"
            "1. Usuarios objetivo: personal financiero de pequeñas y medianas empresas.\n"
            "2. Funciones principales: generación automática de estados financieros, previsión presupuestaria, análisis de costos.\n"
            "3. Stack tecnológico: Python, Django, PostgreSQL, React.\n"
            "4. Consideraciones de seguridad: cifrado de datos, control de acceso, registro de auditoría.\n"
            "Proporciona un desglose detallado de módulos, diseño de API y esquema de base de datos."
        )

    @staticmethod
    def get_design_fr() -> str:
        return (
            "Concevez une architecture système basée sur les exigences suivantes :\n"
            "1. Utilisateurs cibles : personnel financier des PME.\n"
            "2. Fonctionnalités principales : génération automatique de rapports financiers, prévision budgétaire, analyse des coûts.\n"
            "3. Stack technologique : Python, Django, PostgreSQL, React.\n"
            "4. Considérations de sécurité : chiffrement des données, gestion des accès, journalisation d'audit.\n"
            "Fournissez une ventilation détaillée des modules, la conception d'API et le schéma de base de données."
        )