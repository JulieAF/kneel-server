import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class SizeView:
    def post(self, handler, size):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def get(self, handler, query_params, pk):
        if pk != 0:
            sql = "SELECT si.id, si.carets, si.price FROM Size si WHERE si.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_sizes = json.dumps(dict(query_results))

            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT si.id, si.carets, si.price FROM Size si"
            query_results = db_get_all(sql)
            sizes = [dict(row) for row in query_results]
            serialized_sizes = json.dumps(sizes)

            return handler.response(serialized_sizes, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
