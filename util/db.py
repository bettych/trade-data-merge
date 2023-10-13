import sshtunnel
from sshtunnel import SSHTunnelForwarder
from mysql.connector import connect

ssh_host = '104.219.248.113'
ssh_port = 21098
username = ''
password = ''

server_side_port = 3306
client_side_port = 5522

database_name = ''
database_username = ''
database_password = ''

localhost = '127.0.0.1'

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

def connect_to_db():
    tunnel = SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username = username,
        ssh_password = password,
        remote_bind_address = (localhost, server_side_port),
        local_bind_address = (localhost, client_side_port)
    )
    tunnel.start()

    connection = connect(
        user = username,
        passwd = password,
        host = tunnel.local_bind_host,
        port = tunnel.local_bind_port,
        db = database_name,
        use_pure = True
    )
    return connection