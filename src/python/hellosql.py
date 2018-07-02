import sql

server = "mssql-instance.cfblwhszdeig.us-east-2.rds.amazonaws.com"
database = "mydb"
username = "mssql"
password = "mssql"

db = sql.Database('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

