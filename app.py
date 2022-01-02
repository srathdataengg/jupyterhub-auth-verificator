from flask import Flask, request, jsonify

import sys
from time import sleep
import splunklib.results as results
import splunklib.client as client

HOST = "localhost"
PORT = 8089
USERNAME = "srath2021"
PASSWORD = "nov#DEC2021"

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Jupyterhub Auth Verificator</h1>'


@app.route('/verify')
def verify():
    username = request.args.get('username')
    service = client.connect(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)

    searchquery_normal = 'search source="movies.csv" host="Soumyakantas-MacBook-Pro.local" sourcetype="csv" ' \
                         'genres="{}"'.format(username)
    kwargs_normalsearch = {"exec_mode": "normal"}
    job = service.jobs.create(searchquery_normal, **kwargs_normalsearch)

    # A normal search returns the job's SID right away, so we need to poll for completion
    while True:
        while not job.is_ready():
            pass
        stats = {"isDone": job["isDone"],
                 "doneProgress": float(job["doneProgress"]) * 100,
                 "scanCount": int(job["scanCount"]),
                 "eventCount": int(job["eventCount"]),
                 "resultCount": int(job["resultCount"])}

        status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
                  "%(eventCount)d matched   %(resultCount)d results") % stats

        sys.stdout.write(status)
        sys.stdout.flush()
        if stats["isDone"] == "1":
            sys.stdout.write("\n\nDone!\n\n")
            break
        sleep(2)

    output = []
    # Get the results and display them
    for result in results.ResultsReader(job.results()):
        output.append(result)

    job.cancel()
    sys.stdout.write('\n')

    return jsonify(output)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
