# ACT Commodities – Business Engineer Technical Assessment

We would like to see your thought process when analysing an unknown dataset and when writing SQL code to transform data into insights.

1.  **SQL skills**

Analyse the following dataset, then create SQL queries to get the information requested below. You can use the attached script and complete the assessment online using [https://sqliteonline.com/](https://sqliteonline.com/) by using MS SQL if you do not have it installed in your laptop.

[sql_assignment.sql](<../../../../../OneDrive/Interview Assesments/Act Group - Senior BI Engineer/SQL Assignment.sql>)

Trades:

| Tradenumber | MatchId | Volume | Price | Direction |
| --- | --- | --- | --- | --- |
| T001 | M1 | 1000 | 0.10 | Buy |
| T002 | M2 | 100 | 0.12 | Buy |
| T003 | M3 | 400 | 0.11 | Buy |
| T004 | M4 | 1500 | 0.09 | Buy |
| T005 | M5 | 600 | 0.13 | Buy |
| T006 | M3 | 400 | 0.15 | Sell |
| T007 | M2 | 100 | 0.16 | Sell |
| T008 | M5 | 600 | 0.14 | Sell |
| T009 | M4 | 1500 | 0.12 | Sell |
| T010 | M1 | 1000 | 0.12 | Sell |

Traders:

| TraderCode | TraderName | TraderTarget |
| --- | --- | --- |
| AB | Arber | 40 |
| RA | Riccardo | 20 |
| CM | Cornelius | 20 |

Deals:

| MatchId | MatchedDate | TraderCode |
| --- | --- | --- |
| M1 | 20250401 | RA |
| M2 | 20250401 | AB |
| M3 | 20250403 | CM |
| M4 | 20250404 | AB |
| M5 | 20250406 | RA |

    1. Calculate the total sold volume.  
    2. Calculate the weighted average buy price.  
    3. Calculate the profit per deal.  
    4. Identify the traders who reached their targets.  
    5. Identify the trader who did the second most profit.  
    6. Calculate the total profit per every day of the period between the 1st and the 10th of April, both included.  
    7. Calculate the cumulative profit for the period between the first and the 10th of April, both included.
   
2. **Data modelling**

Given the dataset named ‘Trading dataset’ attached in the email remodel the data by creating dimension and fact tables. The dimension(s) should be of SCD type 2 and the fact(s) should be a periodical snapshot fact.

This exercise aims to test the dimensional modelling skills. The output of the exercise should be a database diagram including:

*   Dimension(s) and Fact(s) tables
*   Attributes in each table
*   Primary Keys, Foreign Keys
*   Relationships between tables

[trading_dataset.xlsx](<../../../../../OneDrive/Interview Assesments/Act Group - Senior BI Engineer/Trading Dataset.xlsx>)

3.  **Report Design**

Visualise the data provided in the Trading dataset using Power BI. Create a Power BI Report named ‘Performance Overview’ to show different aspects of the data. Use the below attached theme in the report.

This exercise aims to test the data analysis and report design skills. The output of the exercise should be the .pbix file representing the report.

[act_power_bi_theme](<../../../../../OneDrive/Interview Assesments/Act Group - Senior BI Engineer/ACT_BI_Theme_Background_1.json>)