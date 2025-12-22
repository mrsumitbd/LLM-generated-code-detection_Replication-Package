import smtplib, json, argparse, os, stat, time, base64, subprocess, socket, uuid, requests, urllib.request, sys, re, hashlib, hmac, shutil

def validate_arguments(args):
    """
        new function for an easier validation of the args passed to the function, due the fact there are now 2 calls methods. If mail_body_html is passed, nor subject and to_address are mandatory
    """
    if not args.mail_bulk and not args.mail_body_html:
        print("Error: You must provide at least --mail_bulk or --mail_body_html.")
        sys.exit(1)
    if args.mail_body_html and (not args.subject or not args.to_address):
        print("Error: If --mail_body_html is provided, both --subject and --to_address are required.")
        sys.exit(1)
    for param_name in ["subject", "to_address", "override_fromname", "override_fromemail"]:
        param_value = getattr(args, param_name, None)
        if param_value and ("\r" in param_value or "\n" in param_value):
            print(f"Error: arg '{param_name}' contains CRLF char, not allowed")
            sys.exit(1)        
    if args.debug_enabled:
        if not os.access(__script_directory__, os.W_OK):
            print(f"Current user doesn't have permission in the execution folder: {__script_directory__}")
            sys.exit(1)     
        sfw = is_secure_directory()
        if sfw:
            print(f"{sfw}")