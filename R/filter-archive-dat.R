library(tidyverse)

dat_path <- file.path('~', 'UCLA', 'code', 'compassionate-releases', 'compassionate-release-denials', 'data', 'archive_crs.csv')
dat <- read_csv(dat_path)

missing_dat <- dat %>% 
    filter(is.na(`Judge (initial)`) | is.na(`Prosecutor Name`)) %>% 
    distinct(`Docket ID`, .keep_all = TRUE)

nrow(missing_dat) # only save unique dockets

write_csv(missing_dat, '/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/missings_crs.csv')