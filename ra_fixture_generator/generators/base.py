# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
import random
from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Union

from faker import Faker
from ramodels.mo import OpenValidity
from ramodels.mo import Validity


class BaseGenerator:
    def __init__(self) -> None:
        self.fake = Faker("da_DK")

        self.now = datetime.now().date()
        self.yesterday = self.now - timedelta(days=1)
        self.in_three_years = self.now + timedelta(days=365 * 3)

        self.past_start = self.now - timedelta(days=365 * 25)
        self.past_end = self.now - timedelta(days=7)
        # Ensure the generated data makes sense for at least two years, in case someone
        # gets the brilliant idea to use the same fixture data for like half a decade...
        self.future_start = self.now + timedelta(days=365 * 2)
        self.future_end = self.now + timedelta(days=365 * 15)

    def validity(
        self,
        *intervals: OpenValidity,
        allow_open_from: bool = True,
        allow_open_to: bool = True,
        force_open_to: bool = True,
    ) -> Union[Validity, OpenValidity]:
        #         T      T+3y
        # |<-->|                          : max_from < min_to < now
        # |<-----><-->|                   : max_from < now < min_to < now + three_years
        # |<----->--------<---->|         : max_from < now < now + three_years < min_to
        #           |<->|                 : now < max_from < min_to < now + three_years
        #           |<----><--->|         : now < max_from < now + three_years < min_to
        #                     |<------>|  : now + three_years < max_from < min_to
        from_dates = [i.from_date.date() for i in intervals if i.from_date is not None]
        to_dates = [i.to_date.date() for i in intervals if i.to_date is not None]

        max_from_dates = max(from_dates, default=self.past_start)
        min_to_dates = min(to_dates, default=self.future_end)

        # If from/to_dates is falsy, all dates must be None, i.e. an open interval, in
        # which case the generated validity will be open with 40%/60% probability.
        if allow_open_from and not from_dates and random.random() < 0.4:
            from_date = None
        else:
            if max_from_dates < min_to_dates < self.now:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=min_to_dates,
                )
            elif max_from_dates < self.yesterday < min_to_dates < self.in_three_years:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=self.yesterday,
                )
            elif max_from_dates < self.yesterday < self.in_three_years < min_to_dates:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=self.yesterday,
                )
            elif self.now < max_from_dates < min_to_dates < self.in_three_years:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=min_to_dates,
                )
            elif self.now < max_from_dates < self.in_three_years < min_to_dates:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=self.in_three_years,
                )
            elif self.in_three_years < max_from_dates < min_to_dates:
                from_date = self.fake.date_between_dates(
                    date_start=max_from_dates,
                    date_end=min_to_dates,
                )
            else:
                raise ValueError("Someone fucked up! Please don't git blame")

        if force_open_to or (allow_open_to and not to_dates and random.random() < 0.6):
            to_date = None
        else:
            if max_from_dates < min_to_dates < self.now:
                to_date = self.fake.date_between_dates(
                    date_start=from_date,
                    date_end=min_to_dates,
                )
            elif max_from_dates < self.now < min_to_dates < self.in_three_years:
                to_date = self.fake.date_between_dates(
                    date_start=self.now,
                    date_end=min_to_dates,
                )
            elif max_from_dates < self.now < self.in_three_years < min_to_dates:
                to_date = self.fake.date_between_dates(
                    date_start=self.in_three_years,
                    date_end=min_to_dates,
                )
            elif self.now < max_from_dates < min_to_dates < self.in_three_years:
                to_date = self.fake.date_between_dates(
                    date_start=from_date,
                    date_end=min_to_dates,
                )
            elif self.now < max_from_dates < self.in_three_years < min_to_dates:
                to_date = self.fake.date_between_dates(
                    date_start=self.in_three_years,
                    date_end=min_to_dates,
                )
            elif self.in_three_years < max_from_dates < min_to_dates:
                to_date = self.fake.date_between_dates(
                    date_start=from_date,
                    date_end=min_to_dates,
                )
            else:
                raise ValueError("Someone fucked up! Please don't git blame")

        validity_cls = OpenValidity if allow_open_from and allow_open_to else Validity

        if from_date is not None:
            assert all(from_date >= d for d in from_dates)
        if to_date is not None:
            assert all(to_date <= d for d in to_dates)

        return validity_cls(from_date=from_date, to_date=to_date)

    def historic_validity(
        self, *intervals: OpenValidity, **kwargs: Any
    ) -> OpenValidity:
        historic_validity = OpenValidity(
            from_date=None,
            to_date=self.past_end,
        )
        return self.validity(*intervals, historic_validity, **kwargs)

    def future_validity(self, *intervals: OpenValidity, **kwargs: Any) -> OpenValidity:
        future_validity = OpenValidity(
            from_date=self.future_start,
            to_date=None,
        )
        return self.validity(*intervals, future_validity, **kwargs)

    def random_validity(
        self, *intervals: OpenValidity, **kwargs: Any
    ) -> Union[Validity, OpenValidity]:
        # this is so bad, lol, but cba
        while True:
            try:
                validity_function = random.choices(
                    (self.validity, self.historic_validity, self.future_validity),
                    cum_weights=(70, 90, 100),
                )[0]
                return validity_function(*intervals, **kwargs)  # type: ignore[operator]
            except ValueError:
                # print("Brute-forcing solution instead of fixing code; hang on...")
                pass  # todo: probably fix
