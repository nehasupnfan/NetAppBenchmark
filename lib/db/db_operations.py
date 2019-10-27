import sys
sys.path.append("../")

from constants.db_constants import Constants


class Operation(object):
    __db = None

    def __init__(self, db):
        self.__db = db
        # pass

    @staticmethod
    def create_insert_statement(columns, value):
        #column_str = ",".join(columns)
        mapping = {}
        for keys in value.keys():
            if keys in columns:
                mapping[keys] = value[keys]

        value_str = ""
        column_str = ""
        for key, value in mapping.items():
            if isinstance(value, str):
                value_str += "'%s'," % value
            else:
                value_str += "%s," % value
            column_str += "%s," % key

        return "(" + column_str[:-1] + ") values (" + value_str[:-1] + ") ;"

    @staticmethod
    def create_select_statement(table, column, value):
        if isinstance(value, str):
            value_string = "'%s'" % value
        else:
            value_string = "%s" % value

        return "SELECT * from %s where %s = %s;" % (table, column, value_string)

    @staticmethod
    def create_update_statement(table, column, value, where_column, where_clause):
        zipped_set = set(zip(column, value))
        update_string = ""
        for each in zipped_set:
            if isinstance(each[1], str):
                update_string += "%s = '%s'," % (each[0], each[1])
            else:
                update_string += "%s = %s," % (each[0], each[1])
        if where_clause and isinstance(where_clause, str):
            where_clause = "'%s'" % where_clause
        elif where_clause:
            where_clause = where_clause
        if where_column and where_clause:
            return "UPDATE %s set %s where %s = %s;" % (table, update_string[:-1], where_column, where_clause)
        else:
            return "UPDATE %s set %s;" % (table, update_string)

    @staticmethod
    def create_create_statement(table, create_value):
        create_str = ""
        for key, value in create_value.items():
            create_str += "%s %s," % (key, value)
        return "CREATE table %s ( %s ); " % (table, create_str[:-1])

    def check_exists_update(self, **kwargs):
        exist_result = self.__db.execute(
            [self.create_select_statement(kwargs["table"], kwargs["column"], kwargs["item"])])
        if exist_result[0]:
            self.__db.execute(
                [self.create_update_statement(kwargs["table"], kwargs["update_column"], kwargs["update_value"],
                                              kwargs["where_column"], kwargs["where_clause"])])
        else:
            table_columns = getattr(Constants, kwargs["table"])
            statement = self.create_insert_statement(table_columns, kwargs["value"])
            try:
                self.__db.execute(["INSERT INTO %s %s " % (kwargs["table"], statement)])
            except Exception as err:
                raise err

    def check_heartbeat_metadata(self):
        #res_offline = self.__db.execute(["select * from heartbeat where status = 'alive' ;"])
        res_dead = self.__db.execute([
            "select * from heartbeat where (strftime('%s', datetime(CURRENT_TIMESTAMP, 'localtime')) - strftime('%s', heartbeat_time) < 60 and status = 'alive');"])
        #if res_offline[0] or res_dead[0]:
        if res_dead[0]:
            return False
        else:
            return True

    def check_start_shutdown_polling(self):
        res_polling = self.__db.execute(["select * from heartbeat;"])
        if res_polling[0]:
            # Heartbeats have been registerd
            return True
        else:
            return False

    def insert_metric(self, **kwargs):
        table_columns = getattr(Constants, kwargs["table"])
        statement = self.create_insert_statement(table_columns, kwargs["value"])
        try:
            self.__db.execute(["INSERT INTO %s %s " % (kwargs["table"], statement)])
        except Exception as err:
            raise err

    def create_tables(self, *args):
        try:
            for table in args:
                v = table + "_create"
                create_stmnt = getattr(Constants, v)
                table_exists = self.__db.execute(
                    ["select name from sqlite_master where type = 'table' and name = '%s';" % table])
                if table_exists[0]:
                    self.__db.execute(["drop table %s ;" % table])
                self.__db.execute([self.create_create_statement(table, create_stmnt)])
        except Exception as error:
            raise error


