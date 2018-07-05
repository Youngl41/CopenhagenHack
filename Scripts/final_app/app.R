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
  
  sidebarLayout(
        sidebarPanel(
          
                  checkboxInput("checkbox_visited", label = "Available", value = FALSE),
          
                  checkboxInput("checkbox_visited", label = "Visited", value = FALSE)
                  ),
        mainPanel(leafletOutput("myMap")),
    
        position = c("right")
    )
    

  
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  
  person <- read_csv('/Users/Hackathon/CopenhagenHack/Working/temp_person_coord.csv', col_types = ('ddcccd'))
  person <- data.frame(person)
  
  coordinates <-  read_csv('/Users/Hackathon/CopenhagenHack/Working/temp_output.csv', col_names = TRUE)
  coordinates <- data.frame(coordinates)
  
  filtered_coordinates <-  reactive({ 
    coordinates[coordinates$traffic_class == "Completely free"]
  })
  
  
  places <-  read_csv('/Users/Hackathon/CopenhagenHack/Working/clean_google_places.csv', col_names = TRUE)
  places <- data.frame(places)  
  

  
    map <- 
      
      leaflet() %>%
      addTiles() %>%
      addMouseCoordinates(style = "basic") %>%
      
      addProviderTiles(providers$CartoDB.Positron) %>%
      
      setView(person$longitude, person$latitude, zoom = 16) %>%
      
      addMarkers(
        lat = person$latitude,
        lng = person$longitude, 
        popup = paste(sep = "<br/>",
                      paste('Customer segment: ', person$segment, sep = ""), 
                      paste('Number visited: ', person$num_places_visited, sep = ""),
                      paste('Date: ', person$date, sep = ""),
                      paste('Hour: ', person$hour, sep = ""))) %>%
      
      addCircleMarkers(
        radius = 5,
        stroke = FALSE, 
        fillOpacity = 0.5,
        color = "grey",
        places$lng, 
        places$lat, 
        popup = paste(sep = "<br/>",
                     paste("<b><a href='", coordinates$website, "'>", coordinates$name, "</a></b>", sep = ""),
                     paste('Rating: ', coordinates$rating, sep = ""),
                     paste('Availability: ', coordinates$traffic_class, sep = ""),
                     paste('Visited: ', coordinates$visited_already, sep = ""),
                     paste('Proximity: ', round(coordinates$proximity, 0), ' m', sep = ""),
                     paste('Overall Sentiment: ', round(coordinates$overall_sentiment_score, 1), sep = ""),
                     paste('Traffic: ', coordinates$traffic, sep = ""),
                     paste('Tweets: ', coordinates$tweet_text, sep = ""))) %>%
      
      addCircleMarkers(
        radius = 5,
        stroke = FALSE, 
        fillOpacity = 0.5,
        color = "red",
        coordinates$lng, 
        coordinates$lat, 
        popup = paste(sep = "<br/>",
                     paste("<b><a href='", filtered_coordinates$website, "'>", coordinates$name, "</a></b>", sep = ""),
                     paste('Rating: ', filtered_coordinates$rating, sep = ""),
                     paste('Availability: ', filtered_coordinates$traffic_class, sep = ""),
                     paste('Visited: ', filtered_coordinates$visited_already, sep = ""),
                     paste('Proximity: ', round(filtered_coordinates$proximity, 0), ' m', sep = ""),
                     paste('Overall Sentiment: ', round(filtered_coordinates$overall_sentiment_score, 1), sep = ""),
                     paste('Traffic: ', filtered_coordinates$traffic, sep = ""),
                     paste('Tweets: ', filtered_coordinates$tweet_text, sep = "")))
  
    
  
  
  output$myMap = renderLeaflet(map)
}


# Run the application 
shinyApp(ui = ui, server = server)



