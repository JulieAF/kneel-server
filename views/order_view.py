import sqlite3
import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class OrderView:
    def post(self, handler, order):
        sql = """
        INSERT INTO `Order`
        (metal_id, style_id, size_id, time_stamp)
        VALUES (?, ?, ?, ?)
        """
        order_id = db_create(
            sql,
            (
                order["metal_id"],
                order["style_id"],
                order["size_id"],
                order["time_stamp"],
            ),
        )
        if order_id > 0:
            order = {
                "id": order_id,
                "metal_id": order["metal_id"],
                "style_id": order["style_id"],
                "size_id": order["size_id"],
                "time_stamp": order["time_stamp"],
            }
            return handler.response(
                json.dumps(order), status.HTTP_201_SUCCESS_CREATED.value
            )
        else:
            return handler.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def get(self, handler, query_params, pk):
        print(query_params)
        base_sql = "SELECT o.id, o.metal_id, o.style_id, o.size_id, o.time_stamp "
        from_sql = "FROM `Order` o "
        join_sql = ""
        where_sql = "WHERE o.id = ?" if pk != 0 else ""

        if "_expand" in query_params and "metals" in query_params["_expand"]:
            join_sql += "JOIN Metal m ON m.id = o.metal_id "
            base_sql += ", m.id metalId, m.metal metalMetal, m.price metalPrice "

        if "_expand" in query_params and "styles" in query_params["_expand"]:
            join_sql += "JOIN Style st ON st.id = o.style_id "
            base_sql += ", st.id styleId, st.style styleStyle, st.Price stylePrice "

        if "_expand" in query_params and "sizes" in query_params["_expand"]:
            join_sql += "JOIN Size si ON si.id = o.size_id "
            base_sql += ", si.id sizeId, si.carets sizeCarets, si.Price sizePrice "

        if join_sql:  # Check if join_sql is not empty
            sql = base_sql + from_sql + join_sql + where_sql
        else:
            sql = base_sql + from_sql + where_sql
        print(sql)
        if pk != 0:
            query_results = db_get_single(sql, pk)
        else:
            query_results = db_get_all(sql)

        if isinstance(query_results, list):
            serialized_results = json.dumps([dict(row) for row in query_results])
        else:
            serialized_results = json.dumps([dict(query_results)])
        return handler.response(serialized_results, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM `Order` WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )
