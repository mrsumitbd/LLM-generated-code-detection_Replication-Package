def _create_github_url_error_attachment(att: Attachment) -> Attachment:
    """Create a helpful error attachment for GitHub blob URLs."""
    raw_url = att.path.replace("/blob/", "/raw/")

    att.text = f"""💡 **GitHub URL Detected**

**Original URL:** `{att.path}`
**Suggested Raw URL:** `{raw_url}`

**Issue:** GitHub blob URLs show the file viewer, not the raw file content.

**Quick Fix:** Use the raw URL instead:
```python
from attachments import Attachments
ctx = Attachments("{raw_url}")
```

**Why this happens:**
- GitHub blob URLs (with `/blob/`) show the file in GitHub's web interface
- Raw URLs (with `/raw/`) provide direct access to file content
- Attachments needs direct file access to process content

**Alternative:** Download the file locally and use the local path instead.
"""

    att.metadata.update(
        {
            "error_type": "github_url",
            "helpful_error": True,
            "suggested_url": raw_url,
            "original_url": att.path,
        }
    )
    return att