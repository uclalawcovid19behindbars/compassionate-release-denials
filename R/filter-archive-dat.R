library(tidyverse)

dat_path <- file.path('~', 'UCLA', 'code', 'compassionate-releases', 'compassionate-release-denials', 'data', 'archive_crs.csv')
dat <- read_csv(dat_path)

missing_dat <- dat %>% 
    filter(is.na(`Judge (initial)`) | is.na(`Prosecutor Name`))

n_distinct(missing_dat$`Docket ID`) # find distinct number of cases with missing info 

write_csv(missing_dat, '/Users/hope/UCLA/code/compassionate-releases/compassionate-release-denials/data/missings_crs.csv')