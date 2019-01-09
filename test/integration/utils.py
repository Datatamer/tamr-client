import json
import logging


def log_entry(method, url, response):
    return json.dumps(
        {
            "method": method,
            "url": url,
            "status": response.status_code,
            "json": response.json(),
        }
    )


def response_logger(log_path, name="python-client"):
    # https://stackoverflow.com/a/53553516/1490091
    import imp

    imp.reload(logging)
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", filename=log_path, filemode="w"
    )
    return logging.getLogger(name)
