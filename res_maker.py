from functools import reduce
from os import path, getcwd
from sys import argv
import datetime
import mimetypes
from socket import socket
from time import time, time_ns
from typing import Tuple

# Init
# TODO: Other files that are not here is sent to be downloaded.
mimetypes.init()

# Set the server working directory
working_dir = path.abspath(argv[1]) if (len(argv) >= 2) else getcwd()

def __header_to_dict(x: dict, y: str) -> dict:
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
    :req: Request HTTP string

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

def make_response(req: str) -> Tuple[bytes, bytes]:
    """Creates a response string for the supplied argument
    :req: Request HTTP string

    :returns: Tuple of 2. The first one is the header, and the second one is
    body. Both is in binary.
    """
    start_time = time_ns()

    p_req = parse_http_req(req)
    req_path = path.join(working_dir, p_req["path"][1:])

    status = "200 OK"
    body = b""

    # File format, for header
    # format = p_req["path"][p_req["path"].rfind("."):]

    # Open file
    try:
        with open(req_path, "rb") as file:
            body = file.read()
    except FileNotFoundError:
        status = "404 Not Found"
    except Exception:
        status = "500 Internal Server Error"

    mime_tup = mimetypes.guess_type(req_path)
    mime = f"{mime_tup[0]}; {mime_tup[1]}"
    
    header = f"""HTTP/1.1 {status}
Server: EpicusMaximus
Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Content-Length: {len(body)}
Content-Type: {mime}

"""
    proctime = ((time_ns() - start_time)/1000000).__round__(3)
    # Print status
    print(f"Request \
{p_req['verb']} {p_req['path']} | \
{status} | \
Proctime: {proctime}ms")

    # Return everything
    return (header.encode("utf-8"), body)

def handle_request(c: socket, addr):
    req = c.recv(8192).decode("utf-8")
    res = make_response(req)

    c.send(res[0])
    c.send(res[1])
