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
                  numericInput("lat", "Latitude:", value = 12.6, min = -90, max = 90, step = 0.001),
 
                  numericInput("long", "Longitude:", value = 55.7, min = -90, max = 90, step = 0.001),

                  dateInput("date", "Date:", value = "2018-05-03", format = "dd/mm/yyyy", language = "en",
                            weekstart = 1),
                  sliderInput("long", "Hour:", value = 15, min = 0, max = 24, step = 1)
                  ),
        mainPanel(leafletOutput("myMap")),
    
        position = c("right")
    )
    
    # Show a plot of the generated distribution

  
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
    setView(person$longitude, person$latitude, zoom = 16) %>%
    addMarkers(
      lat = person$latitude,
      lng = person$longitude, popup = paste(sep = "<br/>",
                                            paste('Customer segment: ', person$segment, sep = ""), 
                                            paste('Number visited: ', person$num_places_visited, sep = ""),
                                            paste('Date: ', person$date, sep = ""),
                                            paste('Hour: ', person$hour, sep = "")
                                            )) %>%
    addCircleMarkers(radius = 5,
                     stroke = FALSE, 
                     fillOpacity = 0.5,
                     color = "red",
                     #clusterOptions = markerClusterOptions(iconCreateFunction =
                    #                                         JS("
                     #                                           function(cluster) {
                      #                                          return new L.DivIcon({
                       #                                         html: '<div style=\"background-color:rgba(77,77,77,0.5)\"><span>' + cluster.getChildCount() + '</div><span>',
                        #                                        className: 'marker-cluster'
                         #                                       });
                          #                                      }")), 
                          coordinates$lng, 
                     coordinates$lat, 
                     popup = paste(sep = "<br/>",
                                   paste("<b><a href='", 
                                         coordinates$website, 
                                         "'>", 
                                         coordinates$name, 
                                         "</a></b>", sep = ""),
                                   paste('Rating: ', coordinates$rating, sep = ""),
                                   paste('Availability: ', coordinates$traffic_class, sep = ""),
                                   paste('Visited: ', coordinates$visited_already, sep = ""),
                                   paste('Proximity: ', round(coordinates$proximity, 0), ' m', sep = ""),
                                   paste('Overall Sentiment: ', round(coordinates$overall_sentiment_score, 1), sep = ""),
                                   paste('Traffic: ', coordinates$traffic, sep = ""),
                                   paste('Tweets: ', coordinates$tweet_text, sep = "")
                     ))
  
  
  output$myMap = renderLeaflet(map)
}


# Run the application 
shinyApp(ui = ui, server = server)



