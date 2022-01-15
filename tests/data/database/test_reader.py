import numpy as np
from cmt_website.data.database.models import Base
from cmt_website.data.database.reader import DBReader
from hypothesis import given
from hypothesis.extra.numpy import datetime64_dtypes
from hypothesis.extra.pandas import column, data_frames
from hypothesis.strategies import datetimes, timezones
from sqlalchemy.engine.create import create_engine


def temp_memory_db(future=False):
    engine = create_engine("sqlite:///:memory:", future=future)
    Base.metadata.create_all(engine)
    return engine


@given(
    data_frames(
        [
            column(name="time", elements=datetimes(timezones=timezones()), unique=True),
            column(name="temperature", dtype=float),
            column(name="humidity", dtype=float),
            column(name="wind speed", dtype=float),
            column(name="wind direction", dtype=float),
        ]
    ),
)
def test_read_weather(weather):
    engine = temp_memory_db()
    with engine.begin() as connection:
        weather.to_sql(
            "weather",
            con=connection,
            if_exists="append",
            index=False,
            index_label="time",
        )

    reader = DBReader(engine=engine, table="weather")
    read_data = reader.read()

    assert len(read_data) == len(weather)
    for col in read_data.columns:
        assert np.array_equal(
            read_data[col].values, weather[col].values, equal_nan=True
        )


@given(
    data_frames(
        [
            column(name="time", elements=datetimes(timezones=timezones()), unique=True),
            column(name="brightness", dtype=float),
        ]
    )
)
def test_read_sqm(sqm):
    engine = temp_memory_db()
    with engine.begin() as connection:
        sqm.to_sql(
            "sqm", con=connection, if_exists="append", index=False, index_label="time"
        )

    reader = DBReader(engine=engine, table="sqm")
    read_data = reader.read()
    assert len(read_data) == len(sqm)
    for col in read_data.columns:
        assert np.array_equal(read_data[col].values, sqm[col].values, equal_nan=True)
