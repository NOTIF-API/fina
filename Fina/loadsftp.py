import pysftp

class MySfpt:
    def __init__(self, host, username, password, port):
        self.Host = host
        self.UserName = username
        self.Password = password
        self.Port = port
    def DownloadFileFromTo(self, server_path, local_computer_path):
        with pysftp.Connection(self.Host, self.UserName, self.Password, port=self.Port) as sftp:
            sftp.get(server_path, local_computer_path)