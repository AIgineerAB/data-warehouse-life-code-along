-- this is an extract of the model 

--CTE part for clean code
--this with create temporary data for the final select statement
with stg_job_ads as (select * from {{ source('job_ads', 'stg_ads') }} )


--Select statement is the major part of the model
SELECT 
    occupation__label,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline
FROM stg_job_ads
order by application_deadline