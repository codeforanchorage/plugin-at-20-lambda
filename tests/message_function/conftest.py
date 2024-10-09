# flake8: noqa 501

import pytest


@pytest.fixture
def weather_xml():
    return '''
    <dwml xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="https://digital.weather.gov/xml/schema/DWML.xsd">
        <head>
            <product srsName="WGS 1984" concise-name="time-series" operational-mode="official">
                <title>NOAA's National Weather Service Forecast Data</title>
            </product>
        </head>
        <data>
            <location>
                <location-key>point1</location-key>
                <point latitude="61.22" longitude="-149.85"/>
            </location>
            <location>
                <location-key>point2</location-key>
                <point latitude="61.16" longitude="-149.99"/>
            </location>
            <moreWeatherInformation applicable-location="point1">
                http://forecast.weather.gov/MapClick.php?textField1=61.22&amp;textField2=-149.85
            </moreWeatherInformation>
            <moreWeatherInformation applicable-location="point2">
                http://forecast.weather.gov/MapClick.php?textField1=61.16&amp;textField2=-149.99
            </moreWeatherInformation>

            <time-layout time-coordinate="local" summarization="none">
                <layout-key>k-p3h-n2-1</layout-key>
                <start-valid-time>2024-10-07T01:00:00-08:00</start-valid-time>
                <start-valid-time>2024-10-07T04:00:00-08:00</start-valid-time>
            </time-layout>
            <parameters applicable-location="point1">
                <temperature type="hourly" units="Fahrenheit" time-layout="k-p3h-n2-1">
                    <name>Temperature</name>
                    <value>31</value>
                    <value>39</value>
                </temperature>
            </parameters>
            <parameters applicable-location="point2">
                <temperature type="hourly" units="Fahrenheit" time-layout="k-p3h-n2-1">
                    <name>Temperature</name>
                    <value>31</value>
                    <value>29</value>
                </temperature>
            </parameters>
            <parameters applicable-location="point2">
                <temperature type="hourly" units="Fahrenheit" time-layout="k-p3h-n2-1">
                    <name>Temperature</name>
                    <value></value>
                    <value></value>
                </temperature>
            </parameters>
        </data>
    </dwml>
'''
