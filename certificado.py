import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12

def autotenticar():
    set_token=""
    x_csrf_token= ""

    pfx_path = "C:\Certificado\PEDRO SILVIO DE OLIVEIRA PINTO_09956547867.p12"
    pfx_password = b'12345678'


    # Carregar o certificado e chave privada do PFX
    with open(pfx_path, 'rb') as f:
         pfx_data = f.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data,
        pfx_password,
        backend=default_backend()
    )

    # Salvando o certificado e a chave privada em arquivos PEM temporários
    cert_file = 'certificado.pem'
    key_file = 'chave_privada.pem'

    # Escreve o certificado em PEM
    with open(cert_file, 'wb') as cert_out:
         cert_out.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))

    # Escreve a chave privada em PEM
    with open(key_file, 'wb') as key_out:
         key_out.write(private_key.private_bytes(
         encoding=serialization.Encoding.PEM,
         format=serialization.PrivateFormat.TraditionalOpenSSL,
         encryption_algorithm=serialization.NoEncryption()  # Sem senha para chave privada
         )
    )

    url = "https://val.portalunico.siscomex.gov.br/portal/api/autenticar"

    payload = {}
    headers = {
                'Role-Type': 'IMPEXP'
              }

    response   = requests.request("POST", url, headers=headers, data=payload,cert=(cert_file,key_file))
    resultado  = {}
    if response.status_code == 200:
       response_body_json = response.json()
       return response.headers
            
  