import sqlite3
import datetime
import os

"""
模板模式：
将重复的步骤在基类中实现，那些不同的步骤则在子类中重写，以提供自定义的功能。
"""


def data_write():
    """创建数据库并写入一些示例数据"""
    # 连接数据库
    conn = sqlite3.connect("sales.db")

    # 建表
    conn.execute("CREATE TABLE Sales (salesperson text, amt currency, year integer, model text, new boolean)")
    # 插入数据
    conn.execute("INSERT INTO Sales values ('Tim', 16000, 2010, 'Honda Fit', 'true')")
    conn.execute("INSERT INTO Sales values ('Tim', 9000, 2006, 'Ford Focus', 'false')")
    conn.execute("INSERT INTO Sales values ('Gayle', 8000, 2004, 'Dodge Neon', 'false')")
    conn.execute("INSERT INTO Sales values ('Gayle', 28000, 2009, 'Ford Mustang', 'true')")
    conn.execute("INSERT INTO Sales values ('Gayle', 50000, 2010, 'Lincoln Navigator', 'true')")
    conn.execute("INSERT INTO Sales values ('Don', 20000, 2008, 'Toyota Prius', 'false')")
    conn.commit()
    conn.close()


class QueryTemplate:
    def connect(self):
        self.conn = sqlite3.connect("sales.db")

    def construct_query(self):
        raise NotImplementedError()

    def do_query(self):
        results = self.conn.execute(self.query)
        self.results = results.fetchall()

    def format_results(self):
        output = []
        for row in self.results:
            row = [str(i) for i in row]
            output.append(", ".join(row))
        self.formatted_results = "\n".join(output)

    def output_results(self):
        raise NotImplementedError()

    def process_format(self):
        self.connect()
        self.construct_query()
        self.do_query()
        self.format_results()
        self.output_results()


class UserGrossQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select salesperson, sum(amt) from Sales group by salesperson"

    def output_results(self):
        filename = "gross_sales_{0}".format(datetime.date.today().strftime("%y%m%d"))
        with open(filename, 'w') as outfile:
            outfile.write(self.formatted_results)


class NewVehiclesQuery(QueryTemplate):
    def construct_query(self):
        self.query = "select * from Sales where new='true'"

    def output_results(self):
        print(self.formatted_results)


if __name__ == "__main__":
    # 将数据写入数据库
    current_path = os.path.dirname(__file__)
    db_file_path = os.path.join(current_path, "sales.db")
    if not os.path.exists(db_file_path):
        print("dataset init")
        data_write()

    nv = NewVehiclesQuery()
    nv.process_format()

    ug = UserGrossQuery()
    ug.process_format()

