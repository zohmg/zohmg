# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# TODO: serve root and 404 from filesystem.

def root(environ, start_response):
    start_response('200 OK', [('content-type', 'text/html')])
    html = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
    <title>Zohmg</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <meta http-equiv="Content-Type" content="text/html" />
</head>

<body>
<div><h1>Zohmg!</h1></div>
<div>
<p>Zohmg is serving data from <a href="/data">/data</a>. You query it by HTTP GET requests.</p>
<p>There is an example consumer at <a href="/graph">/graph</a>.</p>
<p>Any files you put in the 'static' directory of your zohmg project will be available at <a href="/static">/static</a>.</p>
</div>
</body>
</html>
"""
    return html

# used if no application is found (i.e. a 404).
def not_found_hook(environ, start_response):

    if environ['PATH_INFO'] == '/':
        # well, let's serve the root.
        return root(environ, start_response)


    # user sees this message.
    message = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
    <title>Zohmg 404</title>
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
            <strong><a href="/static">/static</a></strong> - serves static files from
            the project's static directory.
        </li>
        <li>
            <strong><a href="/graph">/graph</a></strong> - example client.
        </li>
        <li>
            <strong>/data/?some-query</strong> - data server.
        </li>
    </ul>
    </p>

</body>
</html>""" % environ["PATH_INFO"]

    # serve message.
    start_response("404 Not Found", [("content-type","text/html")])
    return message
