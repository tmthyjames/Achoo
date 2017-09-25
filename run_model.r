# run_model.r
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
    order by t.dateof desc
    limit 1
")

# for now, ignoring distinction between breathing treatment (2) and inhaler useage (1)
dtab$treatment_ <- ifelse(dtab$treatment>0, 1, 0)

# obviously you'll want to use actual data here to predict
predict_value <- predict(model, newdata = dtab[1,])
                   
today <- as.numeric(as.POSIXct(Sys.time()))
results <- data.frame(prediction=predict_value[[1]], dateof=today)

dbWriteTable(con, 'results', results, row.names=FALSE, append=TRUE)