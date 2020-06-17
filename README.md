# World view of the risks associated with COVID-19

## Objective
This project provides a COVID-19 score at country-level, through a World Map.
The map representation gives a clear indication of the countries most at risk.

## Modelisation
For each country, a set of propagation factors are assessed (a score is attributed for each factor).
Then, an impact weight is associated to each factor.
A combined Risk score can then be extrapolated, for each country.
The generated World Map representation output displays the results in a visual format.

## Propagation factors
The factors taken into account are based on scientific litterature and public Health reports.
Such factors cover domains such as Health, Transport, Economic Quality, Education, Governance, Infrastructure, Social Capital up to Living Conditions.
The full list of factors is listed in the file *Data/world_data_XX_XX_XXXX--list_country_properties.json'*.
Additional factors can be added to the analysis if relevant.

## Sources for impact factors data
The data in this project is built from multiple publicly available reports:
* the World Health Organization
* the Legatum Prosperity Report
* the World Bank
* the Central Intelligence Agency

## Configuration
The output risk representation depends on the selected weighting of input parameters.
It is therefore essential to tune them relevantly.
A proposition of ponderation is provided in this project. Adjustments to weights can be made based on scientific knowledge to better model the Propagation Risks.
To fine-tune those weights, update the file *Data/world_data_XX_XX_XXXX--list_country_properties.json'*


## Credit
This work is the result of a collaboration between Stanwell Consulting & Handicap International

## Version
1.0 - 17/06/2020
