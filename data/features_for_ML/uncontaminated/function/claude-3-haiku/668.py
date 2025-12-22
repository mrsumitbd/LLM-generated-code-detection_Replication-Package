def run_roomie_diagnostics(old, new):
    if 'edit_mode' in new and new['edit_mode']:
        return

    # Perform diagnostics on the new configuration
    diagnostics = check_for_issues(new)

    # Compare the old and new configurations
    changes = compare_configs(old, new)

    # Generate a report with the diagnostics and changes
    report = generate_report(diagnostics, changes)

    # Send the report to the appropriate channels
    send_report(report)