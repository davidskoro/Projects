#Model: Spline regression w/ Filled Values & Major Options
# Major options with dummy variables (1,2)
# Backwards step wise on numeric values
# Spline regression model using selected variables

#Load the data. Set spaces to NAs
data <- read.csv("data/analysisData.csv", na.strings=c("","NA"))
scoringData <- read.csv("data/scoringData.csv", na.string=c("","NA"))

#Load the packages
library(tidyr)
library(dplyr)
library(stringr)
library(mgcv)

#Cleaning Data

#Test Data
data <- data |>
  # Replace NAs with 0s & "Not Available"
  mutate_if(is.numeric, ~replace_na(., 0)) |>
  mutate_if(is.character, ~replace_na(., "Not Available")) |>
  #Split major_options into individual rows
  mutate(major_options = strsplit(as.character(major_options), ",")) |>
  unnest(major_options)

#Scoring Data
scoringData <- scoringData |>
  # Replace NAs with 0s & "Not Available"
  mutate_if(is.numeric, ~replace_na(., 0)) %>%
  mutate_if(is.character, ~replace_na(., "Not Available")) |>
  #Split major_options into individual rows
  mutate(major_options = strsplit(as.character(major_options), ",")) |>
  unnest(major_options)

# Remove & replace special characters

#Test Data
data$major_options <- str_remove_all(data$major_options,"[\\[\\]''']") # Remove special characters
data$major_options <- str_trim(data$major_options)  # Remove white space
data$major_options <- gsub(" ", "_", data$major_options) # Replace with a space
data$major_options <- gsub("/", "_", data$major_options) # Replace with a space

#Scoring Data
scoringData$major_options <- str_remove_all(scoringData$major_options, "[\\[\\]''']") # Remove special characters
scoringData$major_options <- str_trim(scoringData$major_options) # Remove white space
scoringData$major_options <- gsub(" ", "_", scoringData$major_options) # Replace with a space
scoringData$major_options <- gsub("/", "_", scoringData$major_options) # Replace with a space

# Pivot major options for variables selection

#Create dummy count variable
data$count <- 1
#Pivot wider so major options are a select-able column
data <- data |>
  pivot_wider(names_from = major_options, values_from = count) |>
  mutate_if(is.numeric, ~replace_na(., 0))

#Create dummy count variable
scoringData$count <- 1
#Pivot wider so major options are a select-able column
scoringData <- scoringData |>
  pivot_wider(names_from = major_options, values_from = count) |>
  mutate_if(is.numeric, ~replace_na(., 0))

# Select only numeric values from test data for quicker variable selection
data_numeric <- data[, sapply(data,is.numeric)]
data_numeric <- data_numeric[1:50] # Revisit

#Perform backwards stepwise for variable selection

start_mod = lm(price~.,data=data_numeric)
empty_mod = lm(price~1,data=data_numeric)
full_mod = lm(price~.,data=data_numeric)
backwardStepwise = step(start_mod,
scope=list(upper=full_mod,lower=empty_mod),
direction='backward')

summary(backwardStepwise) 

#Creating Model

# Select variables that are highly significant & apply to a spline model
model = gam(price ~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+back_legroom_inches+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+daysonmarket+maximum_seating+year+mileage+owner_count+seller_rating+Bluetooth+Backup_Camera+Android_Auto+CarPlay+Sunroof_Moonroof+Navigation_System+Alloy_Wheels+Power_Package+Third_Row_Seating+Leather_Seats+Adaptive_Cruise_Control+Adaptive_Suspension+Blind_Spot_Monitoring+Tow_Package+Standard_Suspension_Package+Technology_Package+Off_Road_Package+Cargo_Package+Quick_Order_Package+make_name+body_type+has_accidents+is_new+listing_color,method = 'REML',data = data)
summary(model)
pred = predict(model, newdata = scoringData)

#Create new .csv submission
submissionFile = data.frame(id = scoringData$id, price = pred)
write.csv(submissionFile, 'Final Submission.csv',row.names = F)
