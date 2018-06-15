import os

# Application working directory.
app_root_dir = os.path.dirname(os.path.realpath(__file__))

# Certificate directory.
cert_dir = os.path.join(app_root_dir, 'cert/rpstatus')

# Path to root certificate authority file
root_ca_file = os.path.join(cert_dir, 'Public-Primary-Certification-Authority-G5.pem')

# Path to certificate pem file.
# cert_file = os.path.join(cert_dir, "180317a9e3-certificate.pem.crt")
cert_file = os.path.join(cert_dir, "f926e85654-certificate.pem.crt")

# Path to private key pem file.
# key_file = os.path.join(cert_dir, "180317a9e3-private.pem.key")
key_file = os.path.join(cert_dir, "f926e85654-private.pem.key")

# AWS IoT host.
aws_iot_host = 'a2pyus5zvqthmj.iot.us-west-2.amazonaws.com'

# AWS IoT Port.
aws_iot_port = 8883

# AWS IoT client ID should be unique for every device.
aws_iot_client_id = 'RpStatus'

# AWS IoT Thing name of the Shadow this device is associated with.
aws_iot_thing_name = 'RpStatus'

