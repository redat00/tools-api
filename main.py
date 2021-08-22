# tools.redat.me
# v0.0.1

from fastapi import FastAPI
import socket
import ssl

app = FastAPI()


def get_certificate(hostname):
    context = ssl.create_default_context()
    context.check_hostname = False

    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 5 second timeout
    conn.settimeout(5.0)
    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return ssl_info


def convert_tuple(tup):
    print(tup)
    converted_str = ''.join(tup)
    return converted_str


@app.get("/api")
def default_func():
    return {"Hello": "World"}


@app.get("/api/certs/")
def certs_dn(domain_name: str):
    cert_information = get_certificate(domain_name)
    subject = {}
    for item in cert_information['subject']:
        subject[item[0][0]] = item[0][1]
    issuer = {}
    for item in cert_information['issuer']:
        issuer[item[0][0]] = item[0][1]
    subject_alt_name = []
    for item in cert_information['subjectAltName']:
        subject_alt_name.append(item[1])
    return {
        "subject": subject,
        "issuer": issuer,
        "notBefore": cert_information['notBefore'],
        "notAfter": cert_information['notAfter'],
        "subjectAltName": subject_alt_name
    }