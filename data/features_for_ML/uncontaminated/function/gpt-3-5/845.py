def get_version() -> str:
    import pkg_resources
    return pkg_resources.get_distribution("your_package_name").version