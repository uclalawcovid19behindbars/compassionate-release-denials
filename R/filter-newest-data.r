library(tidyverse)
library(lubridate)
library(stringr)
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

## filter out first word "motion"
## flag if description contains the word "pre-trial"
new_dat_out <- new_dat %>% 
       mutate(isPreTrial = ifelse(str_detect(`Document Description`, "(?i)pre-trial|pre trial|pretrial"), TRUE, ""),
              firstWordInDesc = tolower(word(`Document Description`, 1)),
              isMotion = ifelse(firstWordInDesc == "motion", TRUE, FALSE)
              ) %>% 
       filter(!isMotion) %>% 
       select(-firstWordInDesc,
              -isMotion)

write.csv(new_dat_out, file.path(dat_path, "archive_new.csv"), na="", row.names=FALSE)

## clean up for next time
# rename current_dat "archive_crs.csv"
write_csv(current_dat, file.path(dat_path, 'archive_crs.csv'))

# delete "archive_{today's date}.csv"
file.remove(file.path(dat_path, glue('archive_{formatted_date}.csv')))
