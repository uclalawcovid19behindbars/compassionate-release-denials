library(tidyverse)
library(lubridate)
library(glue)

formatted_date <- format(today(), "%m-%d-%Y")

dat_path <- file.path('~', 'UCLA', 'code', 'compassionate-releases', 'compassionate-release-denials', 'data')

## read in the old archive
old_dat <- read_csv(file.path(dat_path, 'archive_crs.csv'),
                    col_types = cols(Cause = "c")) %>% 
            mutate(docketNum = substr(`Docket Number`, 1, 13),
                   document_id = glue("{`Case Name`}_{docketNum}_{`Document Number`}_{`Date Filed`}"))

## read in the current archive (old + new)
current_dat <- read_csv(file.path(dat_path, glue('archive_{formatted_date}.csv')),
                            col_types = cols(Cause = "c")) %>% 
                mutate(docketNum = substr(`Docket Number`, 1, 13),
                       document_id = glue("{`Case Name`}_{docketNum}_{`Document Number`}_{`Date Filed`}"))

## isolate new documents from current_dat
new_dat <- anti_join(current_dat, old_dat, by = "document_id") %>% 
          select(-X1,
                 -docketNum,
                 -document_id)

nrow(current_dat) - nrow(old_dat)
nrow(new_dat)

write_csv(new_dat, file.path(dat_path, "archive_new.csv"))

## clean up for next time
# rename current_dat "archive_crs.csv"
write_csv(current_dat, file.path(dat_path, 'archive_crs.csv'))

# delete "archive_{today's date}.csv"
file.remove(file.path(dat_path, glue('archive_{formatted_date}.csv')))
