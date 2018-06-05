#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(leaflet)
library(RColorBrewer)
library(scales)
library(lattice)
library(dplyr)


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
  
  
  coordinates <-  read_csv('/Users/mia/Downloads/clean_sample_loc.csv', col_names = TRUE, col_types = "ccdd")
  coordinates$time_tuple <- strptime(coordinates$time_tuple, format = "%Y-%m-%d %H:%M:%S")
  
  #coordinates <- coordinates[coordinates$time_tuple > input$start & coordinates$time_tuple < input$end,]

  data <- data.frame(coordinates)
  
  map <- leaflet() %>%
         addTiles() %>% 
         addProviderTiles(providers$CartoDB.Positron) %>% 
         setView(12.5683,55.6761, zoom = 15) %>% 
         addCircleMarkers(radius = 5,
                          stroke = FALSE, 
                          fillOpacity = 0.5,
                          color = "red",
                          clusterOptions = markerClusterOptions(), 
                          data$longitude, 
                          data$latitude, 
                          popup = data$unique_id)
  
  output$myMap = renderLeaflet(map)
  }


# Run the application 
shinyApp(ui = ui, server = server)

