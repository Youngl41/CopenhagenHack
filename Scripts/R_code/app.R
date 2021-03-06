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
library(rgdal)
library(mapview)

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  
  
  # Application title
  titlePanel("Copenhagen Hackathon"),
  sidebarLayout(
    sidebarPanel(
      verbatimTextOutput("click_info")
    ),
    mainPanel(leafletOutput("myMap")),
    
    position = c("right")
    ),
  
  tags$style(type="text/css",
             ".shiny-output-error { visibility: hidden; }",
             ".shiny-output-error:before { visibility: hidden; }"
  )
  )
  
  # Show a plot of the generated distribution
  

# Define server logic required to draw a histogram
server <- function(input, output, session) {
  
  
  person <- read_csv('/Users/GitHub/CopenhagenHack/Working/temp_person_coord.csv', col_types = ('ddcccd'))
  person <- data.frame(person)
  
  coordinates <-  read_csv('/Users/GitHub/CopenhagenHack/Working/temp_output.csv', col_names = TRUE)
  
  new_coordinates <- reactiveFileReader(100, session, '/Users/GitHub/CopenhagenHack/Working/temp_output.csv', read.csv)
  
  coordinates <- data.frame(coordinates)
  
  places <-  read_csv('/Users/GitHub/CopenhagenHack/Working/clean_google_places.csv', col_names = TRUE)
  places <- data.frame(places)
  	
  map <- reactive({
    
    leaflet() %>%
    addProviderTiles(providers$CartoDB.Positron) %>%
    addMouseCoordinates(style = "basic") %>%
    setView(lng = 12.6012, lat = 55.67274264022657, zoom = 15) %>%
    addMarkers(
        lat = 55.67274264022657,
        lng = 12.6012, popup = paste(sep = "<br/>",
                                                 paste('Customer segment: ', person$segment, sep = ""), 
                                                 paste('Number visited: ', person$num_places_visited, sep = ""),
                                                 paste('Date: ', person$date, sep = ""),
                                                 paste('Hour: ', person$hour, sep = "")
        )) %>%
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
                      paste('Tweets: ', coordinates$tweet_text, sep = "")))
  })
  
  
  output$myMap = renderLeaflet(map())
  
  clicked_place <- observe({
    p1 <- input$myMap_click
    write.csv(as.data.frame(p1), "/Users/GitHub/CopenhagenHack/Working/clicked_coordinates.csv")
  })
  
  output$click_info <- renderPrint({
    cat("Map Click Coordinates:\n")
    as.data.frame(input$myMap_click)[c("lat", "lng")]
  })
  
  
  observeEvent(input$myMap_click, {
    invalidateLater(1000, session)
    leafletProxy("myMap") %>%
      clearMarkers() %>%
      addMarkers(
        lat = as.data.frame(input$myMap_click)$lat,
        lng = as.data.frame(input$myMap_click)$lng, popup = paste(sep = "<br/>",
                                                 paste('Customer segment: ', person$segment, sep = ""), 
                                                 paste('Number visited: ', person$num_places_visited, sep = ""),
                                                 paste('Date: ', person$date, sep = ""),
                                                 paste('Hour: ', person$hour, sep = "")
        )) %>%
    addCircleMarkers(radius = 5,
                     stroke = FALSE, 
                     fillOpacity = 0.5,
                     color = "red",
                     new_coordinates()$lng, 
                     new_coordinates()$lat, 
                     popup = paste(sep = "<br/>",
                                   paste("<b><a href='", 
                                         coordinates$website, 
                                         "'>", 
                                         coordinates$name, 
                                         "</a></b>", sep = ""),
                                   paste('Rating: ', new_coordinates()$rating, sep = ""),
                                   paste('Availability: ', new_coordinates()$traffic_class, sep = ""),
                                   paste('Visited: ', new_coordinates()$visited_already, sep = ""),
                                   paste('Proximity: ', round(new_coordinates()$proximity, 0), ' m', sep = ""),
                                   paste('Overall Sentiment: ', round(new_coordinates()$overall_sentiment_score, 1), sep = ""),
                                   paste('Traffic: ', new_coordinates()$traffic, sep = ""),
                                   paste('Tweets: ', new_coordinates()$tweet_text, sep = "")
                     )) %>%
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
                      paste('Tweets: ', coordinates$tweet_text, sep = "")))
  })
  

  
}


# Run the application 
shinyApp(ui = ui, server = server)