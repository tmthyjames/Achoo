# train_model.r
library('RPostgreSQL')

pg <- dbDriver("PostgreSQL")

con <- dbConnect(pg, user=Sys.getenv('USERNAME'), password=Sys.getenv('PASSWORD'),
                host="localhost", port=5432, dbname="allergyalert")

dtab <- dbGetQuery(con, "
    select distinct on(t.dateof) t.dateof, *
    from daily_weather d
    join pollutants p 
        on to_char(to_timestamp(p.dateof), 'YYYY-MM-DD') = to_char(to_timestamp(d.time), 'YYYY-MM-DD')
    join treatments t
        on to_char(to_timestamp(t.dateof), 'YYYY-MM-DD') = to_char(to_timestamp(d.time), 'YYYY-MM-DD')
    join allergens a 
        on to_char(to_timestamp(a.dateof), 'YYYY-MM-DD') = to_char(to_timestamp(d.time), 'YYYY-MM-DD')
")

# for now, ignoring distinction between breathing treatment (2) and inhaler useage (1)
dtab$treatment_ <- ifelse(dtab$treatment>0, 1, 0)

model <- glm(
    treatment_ ~ ozone 
        + dewPoint
        + humidity
        + pressure
        + windSpeed
        + pollutant
        + Index
        + value,
    data=dtab,
    family=binomial(link="logit")
)
                   
saveRDS(model, 'achoo_model_logistic_glm.r')