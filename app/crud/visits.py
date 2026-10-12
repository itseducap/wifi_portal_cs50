from sqlalchemy import select, and_, or_ , func, JSON, insert
from app.models.lead import Lead
from app.models.visit import Visit
from datetime import datetime, timedelta, timezone, time
from zoneinfo import ZoneInfo

# AI made the constants
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
UTC = timezone.utc

#TODO: Replace the hardcoded user_id for the variable of the currrent user id when login feature is implemented
def lead_visits_query(lead_id: int, user_id: int):
    stmt = (select(
        Visit.created_at,
        Visit.ssid
    ).join(Lead)
    .where(
        Lead.id == lead_id,
        Lead.user_id == user_id
    )
)
    return stmt

def count_total_visits(user_id: int):
    stmt = select(func.count(Visit.id)).join(Lead).where(Lead.user_id == user_id)
    return stmt

def count_visits_today(user_id: int):
    # AI helped with timezone conversion
    now_local = datetime.now(SAO_PAULO)
    today_start_local= datetime.combine(now_local.date(), time.min, tzinfo= SAO_PAULO)
    today_start_utc = today_start_local.astimezone(UTC).replace(tzinfo=None)
    now_utc = now_local.astimezone(UTC).replace(tzinfo=None)
    stmt = select(func.count(Visit.id)).join(Lead).where(
        and_(
            Lead.user_id == user_id,
            Visit.created_at >= today_start_utc,
            Visit.created_at <= now_utc
        )
    )
    return stmt




def count_visits_week(user_id: int):
    # AI helped me with timedelta and timezone conversion
    now_local = datetime.now(SAO_PAULO)
    now_utc = now_local.astimezone(UTC).replace(tzinfo=None)
    today_start_local= datetime.combine(now_local.date(), time.min, tzinfo= SAO_PAULO)
    start_week_local = (today_start_local - timedelta(days=now_local.weekday()))
    start_week_utc = start_week_local.astimezone(UTC).replace(tzinfo=None)
    stmt = select(func.count(Visit.id)).join(Lead).where(
        and_(
            Lead.user_id == user_id,
            Visit.created_at >= start_week_utc,
            Visit.created_at <= now_utc
        )
    )
    return stmt
