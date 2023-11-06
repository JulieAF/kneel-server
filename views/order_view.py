import sqlite3
import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create


class OrderView:
    # method, self (Python convention for referring to the object the method is being called on), handler (object used to send HTTP responses), and order (dictionary containing details about the order)
    def post(self, handler, order):
        sql = """
        INSERT INTO `Order`
        (metal_id, style_id, size_id, time_stamp)
        VALUES (?, ?, ?, ?)
        """
        # db_create returns the ID of the newly created order
        # arguments to db_create = SQL command and a tuple containing the values to replace the ? placeholders
        order_id = db_create(
            sql,
            (
                order["metal_id"],
                order["style_id"],
                order["size_id"],
                order["time_stamp"],
            ),
        )
        # if true creates a new dictionary with the order details and the ID of the newly created order
        if order_id > 0:
            order = {
                "id": order_id,
                "metal_id": order["metal_id"],
                "style_id": order["style_id"],
                "size_id": order["size_id"],
                "time_stamp": order["time_stamp"],
            }
            # send a HTTP response with a 201 status code and the order details in JSON format.
            return handler.response(
                json.dumps(order), status.HTTP_201_SUCCESS_CREATED.value
            )
        # handles the case where the order was not successfully created (because order_id is not greater than 0). Sends a HTTP response with a 404 status code
        else:
            return handler.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def get(self, handler, query_params, pk):
        # initialize strings used to construct SQL query
        base_sql = "SELECT o.id, o.metal_id, o.style_id, o.size_id, o.time_stamp "
        from_sql = "FROM `Order` o "
        join_sql = ""
        where_sql = "WHERE o.id = ?" if pk != 0 else ""
        # if both conditions are true: that the key _expand exists in query_params dictionary and that the key metals, styles, and/or sizes exists in the value associated with the key _expand in query_params
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
        if pk != 0:
            query_results = db_get_single(sql, pk)
        else:
            query_results = db_get_all(sql)
        # initializes an empty list
        orders = []
        # for loop that iterates over each row(order) in query_results. query_results is a list of dictionaries
        for row in query_results:
            # creates a new dictionary named order for each row(order) found in query_results. It uses the get method to retrieve the value of each key from the row
            order = {
                "id": row.get("id"),
                "metal_id": row.get("metal_id"),
                "style_id": row.get("style_id"),
                "size_id": row.get("size_id"),
                "time_stamp": row.get("time_stamp"),
            }
            # If both conditions are true, it creates a new dictionary named metal for each row(metal) found in query_results and adds it to the order dictionary under the key "metal"
            if "_expand" in query_params and "metals" in query_params["_expand"]:
                metal = {
                    "id": row.get("metalId"),
                    "metal": row.get("metalMetal"),
                    "price": row.get("metalPrice"),
                }
                # Remove None values from the metal dictionary
                metal = {k: v for k, v in metal.items() if v is not None}
                # If the metal dictionary is not empty, this line adds it to the order dictionary under the key "metal"
                if metal:
                    order["metal"] = metal
            # If both conditions are true, it creates a new dictionary named style for each row(style) in query_results and adds it to the order dictionary under the key "style"
            if "_expand" in query_params and "styles" in query_params["_expand"]:
                style = {
                    "id": row.get("styleId"),
                    "style": row.get("styleStyle"),
                    "price": row.get("stylePrice"),
                }
                # Remove None values from the style dictionary
                style = {k: v for k, v in style.items() if v is not None}
                # If the style dictionary is not empty, this line adds it to the order dictionary under the key "style"
                if style:
                    order["style"] = style
            ##If both conditions are true, it creates a new dictionary named size for each row(size) in query_results and adds it to the order dictionary under the key "size"
            if "_expand" in query_params and "sizes" in query_params["_expand"]:
                size = {
                    "id": row.get("sizeId"),
                    "carets": row.get("sizeCarets"),
                    "price": row.get("sizePrice"),
                }
                # Remove None values from the size dictionary
                size = {k: v for k, v in size.items() if v is not None}
                # If the size dictionary is not empty, this line adds it to the order dictionary under the key "size
                if size:
                    order["size"] = size
            # adds the order dictionary to the orders list
            orders.append(order)
            # serialize the orders list into a JSON string using json.dumps, and then return this JSON string in the HTTP response with a status code of 200
            serialized_results = json.dumps(orders)
            # handler.response method is used to create the HTTP response.
            return handler.response(serialized_results, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM `Order` WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )
