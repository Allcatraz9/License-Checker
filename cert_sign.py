from backend import TransportAuthority, RSA





ta = TransportAuthority("DELHI TRANSPORT AUTHORITY",
                        12345, (5, 91), (29, 91))  #public key first then private key

cert = (1,) + RSA.rsa_encode_string("DELHI TRANSPORT AUTHORITY") + \
    RSA.rsa_encode_string("Osho") + RSA.rsa_encode_string("CG0720140016617")

print(f"""
    "cert": {cert},
    "sign": {ta.sign(cert)}
""")
