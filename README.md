# COVID-19 Related Federal Compassionate Release

## Data Collection Strategy

The UCLA Law COVID-19 Behind Bars Data Project collected federal COVID-19 related compassionate release decisions and related metadata from PACER, and programatically classified many of the decisions as “granting” or “denying'' compassionate release.  Volunteers read through thousands of court decisions that could not be automatically classified. 

Because our data concerns the federal courts, it all ultimately comes from the federal courts’ electronic records system, PACER (Public Access to Court Electronic Information). However, we did not search PACER directly. 

We compiled our data using [CourtListener’s API service](https://www.courtlistener.com/api/) and by bringing in additional data from [Westlaw case law searches](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3801075) run by Victoria Finkle.

**Limitations**: CourtListener and WestLaw's PACER collections primarily consist of documents marked as “opinions” by federal courts, docket information produced through court RSS feeds, documents purchased by other users, and particular PACER documents the vendors have identified as useful. They are incredibly useful collections, but contain only a fraction of all PACER data. Thus, one limitation of our data is that our sources were incomplete; it does not contain judicial decisions that were not collected by the vendors we surveyed. 

The other limitation of our data is based on our search strategy. To identify compassionate release cases in CourtListener, we used key words (our exact search can be found here), which we searched for in the document or docket description. However, some courts may issue an order related to compassionate release without ever even using the word release. Therefore, our data may be underinclusive. 

Because a district court’s policies (in marking documents as “opinions”, in maintaining RSS feeds, and in formulating document descriptions) may influence whether our search strategy is effective, we have attempted to determine whether there are any districts over- or under-represented in our data.  

**Other sources**: 
Descriptive variables for the federal court jurisdictions, including chief judge, nominating president, term as chief judge, and district number, were sourced from [Homeland Infrastructure Foundation-Level Data](https://hifld-geoplatform.opendata.arcgis.com/datasets/geoplatform::us-district-court-jurisdictions/about). 

## Data Dictionary 

| Variable               | Description                                                                                                                    |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `case_name`          | Compassionate release court case name                                                                          |
| `docket_number`         | Case docket number                   |
| `date`                 | Date case data was last updated                                               |  
| `court_std`                | Standardized federal court name                                                                                           |
| `judge`                 | Federal judge name                                                                                                                |
| `granted_denied`               | Whether the petition for compassionate release was granted or denied                                                                                        |
| `doc_description`  | Document description                                                        |
| `doc_title`      | Document title                                                                            |
| `def_last_name`     | Defendant's last name                                                          |
| `nature_of_suit`         | Nature of suit                                                                             |
| `prosecutor_name`  | Prosecutor                                                      |
| `ucla_citation`      | Case citation created by the UCLA Law team                                                                        |
| `published_cite`     | Published citation                                               |
| `courtlistener_url`         | URL linked to a case on courtlistener.com                                                                             |
| `westlaw_url`   | URL linked to a case on westlaw.com                                       |
| `westlaw_cite`       | Citation for WestLaw                                                                  |
| `state_fips`        | State FIPS code for federal court location                                                           |
| `state`     | State name for federal court location                                                                      |
| `full_court_name` | Full federal court name                                                       |
| `chief_judge`     | Chief judge                                                            |
| `nominating`         | Nominating president for chief judge of federal court                                                                               |
| `term_as_ch`     | Term as chief judge                                                  |
| `district_n` | District number for federal court                                                   |

## License 

Our data is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/). That means that you must give appropriate credit, provide a link to the license, and indicate if changes were made. You may not use our work for commercial purposes, which means anything primarily intended for or directed toward commercial advantage or monetary compensation. 

## Contributors 

For questions or feedback about the data, please reach out to Hope Johnson (johnsonh@law.ucla.edu) and Rebecca Fordon (fordon@law.ucla.edu). 

Additional information on compassionate release cases was provided by Victoria Finkle.