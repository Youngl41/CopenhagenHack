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
library(DT)

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  
  
  # Application title
  titlePanel("Copenhagen Hackathon"),
  sidebarLayout(
    sidebarPanel(
      verbatimTextOutput("click_info")
      
    ),
    mainPanel(leafletOutput("myMap", height=700),
              p(),
              actionButton("updatecoord", "Find Me Attractions!", icon("paper-plane"), 
                           style="color: #fff; background-color: #337ab7; border-color: #2e6da4"),
              p(),
              DT::dataTableOutput("attractions_table")),
    
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
  
  places <-  read_csv('/Users/GitHub/CopenhagenHack/Working/clean_google_places.csv')
  places <- data.frame(places)
  
  start_clicked_coordinates <- as.data.frame(cbind(person$latitude, person$longitude))
  names(start_clicked_coordinates)[1] <- "lat"
  names(start_clicked_coordinates)[2] <- "lng"
  
  
  map <- leaflet() %>%
    addProviderTiles(providers$CartoDB.Positron) %>%
    addMouseCoordinates(style = "basic") %>%
    setView(lng = 12.58432, lat = 55.67821,  zoom = 13) %>%
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
                    paste("<b><a href='", places$website, "'>", places$name, "</a></b>", sep = ""),
                    paste("Address:", places$formatted_address),
                    paste('Rating: ', places$rating, sep = ""),
                    paste('Overall Sentiment: ', round(places$overall_sentiment_score, 1), sep = ""),
                    paste('Tweets: ', places$tweet_text, sep = "")))
  
  
  output$myMap = renderLeaflet(map)

  
  clicked_place <- observe({
    p1 <- input$myMap_click
    write.csv(as.data.frame(p1), "/Users/GitHub/CopenhagenHack/Working/clicked_coordinates.csv")
  })
  



  output$click_info <- renderPrint({
    cat("Map Click Coordinates:\n")
    as.data.frame(input$myMap_click)[c("lat", "lng")]
  })
  
  observeEvent(input$myMap_click, {
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
      addCircleMarkers(
        radius = 5,
        stroke = FALSE, 
        fillOpacity = 0.5,
        color = "grey",
        places$lng, 
        places$lat, 
        popup = paste(sep = "<br/>",
                      paste("<b><a href='", places$website, "'>", places$name, "</a></b>", sep = ""),
                      paste("Address:", places$formatted_address),
                      paste('Rating: ', places$rating, sep = ""),
                      paste('Overall Sentiment: ', round(places$overall_sentiment_score, 1), sep = ""),
                      paste('Tweets: ', places$tweet_text, sep = "")))
  })
  
  
  attractions <- eventReactive(input$updatecoord, {
    new_coordinates <- read_csv('/Users/GitHub/CopenhagenHack/Working/temp_output.csv')
    if (dim(new_coordinates)[1] == 0) {
      new_coordinates <- read_csv('/Users/GitHub/CopenhagenHack/Working/default_locations.csv')
    }
    new_coordinates
  })
  
  cols = c("name", "rating", "formatted_address", "international_phone_number", "proximity")
  
  output$attractions_table <- DT::renderDataTable({
    datatable(
      arrange(attractions()[cols], proximity) %>% mutate(proximity = paste(round(proximity, 0), ' m', sep = "")),
      filter = 'top',
      colnames=c("Name", "Rating", "Address", "Phone Number","Proximity")
    )
  })
  
  
  observeEvent(input$updatecoord, {
    person <- read_csv('/Users/GitHub/CopenhagenHack/Working/temp_person_coord.csv', col_types = ('ddcccd'))
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
      addCircleMarkers(
        radius = 5,
        stroke = FALSE, 
        fillOpacity = 0.5,
        color = "grey",
        places$lng, 
        places$lat, 
        popup = paste(sep = "<br/>",
                      paste("<b><a href='", places$website, "'>", places$name, "</a></b>", sep = ""),
                      paste("Address:", places$formatted_address),
                      paste('Rating: ', places$rating, sep = ""),
                      paste('Overall Sentiment: ', round(places$overall_sentiment_score, 1), sep = ""),
                      paste('Tweets: ', places$tweet_text, sep = ""))) %>%
      
      addCircleMarkers(radius = 5,
                       stroke = FALSE, 
                       fillOpacity = 0.8,
                       color = "red",
                       attractions()$lng, 
                       attractions()$lat, 
                       popup = paste(sep = "<br/>",
                                     paste("<b><a href='", 
                                           attractions()$website, 
                                           "'>", 
                                           attractions()$name, 
                                           "</a></b>", sep = ""),
                                     paste('Rating: ', attractions()$rating, sep = ""),
                                     paste('Availability: ', attractions()$traffic_class, sep = ""),
                                     paste('Visited: ', attractions()$visited_already, sep = ""),
                                     paste('Proximity: ', round(attractions()$proximity, 0), ' m', sep = ""),
                                     paste('Overall Sentiment: ', round(attractions()$overall_sentiment_score, 1), sep = ""),
                                     paste('Traffic: ', attractions()$traffic, sep = ""),
                                     paste('Tweets: ', attractions()$tweet_text, sep = "")
                       ))
    
  })
  
}


# Run the application 
shinyApp(ui = ui, server = server)