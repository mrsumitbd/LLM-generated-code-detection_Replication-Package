from colorama import Fore, Style, init
import os
import subprocess
import platform

def add_cron_job(server_name, base_dir, script_direct):
    """Adds a new cron job for the specified server.

    Args:
        server_name (str): The name of the server.
        base_dir (str): Base directory.
        script_dir (str): Script directory.

    Returns:
        int: 0 on success, error code on failure.
    """
    action = "add cron job"
    if not server_name:
        msg_error("add_cron_job: server_name is empty.")
        return handle_error(25, action)

    if platform.system() != "Linux":
        msg_error("Cron jobs are only supported on Linux.")
        return 1

    os.system("cls" if platform.system() == "Windows" else "clear")  # Clear
    print(
        Fore.MAGENTA
        + "Bedrock Server Manager"
        + Style.RESET_ALL
        + " - "
        + Fore.MAGENTA
        + "Task Scheduler"
        + Style.RESET_ALL
    )

    cron_jobs = get_server_cron_jobs(server_name)
    if cron_jobs is None:  # Use 'is None' to check for error from get_server_cron_jobs
        msg_error("Failed to get existing cron jobs")
        # Return to the cron_scheduler menu, do not exit

    if display_cron_job_table(cron_jobs) != 0:  # Pass the cron_jobs string
        msg_error("Failed to display existing cron jobs")

    print(f"Choose the command for '{server_name}':")
    print("1) Update Server")
    print("2) Backup Server")
    print("3) Start Server")
    print("4) Stop Server")
    print("5) Restart Server")
    print("6) Scan Players")

    while True:
        try:
            choice = int(input("Enter the number (1-6): "))
            if 1 <= choice <= 6:
                break
            else:
                msg_warn("Invalid choice, please try again.")
        except ValueError:
            msg_warn("Invalid input. Please enter a number.")

    if choice == 1:
        command = f"{script_direct} update-server --server {server_name}"
    elif choice == 2:
        command = f"{script_direct} backup-server --server {server_name}"
    elif choice == 3:
        command = f"{script_direct} start-server --server {server_name}"
    elif choice == 4:
        command = f"{script_direct} stop-server --server {server_name}"
    elif choice == 5:
        command = f"{script_direct} restart-server --server {server_name}"
    elif choice == 6:
        command = f"{script_direct} scan-players"

    # Get cron timing details with validation
    while True:
        month = input("Month (1-12 or *): ")
        if validate_cron_input(month, 1, 12) != 0:
            continue

        day = input("Day of Month (1-31 or *): ")
        if validate_cron_input(day, 1, 31) != 0:
            continue

        hour = input("Hour (0-23 or *): ")
        if validate_cron_input(hour, 0, 23) != 0:
            continue

        minute = input("Minute (0-59 or *): ")
        if validate_cron_input(minute, 0, 59) != 0:
            continue

        weekday = input("Day of Week (0-7, 0 or 7 for Sunday or *): ")
        if validate_cron_input(weekday, 0, 7) != 0:
            continue
        break  # All inputs valid

    schedule_time = convert_to_readable_schedule(month, day, hour, minute, weekday)
    if schedule_time is None:
        msg_error("Failed to convert schedule to readable format.")
        schedule_time = "ERROR CONVERTING"

    print("Your cron job will run with the following schedule:")
    print("-------------------------------------------------------")
    print(f"{'CRON JOB':<15} {'SCHEDULE':<20}  {'COMMAND':<10}")
    print("-------------------------------------------------------")

    # Format command
    display_command = command.split("bedrock-server-manager", 1)[-1].strip()
    display_command = display_command.split(".py", 1)[-1].strip()
    display_command = display_command.split("--", 1)[1].strip()
    print(
        Fore.CYAN
        + f"{minute} {hour} {day} {month} {weekday}".ljust(10)
        + Style.RESET_ALL
        + Fore.GREEN
        + f"{schedule_time:<25}"
        + Style.RESET_ALL
        + Fore.YELLOW
        + f"{display_command}"
        + Style.RESET_ALL
    )
    print()
    print("-------------------------------------------------------")

    while True:
        confirm = input("Do you want to add this job? (y/n): ").lower()
        if confirm in ("yes", "y"):
            # Add the cron job
            new_cron_job = f"{minute} {hour} {day} {month} {weekday} {command}"
            try:
                # Get existing cron jobs
                result = subprocess.run(
                    ["crontab", "-l"], capture_output=True, text=True, check=False
                )
                existing_crontab = result.stdout
                # If no crontab exists and there is an error, set existing crontab to empty
                if result.returncode != 0 and "no crontab for" in result.stderr.lower():
                    existing_crontab = ""
                elif result.returncode != 0:  # If there is another error, raise it
                    raise subprocess.CalledProcessError(
                        result.returncode, result.stderr
                    )

                # Add the new job and write back to crontab
                new_crontab = existing_crontab + new_cron_job + "\n"
                process = subprocess.Popen(
                    ["crontab", "-"], stdin=subprocess.PIPE, text=True
                )
                process.communicate(input=new_crontab)
                if process.returncode != 0:  # Check return code
                    raise subprocess.CalledProcessError(process.returncode, "crontab")
                msg_ok("Cron job added successfully!")
                return 0
            except subprocess.CalledProcessError as e:
                msg_error(f"Failed to add cron job: {e}")
                return handle_error(22, action)
            except FileNotFoundError:
                msg_error("crontab command not found")
                return handle_error(22, action)

        elif confirm in ("no", "n", ""):
            msg_info("Cron job not added.")
            return 0
        else:
            msg_warn("Invalid input. Please answer 'yes' or 'no'.")