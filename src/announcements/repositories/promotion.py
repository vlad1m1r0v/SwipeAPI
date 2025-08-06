from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from src.apartments.models import Apartment

from src.user.models import User, Balance
from src.user.exceptions import NotEnoughMoneyException

from src.announcements.models import Announcement, Promotion
from src.announcements.constants import (
    HIGHLIGHT_PRICE,
    PHRASE_PRICE,
    BIG_ADVERTISEMENT_PRICE,
    BOOST_ADVERTISEMENT_PRICE,
)


class AnnouncementPromotionRepository(SQLAlchemyAsyncRepository[Promotion]):
    model_type = Promotion

    async def update_promotion(self, promotion_id: int, data: dict) -> Promotion:
        stmt = (
            select(Promotion)
            .where(Promotion.id == promotion_id)
            .options(
                joinedload(Promotion.announcement)
                .joinedload(Announcement.apartment)
                .joinedload(Apartment.user)
                .joinedload(User.balance)
            )
        )

        result = await self.session.execute(stmt)
        row: Promotion = result.scalar_one_or_none()

        updated_values: dict = {}
        total_price: int = 0

        now = datetime.now(timezone.utc)

        def get_new_expiry(current_expiry):
            if current_expiry and current_expiry.tzinfo is not None:
                current_expiry = current_expiry.astimezone(timezone.utc).replace(
                    tzinfo=None
                )

            now_naive = now.replace(tzinfo=None)

            if current_expiry:
                return max(current_expiry, now_naive) + relativedelta(months=1)

            return now_naive + relativedelta(months=1)

        if highlight_colour := data.get("highlight_colour"):
            new_expiry_date = get_new_expiry(row.highlight_expiry_date)
            updated_values["highlight_colour"] = highlight_colour
            updated_values["highlight_expiry_date"] = new_expiry_date
            total_price += HIGHLIGHT_PRICE

        if phrase := data.get("phrase"):
            new_expiry_date = get_new_expiry(row.phrase_expiry_date)
            updated_values["phrase"] = phrase
            updated_values["phrase_expiry_date"] = new_expiry_date
            total_price += PHRASE_PRICE

        if data.get("is_boosted"):
            new_expiry_date = get_new_expiry(row.boost_expiry_date)
            updated_values["boost_expiry_date"] = new_expiry_date
            total_price += BOOST_ADVERTISEMENT_PRICE

        if data.get("is_big_advert"):
            new_expiry_date = get_new_expiry(row.big_advert_expiry_date)
            updated_values["big_advert_expiry_date"] = new_expiry_date
            total_price += BIG_ADVERTISEMENT_PRICE

        if row.announcement.apartment.user.balance.value < total_price:
            raise NotEnoughMoneyException()

        stmt = (
            update(Promotion)
            .where(Promotion.id == promotion_id)
            .values(**updated_values)
            .returning(Promotion)
        )

        result = await self.session.execute(stmt)
        promotion: Promotion = result.scalar_one_or_none()

        balance_id = row.announcement.apartment.user.balance.id
        new_balance_value = row.announcement.apartment.user.balance.value - total_price

        stmt = (
            update(Balance)
            .where(Balance.id == balance_id)
            .values(value=new_balance_value)
        )
        await self.session.execute(stmt)

        return promotion
