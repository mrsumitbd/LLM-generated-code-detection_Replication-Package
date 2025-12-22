def search_emails_handler(args, context):
        result = service.search_emails_cached(
            query=args.get('query', ''),
            account_id=args.get('account_id'),
            limit=args.get('limit', 50)
        )
        
        if 'error' in result:
            return [{"type": "text", "text": f"Error: {result['error']}"}]
        
        cache_info = f" (from {result.get('source', 'remote')})" if 'source' in result else ""
        
        text = f"Found {len(result['emails'])} emails{cache_info}\\n\\n"
        for email in result['emails']:
            text += f"{email['subject']}\\n"
            text += f"  From: {email['from']}\\n\\n"
        
        return [{"type": "text", "text": text}]