from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.conf import settings

WHERE_QUERY_MAPPING = {
    "date_from": "date >= '{}'",
    "date_to": "date <= '{}'",
    "countries": "country = '{}'",
    "channels": "channel = '{}'",
    "systems": "os = '{}'"
}


def build_query(**kwargs):
    """returns mysql Query"""

    query = """
    SELECT {select_columns}, (SUM(spend) / SUM(installs)) as CPI FROM {table_name} 
    {where_query} 
    {group_by_query} 
    {order_by_query};
    """

    select_columns = ", ".join(kwargs.get("group_by") + ["SUM({col}) AS {col}".format(col=i) for i in kwargs.get("sum_on")])
    columns = ",".join(kwargs.get("group_by"))

    where_query = ""
    where_query_vals = []
    for key, val in WHERE_QUERY_MAPPING.items():
        for i in kwargs.get(key):
            where_query_vals.append(WHERE_QUERY_MAPPING[key].format(i))
    if where_query_vals:
        where_query = "WHERE {}".format(" AND ".join(where_query_vals))

    if not kwargs.get("group_by"):
        raise ValueError("No group by columns found.")
    group_by_query = "GROUP BY {}".format(columns)

    order_by_query = "ORDER BY {} {}".format(kwargs.get("sort_by"), kwargs.get("order_type"))

    sql_query = query.format(
        table_name=settings.CONFIG["MYSQL"]["DB_TABLE"],
        select_columns=select_columns,
        where_query=where_query,
        group_by_query=group_by_query,
        order_by_query=order_by_query,
    )
    print(sql_query)
    return sql_query


def get_api(request):
    """Returns data based on GET parameters."""
    date_from = request.GET.getlist("date_from")
    date_to = request.GET.getlist("date_to")
    countries = request.GET.getlist("country")
    channels = request.GET.getlist("channel")
    systems = request.GET.getlist("os")

    group_by = request.GET.getlist("group_by")
    sum_on = request.GET.getlist("sum_on")

    sort_by = request.GET.get("sort_by")
    order_type = request.GET.get("order_type")

    ctx = dict()
    ctx["status"] = "OK"
    if order_type.lower() not in ["asc", "desc"]:
        ctx["status"] = "ERROR"
        ctx["message"] = "Invalid order type"
        return JsonResponse(ctx)

    with connections['adjust_mysql'].cursor() as cursor:
        sql_query = build_query(
            date_from=date_from,
            date_to=date_to,
            countries=countries,
            channels=channels,
            systems=systems,
            group_by=group_by,
            sum_on=sum_on,
            sort_by=sort_by,
            order_type=order_type
        )
        cursor.execute(sql_query)
        ctx["data"] = list()
        for i in cursor.fetchall():
            ctx["data"].append(dict(zip((group_by + sum_on + ['CPI']), i)))
    return JsonResponse(ctx)
