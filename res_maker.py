from functools import reduce

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

def parse_http_req(req: str):
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
        "path": req_line[1],
        "version": req_line[2],
        "header": header,
        "body": body,
    }
