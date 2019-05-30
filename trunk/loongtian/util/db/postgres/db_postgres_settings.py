class PostgresSetting():

    def __init__(self, Host=None, Port=None, Database=None, User=None, Password=None):
        self.Host = Host  # "192.168.1.100"
        self.Port = Port
        self.Database = Database
        self.User = User
        self.Password = Password


DB_Postgres_Settings={
    "nvwa":PostgresSetting(Host ="localhost", Port = 5432, Database ="nvwa", User ="postgres", Password ="123456qaz")
}

