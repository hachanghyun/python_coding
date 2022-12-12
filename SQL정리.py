-- 중복된 이름 개수 세기
SELECT count(DISTINCT NAME) 
FROM ANIMAL_INS 
WHERE NAME IS NOT NULL
SELECT ANIMAL_TYPE, 
       count(ANIMAL_TYPE) as count 
FROM ANIMAL_INS 
GROUP BY ANIMAL_TYPE 
ORDER BY ANIMAL_TYPE ASC
-- 동명이름 개수세기 조건 추가
SELECT
NAME
,COUNT
FROM
(
    SELECT NAME, COUNT(NAME) AS COUNT 
    FROM ANIMAL_INS 
    GROUP BY NAME 
    ORDER BY NAME ASC
) AS TA
WHERE COUNT >= 2
-- 입양 시각 정하기
SELECT 
    HOUR
  , COUNT(HOUR) AS COUNT
FROM
(
SELECT 
      HOUR(DATETIME) AS HOUR
FROM ANIMAL_OUTS 
) AS TA
WHERE HOUR >= 9 AND HOUR <= 19
GROUP BY HOUR
ORDER BY HOUR ASC
-- RECURSIVE 함수
WITH RECURSIVE RECUR AS
(
SELECT 
    0 AS HOUR
  , 0 AS COUNT
UNION ALL
SELECT 
    HOUR + 1
  , COUNT 
FROM RECUR
WHERE HOUR < 23
)
SELECT 
    TAA.HOUR
  -- , CASE WHEN TAA.COUNT != 0 THEN TAA.COUNT ELSE 0 END AS COUNT 
  , CASE WHEN TBB.COUNT IS NOT NULL THEN TBB.COUNT ELSE 0 END AS COUNT
FROM RECUR AS TAA
LEFT OUTER JOIN 
(SELECT
    HOUR
  , COUNT(HOUR) AS COUNT
FROM
(
    SELECT 
        HOUR(DATETIME) AS HOUR
    FROM ANIMAL_OUTS
) AS TA
WHERE HOUR >= 0 and HOUR <= 23
GROUP BY HOUR
ORDER BY HOUR ASC)
AS TBB
ON TAA.HOUR = TBB.HOUR
-- NULL 처리하기
SELECT
    ANIMAL_TYPE
  , CASE WHEN NAME IS NULL THEN 'No name' ELSE NAME END AS NAME
  , SEX_UPON_INTAKE
FROM
    ANIMAL_INS
-- 오랜기간 보호한 동물
SELECT 
    TA.NAME
  , TA.DATETIME
FROM
    ANIMAL_INS AS TA
LEFT JOIN ANIMAL_OUTS AS TB
ON TA.ANIMAL_ID = TB.ANIMAL_ID
WHERE TB.ANIMAL_ID IS NULL
ORDER BY TA.DATETIME ASC
LIMIT 3

-- 보호소에서 보호한 동물
SELECT
    ANIMAL_ID
  , ANIMAL_TYPE
  , NAME
FROM
(
SELECT
    TA.ANIMAL_ID
  , TA.ANIMAL_TYPE
  , TA.NAME
  , TA.SEX_UPON_INTAKE
  , TB.SEX_UPON_OUTCOME
FROM
    ANIMAL_INS AS TA
INNER JOIN ANIMAL_OUTS AS TB
ON TA.ANIMAL_ID = TB.ANIMAL_ID 
WHERE TA.SEX_UPON_INTAKE like '%Intact%'
AND (TB.SEX_UPON_OUTCOME like '%Spayed%' OR TB.SEX_UPON_OUTCOME like '%Neutered%')
) AS TZ
-- 중성화 여부 파악
SELECT
    ANIMAL_ID
  , NAME
  , CASE WHEN SEX_UPON_INTAKE like '%Neutered%' OR
SEX_UPON_INTAKE like '%Spayed%' THEN 'O' ELSE 'X' END AS 중성화
FROM ANIMAL_INS

-- 기간비교
SELECT
    ANIMAL_ID
  , NAME
FROM
(
SELECT 
    DATEDIFF(TB.DATETIME,TA.DATETIME) AS DATEDIFF
  , TA.ANIMAL_ID
  , TA.NAME
FROM ANIMAL_INS AS TA
INNER JOIN ANIMAL_OUTS AS TB
ON TA.ANIMAL_ID = TB.ANIMAL_ID
ORDER BY DATEDIFF DESC
LIMIT 2
) AS TZ


