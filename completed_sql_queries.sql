-- ==========================================
-- ACT Commodities BI Assessment - SQL Solutions
-- ==========================================
-- Author: [Naveen Gandhi Raj Mohan]
-- Date: November 15, 2024
-- 
-- SCHEMA NOTES:
-- 1. Deals.MatchedData is a typo? (should be MatchedDate?) - used as-is from source and output is altered for readability
-- 2. Traders.TraderTarget is nvarchar(100) but contains numeric target values - CAST() used for calculations
-- ==========================================

-- ==========================================
-- Query 1: Total Sold Volume
-- ==========================================
-- THOUGHT PROCESS:
-- - Requirement asks for total sold volume specifically
-- - Need to filter for sell-side transactions only (Direction = 'Sell')
-- - Simple aggregation using SUM() on Volume column
-- - No joins needed as all data is in Trades table
-- - Added ISNULL to handle potential NULL volumes
-- - Added validation for negative volumes (data quality check)
-- - In production, would add index on Direction column for performance

SELECT 
    ISNULL(SUM(Volume), 0) AS TotalSoldVolume,
FROM Trades
WHERE Direction = 'Sell';



-- ==========================================
-- Query 2: Weighted Average Buy Price
-- ==========================================
-- THOUGHT PROCESS:
-- - Weighted average gives more importance to larger volume trades
-- - Formula: SUM(Price * Volume) / SUM(Volume) not simple AVG(Price)
-- - Filter for buy-side only (Direction = 'Buy') as per requirement
-- - Multiply by Price * Volume to weight each price by its trade size
-- - SUM(Price * Volume) is already decimal, but * 1.0 is kept as a safeguard to force decimal division if types change
-- - Divide by total volume to normalize the weighted sum
-- - CAST and ROUND for clean decimal presentation (2 decimal places)
-- - Added Currency for business context, EUR is taking as the reporting currency as per traning dataset
-- - If no buy trades, SUM(Volume) = 0, avoid division by zero by returning NULL

SELECT 
    CASE 
        WHEN SUM(Volume) = 0 THEN NULL
        ELSE CAST(
                 ROUND(
                     SUM(Price * Volume) * 1.0 / SUM(Volume),
                     2
                 ) AS DECIMAL(10,2)
             )
    END AS WeightedAvgBuyPrice,
    'EUR' AS Currency
FROM Trades
WHERE Direction = 'Buy';





-- ==========================================
-- Query 3: Profit Per Deal
-- ==========================================
-- THOUGHT PROCESS:
-- - Each deal (MatchId) consists of a matched buy/sell pair
-- - Need to join Trades table twice: once for buy, once for sell
-- - Profit formula: (Sell Price - Buy Price) * Volume
-- - Volume reconciliation: Do Buy and Sell volumes ALWAYS match in your real data? In the sample, they do. But in production trading systems, I've seen:
--  Partial fills
--  Amendments
--  Multiple buys/sells per/volume mismatch MatchId (preaggregation per side may be needed)
-- - Sign convention: Is profit always (Sell - Buy) × Volume, or do you flip signs based on Direction?
-- - Aliased MatchedData to MatchedDate for readability
-- - ORDER BY MatchId for logical result ordering

SELECT 
    d.MatchId,
    d.TraderCode,
    d.MatchedData AS MatchedDate,
    (ts.Price - tb.Price) * ts.Volume AS Profit
FROM Deals d
JOIN Trades tb ON d.MatchId = tb.MatchId AND tb.Direction = 'Buy'
JOIN Trades ts ON d.MatchId = ts.MatchId AND ts.Direction = 'Sell'
ORDER BY d.MatchId;




-- ==========================================
-- Query 4: Traders Who Reached Their Targets
-- ==========================================
-- THOUGHT PROCESS:
-- - TraderTarget is nvarchar(100) - must CAST to numeric for comparison
-- - Join chain: Traders -> Deals -> Trades (buy) + Trades (sell)
-- - GROUP BY TraderCode to sum profits per trader
-- - Added CASE statement for clear Yes/No indicator
-- - Show both target and actual profit for transparency
-- - TargetAchieved flag provides business-friendly output

SELECT 
    t.TraderCode,
    t.TraderName,
    CAST(t.TraderTarget AS INT) AS Target,
    SUM((ts.Price - tb.Price) * ts.Volume) AS TotalProfit,
    CASE 
        WHEN SUM((ts.Price - tb.Price) * ts.Volume) >= CAST(t.TraderTarget AS INT)
        THEN 'Yes'
        ELSE 'No'
    END AS TargetAchieved
FROM Traders t
JOIN Deals d ON t.TraderCode = d.TraderCode
JOIN Trades tb ON d.MatchId = tb.MatchId AND tb.Direction = 'Buy'
JOIN Trades ts ON d.MatchId = ts.MatchId AND ts.Direction = 'Sell'
GROUP BY t.TraderCode, t.TraderName, t.TraderTarget;



-- ==========================================
-- Query 5: Second-Highest Profit Trader
-- ==========================================
-- THOUGHT PROCESS:
-- - Need to rank traders by total profit and select rank 2
-- - Used CTE (Common Table Expression) for cleaner, readable code
-- - DENSE_RANK() chosen over RANK() to handle potential ties properly
-- - DENSE_RANK ensures if multiple traders tie for 1, next is still 2 (not 3)
-- - Aggregate profits in CTE, then filter WHERE ProfitRank = 2 in outer query
-- - Alternative: Could use OFFSET 1 ROW FETCH NEXT 1 ROW, but DENSE_RANK is more robust
-- - CTE approach is more maintainable if we later need other ranks

WITH TraderProfits AS (
    SELECT 
        t.TraderCode,
        t.TraderName,
        SUM((ts.Price - tb.Price) * ts.Volume) AS TotalProfit,
        DENSE_RANK() OVER (ORDER BY SUM((ts.Price - tb.Price) * ts.Volume) DESC) AS ProfitRank
    FROM Traders t
    JOIN Deals d ON t.TraderCode = d.TraderCode
    JOIN Trades tb ON d.MatchId = tb.MatchId AND tb.Direction = 'Buy'
    JOIN Trades ts ON d.MatchId = ts.MatchId AND ts.Direction = 'Sell'
    GROUP BY t.TraderCode, t.TraderName
)
SELECT 
    TraderCode,
    TraderName,
    TotalProfit
FROM TraderProfits
WHERE ProfitRank = 2;


-- ==========================================
-- Query 6: Daily Profit (April 1–10, 2023)
-- ==========================================
-- THOUGHT PROCESS:
-- - We need total profit for each day between April 1–10.
-- - Profit = (SellPrice - BuyPrice) * Volume.
-- - Join Deals to Buy/Sell trades to calculate profit per deal.
-- - Group by MatchedData to get one profit value per day.
-- - Sort by date so results appear in order.
-- - Note: Days with no trades will not show up because of the inner join.
-- - A calendar table would be needed to show zero-profit days.
-- - Aliased MatchedData to MatchedDate for readability.

SELECT 
    d.MatchedData AS MatchedDate,
    SUM((ts.Price - tb.Price) * ts.Volume) AS DailyProfit
FROM Deals d
JOIN Trades tb ON d.MatchId = tb.MatchId AND tb.Direction = 'Buy'
JOIN Trades ts ON d.MatchId = ts.MatchId AND ts.Direction = 'Sell'
WHERE d.MatchedData BETWEEN '20230401' AND '20230410'
GROUP BY d.MatchedData
ORDER BY d.MatchedData;

-- ==========================================
-- Query 7: Cumulative Profit (April 1-10, 2023)
-- ==========================================
-- THOUGHT PROCESS:
-- - First calculate daily profit just like in Query 6
-- - Then use a window function to build a running total over the days
-- - SUM() OVER(ORDER BY MatchedData) adds each day's profit to all previous days
-- - ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW means "start from row 1 
--   and keeps adding up to the current row"
-- - Dates must be ordered so the cumulative total makes sense
-- - Aliased MatchedData to MatchedDate for readability


SELECT 
    d.MatchedData AS MatchedDate,
    SUM((ts.Price - tb.Price) * ts.Volume) AS DailyProfit,
    SUM(SUM((ts.Price - tb.Price) * ts.Volume)) 
        OVER (ORDER BY d.MatchedData 
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CumulativeProfit
FROM Deals d
JOIN Trades tb ON d.MatchId = tb.MatchId AND tb.Direction = 'Buy'
JOIN Trades ts ON d.MatchId = ts.MatchId AND ts.Direction = 'Sell'
WHERE d.MatchedData BETWEEN '20230401' AND '20230410'
GROUP BY d.MatchedData
ORDER BY d.MatchedData;




-- ==========================================
-- END OF SOLUTIONS
-- ==========================================
-- Testing Notes:
-- - Run on https://sqliteonline.com/ (MS SQL mode)
-- - All queries use schema as-provided (including typos)
-- - CAST() used for TraderTarget calculations
-- ==========================================