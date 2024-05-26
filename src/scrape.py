import datetime
import random
import time
from typing import Any, Callable, Dict, List, Union

import pandas as pd
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def wait():
	# wait randomly between 10 seconds
	time.sleep(random.randint(1, 10))


def get_driver(
	headless: bool = False,
	disable_automation: bool = False,
):
	options = webdriver.FirefoxOptions()
	# options.add_argument(f"user-agent={user_agent}")
	if headless:
		options.add_argument("--headless")

	return webdriver.Firefox(options=options)


def get_children(parent: Union[WebElement, WebDriver], children_class_name: str) -> List[WebElement]:
	return parent.find_elements(By.CLASS_NAME, children_class_name)


def get_events(driver: WebDriver | WebElement) -> List[WebElement]:
	return get_children(driver, "eventHolder")


def process_date(extracted_date: str):
	if extracted_date.lower() == "today":
		return datetime.datetime.now().strftime("%Y-%m-%d")
	elif extracted_date.lower() == "tomorrow":
		return (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
	else:
		return extracted_date


def get_event_date(driver: WebDriver, event: WebElement):
	parent_panel = find_parent_element(driver=driver, event=event, get_elements=get_panels)
	if parent_panel is not None:
		event_date = process_date(get_panel_date(panel=parent_panel))
	else:
		print("No parent panel found")
		event_date = None
	return event_date


def get_event_info(driver: WebDriver, event: WebElement) -> Dict[str, Any]:
	event_time = event.find_element(By.CLASS_NAME, "oneLineDateTime").text
	event_date = get_event_date(driver, event)
	home_team = event.find_element(By.CLASS_NAME, "teamNameHome").text
	away_team = event.find_element(By.CLASS_NAME, "teamNameAway").text
	logger.info(f"Processing {home_team} vs {away_team}")
	try:
		home_odds = event.find_elements(By.CLASS_NAME, "oddsDisplay")[0].text
		away_odds = event.find_elements(By.CLASS_NAME, "oddsDisplay")[1].text

	except Exception as e:
		print(e)
		home_odds = None
		away_odds = None

	return {
		"event_date": event_date,
		"event_time": event_time,
		"home_team": home_team,
		"away_team": away_team,
		"home_odds": home_odds,
		"away_odds": away_odds,
		"draw_odds": None,
	}


def get_panels(driver: WebDriver) -> List[WebElement]:
	BETWAY_PANEL_CLASS = "collapsablePanel"
	panels = driver.find_elements(By.CLASS_NAME, BETWAY_PANEL_CLASS)
	return panels


def get_headers(driver: WebDriver) -> List[WebElement]:
	BETWAY_HEADER_CLASS = "alternativeHeaderBackground"
	headers = driver.find_elements(By.CLASS_NAME, BETWAY_HEADER_CLASS)
	return headers


def is_element_ancestor(element: WebElement, event: WebElement):
	element_descendants = get_events(element)
	return event.id in [o.id for o in element_descendants]


def find_parent_element(driver: WebDriver, event: WebElement, get_elements: Callable) -> WebElement | None:
	elements = get_elements(driver)
	result = None
	for element in elements:
		if is_element_ancestor(element, event):
			result = element
	return result


def get_panel_date(panel: WebElement) -> str:
	return panel.find_element(By.CLASS_NAME, "titleText").text


def league_from_url(url: str) -> str:
	return url.split("/")[-3]


def country_from_url(url: str) -> str:
	return url.split("/")[-1]


def sport_from_url(url: str) -> str:
	return url.split("/")[-2]


def get_data(url: str) -> pd.DataFrame:
	driver = get_driver()
	driver.get(url)
	wait()
	events = get_events(driver)
	wait()
	data = []
	for event in events:
		try:
			event_info = get_event_info(driver, event)
			data.append(event_info)
		except Exception as e:
			logger.exception(e)

	driver.quit()
	source = "betway"

	return (
		pd.DataFrame(data)
		.assign(
			url=url,
			source=source,
			country=country_from_url(url),
			sport=sport_from_url(url),
			league=league_from_url(url),
		)
		.loc[
			:,
			[
				"url",
				"source",
				"country",
				"sport",
				"league",
				"event_date",
				"event_time",
				"home_team",
				"away_team",
				"home_odds",
				"away_odds",
				"draw_odds",
			],
		]
	)
