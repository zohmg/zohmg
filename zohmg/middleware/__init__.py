# used if no application is found (i.e. a 404).
def not_found_hook(environ,start_response):
    # user sees this message.
    message = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
    <title>Zohmg Error</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <meta http-equiv="Content-Type" content="text/html" />
</head>

<body>

    <h1>404 Not Found</h1>

    <p>
    There is no application for the path
    <blockquote>
    %s
    </blockquote>
    </p>

    <p>
    Available applications
    <ul>
        <li>
            <strong>/client/filename</strong> - serves static files from
            the project's clients directory.
        </li>
        <li>
            <strong>/data/?query</strong> - serves aggregates from HBase.
        </li>
        <li>
            <strong>/transform/filename/?query</strong> - serves
            aggregates transformed with a transformer from the project's
            transformers directory.
        </li>
    </ul>
    </p>

    <p>
    Zohmg.
    </p>

</body>
</html>""" % environ["PATH_INFO"]

    # serve message.
    start_response("404 Not Found", [("content-type","text/html")])
    return message
