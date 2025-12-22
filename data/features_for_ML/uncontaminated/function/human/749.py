from datetime import datetime, timezone
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, jsonify, g
import os
from flask import session

def audiobookshelf():
    if config.get("ABS_ENABLED", "yes") != "yes":
        return ("Not Found", 404)
    if not session.get("authenticated"):
        # Use client-side redirect to preserve hash fragments
        return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head><title>Redirecting...</title></head>
            <body>
                <script>
                    sessionStorage.setItem('intended_url_after_login', window.location.href);
                    window.location.href = '/login';
                </script>
            </body>
            </html>
        """)
    
    # Check for first-time IP access
    client_ip = get_client_ip()
    check_first_time_ip_access(client_ip)

    submitted = False

    if request.method == "POST":
        # Get client IP for rate limiting
        client_ip = get_client_ip()
        
        # Check form submission rate limiting
        is_rate_limited, remaining_time = check_rate_limit(client_ip, "form_submission", "audiobookshelf")
        if is_rate_limited:
            time_remaining = format_time_remaining(remaining_time)
            log_security_event("form_rate_limited", client_ip, f"Audiobookshelf form submission rate limited, {time_remaining} remaining")
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": f"Too many submissions. Please try again in {time_remaining}."})
            else:
                return render_template("audiobookshelf.html", error=f"Too many submissions. Please try again in {time_remaining}.")
        
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate email
        if not config.validate_email(email):
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Invalid email address."})
            else:
                return render_template("audiobookshelf.html", error="Invalid email address.")

        # Validate password length (minimum 8 characters)
        if len(password) < 8:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "Password must be at least 8 characters long."})
            else:
                return render_template("audiobookshelf.html", error="Password must be at least 8 characters long.")

        # Check for duplicate email
        submissions = load_json_file("audiobookshelf_submissions.json", [])
        existing_emails = [submission.get("email", "").lower() for submission in submissions]
        if email.lower() in existing_emails:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "error": "This email has already been submitted."})
            else:
                return render_template("audiobookshelf.html", error="This email has already been submitted.")

        if email and username and password:
            submission_entry = {
                "email": email,
                "username": username,
                "password": password,
                "submitted_at": datetime.now(timezone.utc).isoformat() + "Z"
            }
            submissions = load_json_file("audiobookshelf_submissions.json", [])
            submissions.append(submission_entry)
            save_json_file("audiobookshelf_submissions.json", submissions)
            submitted = True
            
            # Record successful form submission
            add_form_submission(client_ip, "audiobookshelf")
            
            send_discord_notification(email, "Audiobookshelf", event_type="abs")
            # AJAX response
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True})
        # AJAX error response
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": False, "error": "Missing required fields."})

    # List all covers in static/posters/audiobooks/
    abs_covers = []
    audiobook_dir = os.path.join("static", "posters", "audiobooks")
    if os.path.exists(audiobook_dir):
        for fname in sorted(os.listdir(audiobook_dir)):
            if fname.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
                abs_covers.append(f"/static/posters/audiobooks/{fname}")

    tautulli_enabled = bool(config.get("TAUTULLI"))
    
    # Get template context with quick_access_services
    context = get_template_context()
    
    # Add page-specific variables
    context.update({
        "submitted": submitted,
        "abs_covers": abs_covers,
        "tautulli_enabled": tautulli_enabled,
    })
    
    return render_template("audiobookshelf.html", **context)