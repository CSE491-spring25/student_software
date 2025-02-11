#!/usr/bin/env python

import argparse
import urllib
import urllib.parse
import urllib.request
import ssl
import os
import json
import traceback
import time
import base64

timeout = 120 # seconds

DEBUG = False
'''
server_cert = """
-----BEGIN CERTIFICATE-----
MIIDqDCCApCgAwIBAgIUKoRNdIJnstmUqsA5Tvb/mxDStOcwDQYJKoZIhvcNAQEL
BQAwYzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1BMRIwEAYDVQQHDAlDYW1icmlk
Z2UxDDAKBgNVBAoMA01JVDEOMAwGA1UECwwFQ1NBSUwxFTATBgNVBAMMDDEyOC4z
MC45Mi43OTAeFw0yNDEyMjYxNjQwMDlaFw0yNTEyMjYxNjQwMDlaMGMxCzAJBgNV
BAYTAlVTMQswCQYDVQQIDAJNQTESMBAGA1UEBwwJQ2FtYnJpZGdlMQwwCgYDVQQK
DANNSVQxDjAMBgNVBAsMBUNTQUlMMRUwEwYDVQQDDAwxMjguMzAuOTIuNzkwggEi
MA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC/1oVcLP1GAy4DuoR9l8W5psKm
ORdKMDHlORe2fTtP+JyTNY3tkNwnU5MR8/NBoLYs9DYG6qMX03WJlpYqSz3hjnSb
MYhMhGOd3WS2o0gJrZArCBy1vGs+8qg7FJYobiOqyefb7sSAketpnKuFkcnNYiJw
JtFUNHrMKIscakXixkdinz84LEMRo5cSW6isXu+fmHJ93Yopqpok69FC5upCtFpn
FwYw4KeVUo/v75jlCAtPocqRyWwxxN+BVbDu9amVSgX9qXiYAIwvV09KdV/zeBBA
QKn4VZhJuHD35jRyRg0F4wMkjtq4DbNs9DX42qEPW9YpmitNmXm3f7iy0LbzAgMB
AAGjVDBSMAsGA1UdDwQEAwIEMDATBgNVHSUEDDAKBggrBgEFBQcDATAPBgNVHREE
CDAGhwSAHlxPMB0GA1UdDgQWBBQmj3klGdnYaL2zIed/RFjx8kN+WTANBgkqhkiG
9w0BAQsFAAOCAQEAoUgy+buFszyH251PAS2YXPMyL8Ktxh//wmzeEgF9jPmLFsUh
+4vDjvW90DYnDj5MA6MeOEe7IHqozgRdmquV9JJiS7tsqaRfhcS/NDHYJVe/u4sK
0D3Ed2kV3M3X7TXZFv39nOEPft6u1Ci8FtbQa+89SXWPuwE7kvWWfIMvLPfsdkY3
W3CzKYZu2pApO2C+oWsgX2ArQCwG4775NIcFO8XFuDeh+9tC1lpMAvSNDOnS8BIy
QHA6L9zCf5eN9sRLFLuxlXPmU1GFWbwNeA5r5LWRHcbGHR4BKBJ+X0Yt+IR5t8DQ
9cBeOh0fdZY1TeNZsWDOPMmqXXIEaOl7Jp6Skw==
-----END CERTIFICATE-----
"""

server_ip_port = "128.30.92.79:4443"
'''
server_cert = """
-----BEGIN CERTIFICATE-----
MIIDoDCCAoigAwIBAgIUR0mJFfz7DoD4ycyFvEmx2/8h/V0wDQYJKoZIhvcNAQEL
BQAwXzELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk1JMRAwDgYDVQQHDAdMYW5zaW5n
MQwwCgYDVQQKDANNU1UxDDAKBgNVBAsMA0NTRTEVMBMGA1UEAwwMMzUuOS4xMzAu
MjM2MB4XDTI1MDExMDE4NDE0NVoXDTI2MDExMDE4NDE0NVowXzELMAkGA1UEBhMC
VVMxCzAJBgNVBAgMAk1JMRAwDgYDVQQHDAdMYW5zaW5nMQwwCgYDVQQKDANNU1Ux
DDAKBgNVBAsMA0NTRTEVMBMGA1UEAwwMMzUuOS4xMzAuMjM2MIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlbm67tEu3O44B/xPmcbofqX2F6hlRR5RTfzo
nvqMtW+RPvHDROCDyWZ0FjqVp+ukSwjxJdJrxl91gWFtyBQqgWOAW1kM+PmvlUXI
D65n6ViHfnmnSJ7fPgxrxV76Hb0c/OQBs5IvAsIyeU5QdtoGMZlfXDomtSvgnDmt
YmfP0SFsuh+X3CalR1HVw/cWG0ssVeY6aAYeFzdSAuCo9j9tgbVAfDmS4NuNpd68
fZUQHl2yzYkco1138Tiib/52KofANzxby4mzYLLtDl1vv13XFqELsUuQ9XBEQfoL
SW5gJ2343e+t4cW0sAFSaSu4HI7QJwfo0qkmgdYf0cx/Xwn1RwIDAQABo1QwUjAL
BgNVHQ8EBAMCBDAwEwYDVR0lBAwwCgYIKwYBBQUHAwEwDwYDVR0RBAgwBocEIwmC
7DAdBgNVHQ4EFgQUpMVk555zMbfTGzDioEp6o1dd6GkwDQYJKoZIhvcNAQELBQAD
ggEBABEzTGUCByew7dmeWau8HagDlgImwaUuMNSsQhM5Ok53bt9yIyWZQ5pGI87U
NUH0wxyO0dhQ23mBy3f0LNXg+Ktc9pAUgGJFOejmyE7Bnd/c2XFcJ7xg73dip08d
ZlEqTecfoNMADRq2e6SQgvMv3UFQ1Si47SfSyfphus4BHv9RW8ueuN4zlL1DMSwD
VLbUWNOBXBwvODTTaVtsM+miKOmnQQegKQXp5R5sFA3gv4ffGkXrzPKnfVL9RPGE
rsJzVPPXBc4R1wEhe3ZFlrIYe7N/cRigFoIVnLYSmDVolc9S6Sv1s7xiROzYNVYT
HK0KggEH/5qjRW9U7ahlfxZnXu8=
-----END CERTIFICATE-----
"""

server_ip_port = "35.9.130.236:4443"

hidden_perf_directory = "/tmp/spe-student-jobs"

poll_interval = 1 # seconds

def process_response(response, script_args=None, job_id=None):
    result = json.loads(response["result"])["result_json"]
    if result["success"]:
        print("Job completed successfully.")
    else:
        print("Job failed.")
    print()
    print("--- Execution log:")
    print()
    print(result["execute_log"])
    
    if 'perf_data' in result and script_args:
        print()
        print("Perf data saved.")
        with open("perf.data", "wb") as f:
            f.write(base64.b64decode(result["perf_data"]))
        for idx, (orig_file, file) in enumerate(zip(script_args["orig_files"], script_args["files"])):
            if orig_file[:2] == './': 
                orig_file = orig_file[2:]
            with open(orig_file, 'rb') as f:
                orig_file_content = f.read()
                # write this to a hidden directory
                assert job_id is not None and script_args is not None
                # if job-{job_id} doesn't exist, create it
                if not os.path.exists(os.path.join(hidden_perf_directory, f"job-{job_id}")):
                    os.makedirs(os.path.join(hidden_perf_directory, f"job-{job_id}"))
                with open(os.path.join(hidden_perf_directory, f"job-{job_id}/{file}"), "wb") as f2:
                    f2.write(orig_file_content)
                    
    
def get_last_complete_job(username, token, ssl_ctx):
    query_params = {"username": username, "token": token}
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/last_complete?" + url_query
    req = urllib.request.Request(url, method="GET")
    try: 
        with urllib.request.urlopen(req, context=ssl_ctx) as f:
            response = json.load(f)
            if response["success"]:
                print("Last completed job:")
                process_response(response)
                if "perf_data" in response["result"]:
                    print("Can't retrieve perf data for last job.")
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")


def submit_job(username, token, script_args, ssl_ctx, override_pending=False, is_util=False):
    query_params = {"username": username, "token": token, "debug": int(DEBUG)}
    if override_pending:
        query_params["override_pending"] = "1"
    query_params["is_util"] = 1 if is_util else 0
    url_query = urllib.parse.urlencode(query_params)
    url = "https://" + server_ip_port + "/api/submit?" + url_query

    file_dict = set()
    for idx, file in enumerate(script_args["orig_files"]):
        with open(file, 'rb') as f:
            file_content = f.read()
            base64_encoded = base64.b64encode(file_content).decode("utf-8")
            script_args[f"file{idx}"] = base64_encoded
        script_args["files"].append(os.path.basename(file))
        if os.path.basename(file) not in file_dict:
            file_dict.add(os.path.basename(file))
        else:
            print(f"Duplicate file: {os.path.basename(file)}, please ensure all files are unique.")
            raise Exception("Duplicate file")
    req_json = json.dumps(script_args).encode("utf-8")
    request = urllib.request.Request(url, data=req_json, method="POST")
    request.add_header("Content-Type", "application/json")
    
    try:
        response = urllib.request.urlopen(request, context=ssl_ctx)
        response_json = json.load(response)
        return response_json["job_id"]
    except urllib.error.HTTPError as e:
        if e.code == 400:
            response_json = json.load(e)
            if response_json["error"] == "pending_job":
                return None
        else: 
            response_json = json.load(e)
            error = response_json.get("error", None)
            if error: 
                print("\n" + "=" * 50)
                print("ERROR:".center(50))
                print("-" * 50)
                print(error)
                print("=" * 50 + "\n")
        raise e
    
def preprocess_args(script_args):
    remaining_args = []
    files = []
    do_perf = False
    for idx, arg in enumerate(script_args):
        if idx == 0 and arg.startswith("perf"):
            assert script_args[idx + 1] == "record"
            do_perf = True

        if os.path.isfile(arg):
            remaining_args.append(f"file{len(files)}")
            files.append(arg)
        else:
            remaining_args.append(arg)
    returns = {
        "command": " ".join(remaining_args),
        "orig_files": files,
        "files": [],
        "perf": do_perf, 
    }
    return returns

def main():
    if DEBUG:
        print("DEBUG:", DEBUG)
    parser = argparse.ArgumentParser()
    # parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments for the script')
    parser.add_argument(
        "--auth",
        help="Authentication token (defaults to ./auth.json in the same directory as this script)",
        default=None
    )
    parser.add_argument(
        "--cores", 
        type=int,
        help="Number of cores to request",
        default=1
    )
    parser.add_argument("--username", type=str, help="Username", default="")
    parser.add_argument("--token", type=str, help="Token", default="")
    parser.add_argument("--override-pending", action="store_true", help="Allow overriding pending jobs")
    parser.add_argument("--utils", action="store_true", help="Use utility queue instead of main queue, for testing purposes instead of benchmarking performance. Timeout will be longer.")
    parser.add_argument("--bypass-last-job", action="store_true", help="Bypass checking for your last job.")
    args, script_args = parser.parse_known_args()
    if len(script_args) == 0:
        print("Please provide a script to run.")
        exit(1)
    
    # turn script_args into a dictionary 
    script_args = preprocess_args(script_args)
    script_args["cores"] = args.cores
    
    if args.username != "" and args.token != "":
        username = args.username
        token = args.token
    else:
        ## Check if auth token is valid
        token_path = f"{os.path.expanduser('~')}/.telerun/auth.json"
        if not os.path.isfile(token_path):
            if args.auth is None:
                print("Please provide an authentication token.")
                exit(1)
            if not os.path.isfile(args.auth):
                print("Invalid authentication token.")
                exit(1)
            if not os.path.exists(os.path.dirname(token_path)):
                os.system("mkdir -p " + os.path.dirname(token_path))   
            os.system(f"cp {args.auth} {token_path}")
            print("Authentication token copied to", token_path)
                
        ## Load auth token
        with open(token_path, "r") as f:
            auth = json.load(f)
        username = auth["username"]
        token = auth["token"]
    is_util = args.utils
    ssl_ctx = ssl.create_default_context(cadata=server_cert)

    if not args.bypass_last_job:
        last_complete_job = get_last_complete_job(username, token, ssl_ctx)

    job_id = submit_job(username, token, script_args, ssl_ctx, override_pending=args.override_pending, is_util=is_util)
    if job_id is None:
        print("You already have a pending job. Pass '--override-pending' if you want to replace it.")
        exit(1)
    print("Submitted job")

    already_claimed = False
    old_time = time.time()
    while True:
        
        if time.time() - old_time > timeout:
            print("Time limit exceeded.")
            break
        try:
            time.sleep(poll_interval)
                
            url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
            req = urllib.request.Request(
                "https://" + server_ip_port + "/api/status?" + url_query,
                method="GET",
            )
            with urllib.request.urlopen(req, context=ssl_ctx) as f:
                response = json.load(f)
            
            state = response["state"]
            if state == "pending":
                continue
            elif state == "claimed":
                if not already_claimed:
                    print("Compiling and running, took {:.2f} seconds to be claimed.".format(time.time() - old_time)) 
                    already_claimed = True
                continue
            elif state == "complete":
                # TODO: Don't double-nest JSON!
                process_response(response, script_args=script_args, job_id=job_id) 
                
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/reported?" + url_query,
                    method="POST",
                )    
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    print("Reported job completion.")
                    
                break
        except urllib.error.HTTPError as e:
            if e.code == 400:
                response_json = json.load(e)
                if response_json["error"] == "pending_job":
                    return None
            else: 
                response_json = json.load(e)
                error = response_json.get("error", None)
                if error: 
                    print("\n" + "=" * 50)
                    print("ERROR:".center(50))
                    print("-" * 50)
                    print(error)
                    print("=" * 50 + "\n")
            raise e
        except KeyboardInterrupt as e: 
            print("Keyboard Interrupted.")
            if not already_claimed: 
                url_query = urllib.parse.urlencode({"username": username, "token": token, "job_id": job_id})
                req = urllib.request.Request(
                    "https://" + server_ip_port + "/api/delete?" + url_query,
                    method="POST",
                )
                with urllib.request.urlopen(req, context=ssl_ctx) as f:
                    response = json.load(f)
                    if response["success"]:
                        print("Job removed successfully.")
            break
        except Exception as e:
            traceback.print_exc()
            continue

if __name__ == "__main__":
    os.makedirs(hidden_perf_directory, exist_ok=True)
    main()
