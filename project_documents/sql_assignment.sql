--Create Tables
IF Object_ID('dbo.Trades') IS NULL
CREATE table dbo.Trades (
  TradeNumber nvarchar(100) NOT NULL, 
  MatchId nvarchar(100) NOT NULL, 
  Volume int NOT NULL, 
  Price decimal(5,2) NOT NULL, 
  Direction nvarchar(100) NOT NULL
);

IF Object_ID('dbo.Deals') IS NULL
CREATE TABLE dbo.Deals
(
  MatchId nvarchar(100) NOT NULL,
  MatchedData date NOT NULL,
  TraderCode nvarchar(100) NOT NULL
);

IF Object_ID('dbo.Traders') IS NULL
CREATE TABLE dbo.Traders
(
  TraderCode nvarchar(100) NOT NULL,
  TraderName nvarchar(100) NOT NULL,
  TraderTarget nvarchar(100) NOT NULL
);

--Clean Tables in case there might be data
TRUNCATE TABLE dbo.Trades
TRUNCATE TABLE dbo.Deals
TRUNCATE TABLE dbo.Traders

--Insert data into the Tables
Insert into dbo.Trades (tradenumber, matchid, volume, price, direction)
SELECT 'T001', 'M1',	1000,	0.10,	'Buy' 	UNION ALL
SELECT 'T002', 'M2',	100,	0.12,	'Buy'	UNION ALL
SELECT 'T003', 'M3',	400,	0.11,	'Buy'	UNION ALL
SELECT 'T004', 'M4',	1500,	0.09,	'Buy'	UNION ALL
SELECT 'T005', 'M5',	600,	0.13,	'Buy'	UNION ALL
SELECT 'T006', 'M3',	400,	0.15,	'Sell'	UNION ALL
SELECT 'T007', 'M2',	100,	0.16,	'Sell'	UNION ALL
SELECT 'T008', 'M5',	600,	0.14,	'Sell'	UNION ALL
SELECT 'T009', 'M4',	1500,	0.12,	'Sell'	UNION ALL
SELECT 'T010', 'M1',	1000,	0.12,	'Sell';
            
Insert into dbo.Deals (MatchId, MatchedData,  TraderCode) 
SELECT 'M1', 	'20230401',	'RA' UNION ALL
SELECT 'M2', 	'20230401',	'AB' UNION ALL
SELECT 'M3', 	'20230403',	'CM' UNION ALL
SELECT 'M4', 	'20230404',	'AB' UNION ALL
SELECT 'M5', 	'20230406',	'RA';

Insert into dbo.Traders
SELECT 'AB', 'Arber',       40 UNION ALL
SELECT 'RA', 'Riccardo',	20 UNION ALL
SELECT 'CM', 'Cornelius',	20;


--Drop Tables if they exist
--IF Object_ID('dbo.Trades') IS NOT NULL DROP TABLE dbo.Trades
--IF Object_ID('dbo.Deals') IS NOT NULL DROP TABLE dbo.Deals
--IF Object_ID('dbo.Traders') IS NOT  NULL DROP TABLE dbo.Traders


/*********************Requirements*****************************/

--1.	Calculate the total sold volume.

--2.	Calculate the weighted average buy price.

--3.	Calculate the profit per deal.

--4.	Identify the traders who reached their targets.

--5		Identify the trader who did the second most profit.

--6.	Calculate the total profit per every day of the period between the 1st and the 10th of April, both included.

--7.	Calculate the cumulative profit for the period between the first and the 10th of April, both included.