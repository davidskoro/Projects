#Load Data
data <- read.csv("data/analysisData.csv")
scoringData <- read.csv("data/scoringData.csv")

str(data)

#Model 0 Sample Linear Regression
model0 <- lm(price~daysonmarket,data)
pred0 <- predict(model0,newdata=scoringData)
summary(model0)

submissionFile = data.frame(id = scoringData$id, price = pred)
write.csv(submissionFile, 'sample_submission.csv',row.names = F)


#Model 1 Linear Regression using is_new variable
summary(model1 <- lm(price~daysonmarket+is_new, data))
pred1 <- predict(model1,newdata=scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred1)
write.csv(submissionFile, 'submission1.csv',row.names = F)

#Model 2 Polynomial Linear Regression using days on market variable
model2 <- lm(price~poly(daysonmarket, 2), data)
pred2 <- predict(model2,newdata = scoringData)

summary(model2)

submissionFile = data.frame(id = scoringData$id, price = pred2)
write.csv(submissionFile, 'submission2.csv',row.names = F)

#Model 3 Polynomial Linear Regression using days on market & is_new
model3 <- lm(price~poly(daysonmarket, 2)+is_new, data)
pred3 <- predict(model3,newdata = scoringData)

summary(model3)

submissionFile = data.frame(id = scoringData$id, price = pred3)
write.csv(submissionFile, 'submission3.csv',row.names = F)

#Model 4 Spline Regression using days on market
library(mgcv)
model4 = gam(price ~ s(daysonmarket)+is_new,method = 'REML', data = data)
summary(model4)
pred4 = predict(model4, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred4)
write.csv(submissionFile, 'submission4.csv',row.names = F)

#Model 5 Spline regression with correlating variables

data_numeric <- data[, sapply(data,is.numeric)]

library(ggcorrplot)
ggcorrplot(cor(data_numeric),
           method = 'square',
           type = 'lower',
           show.diag = F,
           colors = c('#e9a3c9', '#f7f7f7', '#a1d76a'))

library(mgcv)
model5 = gam(price ~ wheelbase_inches+back_legroom_inches+length_inches+width_inches+height_inches+maximum_seating+year+is_new+make_name,method = 'REML', data = data)
summary(model5)
pred5 = predict(model5, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred5)
write.csv(submissionFile, 'submission5.csv',row.names = F)

# Model 6 Linear vs Spline (Model 7 has the same score as model 6)
model6 = lm(price ~ wheelbase_inches+back_legroom_inches+length_inches+width_inches+height_inches+maximum_seating+year+is_new+make_name,method = 'REML', data = data)
summary(model6)
pred7 = predict(model6, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred7)
write.csv(submissionFile, 'submission6.csv',row.names = F)

#Model 7 Spline regression w/ Numeric Data selected via Backward Stepwise

start_mod = lm(price~.,data=data_numeric)
empty_mod = lm(price~1,data=data_numeric)
full_mod = lm(price~.,data=data_numeric)
backwardStepwise = step(start_mod,
                        scope=list(upper=full_mod,lower=empty_mod),
                        direction='backward')

summary(backwardStepwise)
backwardStepwise$anova

model7 = gam(price ~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+maximum_seating+year+mileage+owner_count+seller_rating+is_new+make_name+body_type,method = 'REML',data = data)
summary(model7)
pred7 = predict(model7, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred7)
write.csv(submissionFile, 'submission7.csv',row.names = F)

#Model 8 Decision Tree with variables selected via backwards step wise on numeric data

library(rpart); library(rpart.plot)

model8 = rpart(price~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+maximum_seating+year+mileage+owner_count+seller_rating+is_new+make_name+body_type,data = data, method = 'anova')
pred8 = predict(model8, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred8)
write.csv(submissionFile, 'submission8.csv',row.names = F)

#Model 9 Spline on columns selected via backwards stepwise with full columns in scoring data
colSums(is.na(scoringData))

model9 = gam(price ~ front_legroom_inches+length_inches+width_inches+height_inches+maximum_seating+year+is_new+make_name+body_type,method = 'REML',data = data)
pred9 = predict(model9, newdata = scoringData)
summary(model9)

submissionFile = data.frame(id = scoringData$id, price = pred9)
write.csv(submissionFile, 'submission9.csv',row.names = F)

#Model 10 -  Model 7 with missing numerical encoded as 0, categorical encoded as Not Available
colSums(is.na(data))

library(tidyr)
library(dplyr)
data <- data |>
  mutate_if(is.numeric, ~replace_na(., 0)) %>%
  mutate_if(is.character, ~replace_na(., "Not Available"))

scoringData <- scoringData |>
  mutate_if(is.numeric, ~replace_na(., 0)) %>%
  mutate_if(is.character, ~replace_na(., "Not Available"))

colSums(is.na(data))
colSums(is.na(scoringData))

model10 = gam(price ~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+maximum_seating+year+mileage+owner_count+seller_rating+is_new+make_name+body_type,method = 'REML',data = data)
summary(model10)
pred11 = predict(model10, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred11)
write.csv(submissionFile, 'submission10.csv',row.names = F)

#Model 11 Spline regression w/ Filled Values & Major Options
# Major options with dummy variables (1,2)
# Backwards step wise on numeric values
# Spline regression model using selected variables

data <- read.csv("data/analysisData.csv", na.strings=c("","NA"))
scoringData <- read.csv("data/scoringData.csv", na.string=c("","NA"))

library(tidyr)
library(dplyr)
library(stringr)
library(mgcv)

#Setting Up Test Data

data <- data |>
  mutate_if(is.numeric, ~replace_na(., 0)) %>%
  mutate_if(is.character, ~replace_na(., "Not Available"))

data <- data |>
  mutate(major_options = strsplit(as.character(major_options), ",")) |>
  unnest(major_options)

data$major_options <- str_remove(data$major_options, "[\\[]")
data$major_options <- str_remove(data$major_options, "[\\]]")
data$major_options <- str_remove(data$major_options, "[']")
data$major_options <- str_remove(data$major_options, "['']")
data$major_options <- str_trim(data$major_options)
data$count <- 1
data$major_options <- sub(" ", "_", data$major_options)
data$major_options <- sub("/", "_", data$major_options)

data <- data |>
  pivot_wider(names_from = major_options, values_from = count)

data <- data |>
  mutate_if(is.numeric, ~replace_na(., 0))

data_numeric <- data[, sapply(data,is.numeric)]
data_numeric <- data_numeric[1:50]

start_mod = lm(price~.,data=data_numeric)
empty_mod = lm(price~1,data=data_numeric)
full_mod = lm(price~.,data=data_numeric)
backwardStepwise = step(start_mod,
scope=list(upper=full_mod,lower=empty_mod),
direction='backward', steps = 100)

summary(backwardStepwise)
backwardStepwise$anova

# Setting Up Scoring Data
scoringData <- scoringData |>
  mutate_if(is.numeric, ~replace_na(., 0)) %>%
  mutate_if(is.character, ~replace_na(., "Not Available"))

scoringData <- scoringData |>
  mutate(major_options = strsplit(as.character(major_options), ",")) |>
  unnest(major_options)

scoringData$major_options <- str_remove(scoringData$major_options, "[\\[]")
scoringData$major_options <- str_remove(scoringData$major_options, "[\\]]")
scoringData$major_options <- str_remove(scoringData$major_options, "[']")
scoringData$major_options <- str_remove(scoringData$major_options, "['']")
scoringData$major_options <- str_trim(scoringData$major_options)
scoringData$count <- 1
scoringData$major_options <- sub(" ", "_", scoringData$major_options)
scoringData$major_options <- sub("/", "_", scoringData$major_options)

scoringData <- scoringData |>
  pivot_wider(names_from = major_options, values_from = count)

scoringData <- scoringData |>
  mutate_if(is.numeric, ~replace_na(., 0))

#Creating Model
model11 = gam(price ~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+daysonmarket+maximum_seating+year+mileage+owner_count+seller_rating+Bluetooth+Backup_Camera+Android_Auto+CarPlay+Sunroof_Moonroof+Navigation_System+Alloy_Wheels+Power_Package+Adaptive_Suspension+Remote_Start+Technology_Package+make_name+body_type+has_accidents+is_new+listing_color,method = 'REML',data = data)
summary(model11)
pred11 = predict(model11, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred12)
write.csv(submissionFile, 'submission11.csv',row.names = F)


#Model 12 Regression Tree Model w/ Filled values & major options
# Backwards step wise on numeric values
# Tree regression using selected variables
# Select categorical variables

library(rpart); library(rpart.plot)

model12 = rpart(price~  fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+daysonmarket+maximum_seating+year+mileage+owner_count+seller_rating+Bluetooth+Backup_Camera+Android_Auto+CarPlay+Sunroof_Moonroof+Navigation_System+Alloy_Wheels+Power_Package+Adaptive_Suspension+Remote_Start+Technology_Package+make_name+body_type+has_accidents+is_new+listing_color,data = data, method = 'anova')
pred12 = predict(model12, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred13)
write.csv(submissionFile, 'submission12.csv',row.names = F)

#Model 13

model13 = gam(price ~ fuel_tank_volume_gallons+highway_fuel_economy+city_fuel_economy+front_legroom_inches+length_inches+width_inches+height_inches+engine_displacement+horsepower+daysonmarket+maximum_seating+year+mileage+owner_count+seller_rating+Bluetooth+Backup_Camera+CarPlay+Sunroof_Moonroof+Navigation_System+Alloy_Wheels+Power_Package+Adaptive_Suspension+Tow_Package+Technology_Package+Cargo_Package+Not_Available+make_name+body_type+has_accidents+is_new+listing_color,method = 'REML',data = data)
summary(model13)
pred13 = predict(model13, newdata = scoringData)

submissionFile = data.frame(id = scoringData$id, price = pred14)
write.csv(submissionFile, 'submission13.csv',row.names = F)