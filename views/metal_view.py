import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class MetalView:
    def post(self, handler, metal):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def get(self, handler, query_params, pk):
        if pk != 0:
            sql = "SELECT m.id, m.metal, m.price FROM Metal m WHERE m.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_metal = json.dumps(dict(query_results))

            return handler.response(serialized_metal, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT m.id, m.metal, m.price FROM Metal m"
            query_results = db_get_all(sql)
            metals = [dict(row) for row in query_results]
            serialized_metals = json.dumps(metals)

            return handler.response(serialized_metals, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
