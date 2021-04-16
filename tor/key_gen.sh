#!/bin/bash

# needs openssl 1.1+
# needs `basez` https://manpages.debian.org/testing/basez/base32hex.1.en.html
#   (but something else that decodes the base64 and re-encodes the raw key bytes
#    to base32 is probably fine too)

##### generate a key

openssl genpkey -algorithm x25519 -out /tmp/k1.prv.pem

##### re-formatting the keys into base32 in a way that tor likes:

# basically take the base64pem from the above key file, decode it to raw binary data,
# strip the PKCS header (key is final 32bytes of the raw data), re-encode it into base32,
# strip the "=" padding

cat /tmp/k1.prv.pem |\
    grep -v " PRIVATE KEY" |\
    base64pem -d |\
    tail --bytes=32 |\
    base32 |\
    sed 's/=//g' > /tmp/k1.prv.key

openssl pkey -in /tmp/k1.prv.pem -pubout |\
    grep -v " PUBLIC KEY" |\
    base64pem -d |\
    tail --bytes=32 |\
    base32 |\
    sed 's/=//g' > /tmp/k1.pub.key

##### do the outputs

echo "X25519 Private Key:"
cat /tmp/k1.prv.key

echo
echo "X25519 Public Key: (give this to the onion service)"
cat /tmp/k1.pub.key

echo
echo "====="
echo "Tor client configuration"
echo "====="
echo "Make sure you have ClientOnionAuthDir set in your torrc. In the"
echo "<ClientOnionAuthDir> directory, create an '.auth_private' file for the"
echo "onion service corresponding to this key (i.e. 'bob_onion.auth_private')."
echo "The contents of the <ClientOnionAuthDir>/<user>.auth_private file should"
echo "look like:"
echo
echo "    <56-char-onion-addr-without-.onion-part>:descriptor:x25519:`cat /tmp/k1.prv.key`"
echo
echo "i.e.:"
echo "    p53lf57qovyuvwsc6xnrppyply3vtqm7l6pcobkmyqsiofyeznfu5uqd:descriptor:x25519:`cat /tmp/k1.prv.key`"

echo
echo "====="
echo "Onion service configuration"
echo "====="
echo "Inside the HiddenServiceDir for this onion service, create an"
echo "/authorized_clients/ subdirectory and a '.auth' file for the user (i.e."
echo "'alice.auth'). The contents of the <HiddenServiceDir>/authorized_clients/<username>.auth"
echo "file should look like:"
echo
echo "    descriptor:x25519:`cat /tmp/k1.pub.key`"

rm -f /tmp/k1.pub.key /tmp/k1.prv.key /tmp/k1.prv.pem