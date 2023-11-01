import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class StyleView:
    def post(self, handler, style):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)

    def get(self, handler, query_params, pk):
        if pk != 0:
            sql = "SELECT st.id, st.style, st.price FROM Style st WHERE st.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_styles = json.dumps(dict(query_results))

            return handler.response(serialized_styles, status.HTTP_200_SUCCESS.value)
        else:
            sql = "SELECT st.id, st.style, st.price FROM Style st"
            query_results = db_get_all(sql)
            styles = [dict(row) for row in query_results]
            serialized_styles = json.dumps(styles)

            return handler.response(serialized_styles, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        return handler.response("", status.HTTP_405_UNSUPPORTED_METHOD.value)
