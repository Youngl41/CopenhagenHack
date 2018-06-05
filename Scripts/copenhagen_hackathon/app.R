#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
library(readr)
library(shiny)
library(leaflet)
library(RColorBrewer)
library(scales)
library(lattice)
library(dplyr)
library(htmltools)


# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("Copenhagen Hackathon"),
   
   # Sidebar with a slider input for number of bins 
   sidebarLayout(
      sidebarPanel(
        dateRangeInput('dateRange2',
                       label = paste('Date range input'),
                       start = Sys.Date() - 7, end = Sys.Date(),
                       separator = " - ", format = "dd/mm/yy",
                       startview = 'year', language = 'en', weekstart = 1
        )
      ),
      
      # Show a plot of the generated distribution
      mainPanel(
        leafletOutput("myMap")
      )
   )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  

  person <- read_csv('/Users/Hackathon/CopenhagenHack/Working/temp_person_coord.csv', col_types = ('ddcccd'))
  person <- data.frame(person)
  
  coordinates <-  read_csv('/Users/Hackathon/CopenhagenHack/Working/temp_output.csv', col_names = TRUE)
  #coordinates$time_tuple <- strptime(coordinates$time_tuple, format = "%Y-%m-%d %H:%M:%S")
  #coordinates <- coordinates[coordinates$time_tuple > input$start & coordinates$time_tuple < input$end,]

  coordinates <- data.frame(coordinates)
  

  
  
  map <- leaflet() %>%
         addTiles() %>% 
         addProviderTiles(providers$CartoDB.Positron) %>% 
         setView(person$longitude, person$latitude, zoom = 15) %>%
         addMarkers(
                          lat = person$latitude,
                          lng = person$longitude) %>%
         addCircleMarkers(radius = 5,
                          stroke = FALSE, 
                          fillOpacity = 0.5,
                          color = "blue",
                          clusterOptions = markerClusterOptions(), 
                          coordinates$lng, 
                          coordinates$lat, 
                          popup = paste(sep = "<br/>",
                                        paste("<b><a href='", 
                                              coordinates$website, 
                                              "'>", 
                                              coordinates$name, 
                                              "</a></b>", sep = ""),
                                        paste('Rating: ', coordinates$rating, sep = ""),
                                        paste('Business: ', coordinates$traffic_class, sep = ""),
                                        paste('Visited: ', coordinates$visited_already, sep = ""),
                                        paste('Proximity: ', coordinates$proximity, sep = ""),
                                        paste('Overall Sentiment:', coordinates$overall_sentiment_score, sep = ""),
                                        paste('Twitter Sentiment:', coordinates$overall_twitter_sentiment, sep = "")
                                        ))

                          
  output$myMap = renderLeaflet(map)
  }


# Run the application 
shinyApp(ui = ui, server = server)

