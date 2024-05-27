import uuid

from sqlalchemy import DATE, TIMESTAMP, UUID, Column, String, text

from src.database.base import Base


class ScrapedData(Base):
	__tablename__ = "scraped_data"

	# create the following columns:
	# id, source, extracted_at, event_date, event_time, home_team, away_team, sport, country, home_odds, away_odds, draw_odds
	extraction_id = Column(UUID, primary_key=True, default=uuid.uuid4)
	url = Column(String(255), nullable=False)
	source = Column(String(255), nullable=False)
	sport = Column(String(255), nullable=False)
	country = Column(String(255), nullable=True)
	league = Column(String(255), nullable=True)
	event_date = Column(DATE, nullable=True)
	event_time = Column(String(255), nullable=True)
	home_team = Column(String(255), nullable=True)
	away_team = Column(String(255), nullable=True)
	home_odds = Column(String(255), nullable=True)
	away_odds = Column(String(255), nullable=True)
	draw_odds = Column(String(255), nullable=True)
	extracted_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
