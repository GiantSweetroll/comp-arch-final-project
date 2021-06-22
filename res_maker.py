from functools import reduce
from os import path, getcwd
import datetime

__format_type = {
    ".html": "text/html"
}

def __header_to_dict(x: dict, y: str):
    # If no string, return.
    if len(y) <= 0: return x

    # Append to the dictionary
    index = y.find(":")
    
    # Parse number, if possible.
    content = y[index + 2:]
    if content.isdigit():
        content = int(content)
    elif content.isdecimal():
        content = float(content)
    
    # Insert
    x[y[:index]] = content
    return x

def parse_http_req(req: str) -> dict:
    """Processes the HTTP request string and parses it to a dictionary.
    :req: Request string

    :returns: Dictionary of parsed string.
    """
    double_n = req.find("\n\n")

    # Do this to resolve no double newline in header
    header_part = req[
        :(double_n + 1) if double_n != -1 else len(req)
    ].split("\n")

    req_line = header_part[0].split(" ")
    header = reduce(
        __header_to_dict,
        header_part[1:],
        {}
    )

    content_pos = double_n+2
    body = "" if double_n == -1 else req[
        content_pos:(content_pos + header.get("Content-Length", -content_pos))
    ]

    return {
        "verb": req_line[0],
        "path": "/index.html" if req_line[1] == "/" else req_line[1],
        "version": req_line[2],
        "header": header,
        "body": body,
    }

def make_response(req: str):
    """Creates a response string for the supplied argument
    """
    p_req = parse_http_req(req)
    req_path = path.join(getcwd(), p_req["path"][1:])

    status = "200 OK"
    body = ""

    # File format, for header
    format = p_req["path"][p_req["path"].rfind("."):]

    # Open file
    try:
        with open(req_path, "r") as file:
            body = file.read()
    except FileNotFoundError:
        status = "404 Not Found"
    except Exception:
        status = "500 Internal Server Error"
    
    response = f"""HTTP/1.1 {status}
Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Content-Length: {len(body)}
Content-Type: {__format_type.get(format, "")}

{body}"""

    # Print response
    print(f"Request {p_req['verb']} {p_req['path']} | {status}")

    return response
