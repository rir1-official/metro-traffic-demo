import json
import random
from datetime import datetime, timedelta

import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from redis.exceptions import RedisError


REDIS_CLIENT = redis.Redis(
    host="127.0.0.1",
    port=6379,
    db=0,
    decode_responses=True,
)

AREA_BASELINES = {
    "站台A区": 156,
    "站台B区": 132,
    "换乘通道": 186,
    "闸机口": 118,
    "站厅中央": 144,
    "扶梯口": 98,
}


def build_history(base_value):
    now = datetime.now()
    history = []
    predicted = []

    for i in range(6):
        point_time = now - timedelta(minutes=(25 - i * 5))
        value = max(50, base_value - 26 + i * random.randint(6, 11) + random.randint(-6, 6))
        history.append(
            {
                "time": point_time.strftime("%H:%M"),
                "value": value,
            }
        )

    forecast_seed = history[-1]["value"]
    for i in range(1, 7):
        point_time = now + timedelta(minutes=i * 5)
        delta = random.randint(3, 10)
        value = forecast_seed + i * delta + random.randint(-4, 5)
        predicted.append(
            {
                "time": point_time.strftime("%H:%M"),
                "value": value,
            }
        )

    return history, predicted


def build_area_status(current_area, current_count):
    statuses = []
    for name, baseline in AREA_BASELINES.items():
        count = current_count if name == current_area else max(40, baseline + random.randint(-26, 34))
        risk_level = "绿色正常"
        if count >= 220:
            risk_level = "红色预警"
        elif count >= 180:
            risk_level = "橙色预警"
        elif count >= 130:
            risk_level = "黄色预警"

        statuses.append(
            {
                "name": name,
                "count": count,
                "risk_level": risk_level,
            }
        )

    return statuses


def build_alerts(area_statuses):
    alerts = []
    now = datetime.now()
    for index, area in enumerate(sorted(area_statuses, key=lambda item: item["count"], reverse=True)[:4]):
        if area["risk_level"] == "绿色正常":
            continue

        alert_type = "客流密度过高"
        if area["name"] == "换乘通道":
            alert_type = "通道局部滞留"
        elif area["name"] == "闸机口":
            alert_type = "进站排队堆积"
        elif area["name"] == "扶梯口":
            alert_type = "扶梯口拥挤"

        suggestion = "建议安排站务人员进行引导"
        if area["risk_level"] == "红色预警":
            suggestion = "建议立即启动分流与限流预案"
        elif area["risk_level"] == "橙色预警":
            suggestion = "建议提前发布分流广播并加强值守"

        alerts.append(
            {
                "time": (now - timedelta(minutes=index * 3)).strftime("%H:%M:%S"),
                "area": area["name"],
                "type": alert_type,
                "level": area["risk_level"],
                "suggestion": suggestion,
            }
        )

    if not alerts:
        alerts.append(
            {
                "time": now.strftime("%H:%M:%S"),
                "area": "全站",
                "type": "运行状态正常",
                "level": "绿色正常",
                "suggestion": "当前无需额外处置",
            }
        )

    return alerts


def build_payload(area=None, current_count=None):
    selected_area = area or random.choice(list(AREA_BASELINES.keys()))
    current_value = current_count if current_count is not None else random.randint(96, 238)
    predicted_30m = current_value + random.randint(12, 48)

    risk_level = "绿色正常"
    if current_value >= 220:
        risk_level = "红色预警"
    elif current_value >= 180:
        risk_level = "橙色预警"
    elif current_value >= 130:
        risk_level = "黄色预警"

    history, predicted_series = build_history(current_value)
    area_statuses = build_area_status(selected_area, current_value)
    alerts = build_alerts(area_statuses)
    high_risk_areas = sum(1 for item in area_statuses if item["risk_level"] != "绿色正常")

    return {
        "type": "flow_update",
        "station": "厦门地铁演示站",
        "line": "1号线",
        "area": selected_area,
        "current_count": current_value,
        "predicted_30m": predicted_30m,
        "risk_level": risk_level,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "today_total": random.randint(18200, 25600),
        "high_risk_areas": high_risk_areas,
        "status_message": "客流状态平稳，系统持续监测中" if risk_level == "绿色正常" else "检测到重点区域压力上升，请关注预警信息",
        "history_series": history,
        "predicted_series": predicted_series,
        "area_statuses": area_statuses,
        "alerts": alerts,
    }


def _default_payload():
    return build_payload(area="站台A区", current_count=148)


def index(request):
    try:
        raw = REDIS_CLIENT.get("metro:latest_flow")
    except RedisError:
        raw = None

    latest = json.loads(raw) if raw else _default_payload()
    return render(request, "demo/index.html", {"initial_data": json.dumps(latest, ensure_ascii=False)})


@csrf_exempt
def mock_update(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed."}, status=405)

    payload = build_payload()

    try:
        REDIS_CLIENT.set("metro:latest_flow", json.dumps(payload, ensure_ascii=False))
    except RedisError:
        pass

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "metro_flow",
        {
            "type": "flow_message",
            "payload": payload,
        },
    )

    return JsonResponse({"message": "mock update sent", "data": payload}, json_dumps_params={"ensure_ascii": False})
