import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class MetalView:
    def post(self, handler, metal):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def get(self, handler, query_params, pk):
        if pk != 0:
            sql = "SELECT m.id, m.metal, m.price FROM Metal m WHERE m.id = ?"
            # executing the SQL query using the db_get_single function
            query_results = db_get_single(sql, pk)
            # converting the query_results into a dictionary and then serializing it into a JSON string using the json.dumps functionß
            serialized_metal = json.dumps(dict(query_results))

            return handler.response(serialized_metal, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT m.id, m.metal, m.price FROM Metal m"
            # executing the SQL query using the db_get_all function
            query_results = db_get_all(sql)
            # converting each row in query_results into a dictionary and storing them in a list
            metals = [dict(row) for row in query_results]
            # serializing the list of dictionaries into a JSON string using the json.dumps function
            serialized_metals = json.dumps(metals)
            # returning an HTTP response with a status code of 200
            return handler.response(serialized_metals, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
