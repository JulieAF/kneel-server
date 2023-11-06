import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class SizeView:
    def post(self, handler, size):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def get(self, handler, query_params, pk):
        if pk != 0:
            sql = "SELECT si.id, si.carets, si.price FROM Size si WHERE si.id = ?"
            # executing the SQL query using the db_get_single function
            query_results = db_get_single(sql, pk)
            # converting the query_results into a dictionary and then serializing it into a JSON string using the json.dumps function
            serialized_sizes = json.dumps(dict(query_results))
            # returning an HTTP response with a status code of 200
            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT si.id, si.carets, si.price FROM Size si"
            # executing the SQL query using the db_get_all function
            query_results = db_get_all(sql)
            # converting each row in query_results into a dictionary and storing them in a list
            sizes = [dict(row) for row in query_results]
            # serializing the list of dictionaries into a JSON string using the json.dumps function
            serialized_sizes = json.dumps(sizes)
            # returning an HTTP response with a status code of 200
            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
