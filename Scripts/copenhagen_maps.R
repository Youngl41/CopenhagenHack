library(ggplot2)
library(ggmap)
library(readr)
library(scales)
library(plotly)


coordinates <-  read_csv('/Users/mia/Downloads/clean_sample_loc.csv', col_names = TRUE, col_types = "ccdd")

coordinates$time_tuple <- strptime(coordinates$time_tuple, format = "%Y-%m-%d %H:%M:%S")

data <- data.frame(coordinates)



copenhagen_map <- get_googlemap(center = "copenhagen", zoom = 12, scale = 2, maptype = 'roadmap', color='bw')
copenhagen_map <- ggmap(copenhagen_map)


# VERY FIRST ATTEMPT
copenhagen_map + geom_point(aes(x = longitude, y = latitude), 
                   colour = "red", 
                   na.rm = TRUE,
                   size = 2, 
                   data = data)


# FIRST ATTEMPT
copenhagen_map +
  stat_density2d(aes(x = longitude, y = latitude, fill = ..level.., alpha = ..level..),
                 size = 2, 
                 bins = 30, 
                 data = data, 
                 geom = "polygon",
                 na.rm = TRUE) +
  scale_fill_gradient("Count") +
  scale_alpha(range = c(.4, .8), guide = FALSE) +
  guides(fill = guide_colorbar(barwidth = 1.5, barheight = 10))



# SECOND ATTEMPT
copenhagen_map +
  stat_density2d(aes(x = longitude, y = latitude, fill = ..level.., alpha = ..level..),
                 size = 2, 
                 bins = 200, 
                 data = data, 
                 geom = "polygon",
                 na.rm = TRUE,
                 show.legend = FALSE) +
  scale_fill_gradient("Fraction", low = "red", high = "blue")



# ANOTHER ATTEMPT
copenhagen_map +
  stat_density2d(aes(x = longitude, y = latitude, fill = ..level.., alpha = ..level..),
                 size = 2, 
                 bins = 200, 
                 data = data, 
                 geom = "polygon",
                 na.rm = TRUE) +
  scale_fill_gradient("Fraction", low = "blue", high = "red") +
  scale_alpha(range = c(.1, .4), guide = FALSE) +
  guides(fill = guide_colorbar(barwidth = 3, barheight = 5)) +
  theme_nothing(legend = TRUE) 



# THIRD ATTEMPT
copenhagen_map +
  stat_density2d(aes(x = longitude, y = latitude, fill = ..level.., alpha = ..level..),
                 bins = 100, 
                 geom = "polygon",
                 data = data,
                 show.legend = FALSE,
                 na.rm = TRUE ) +
  scale_fill_gradient("Tweet Count", low = "blue", high = "red") +
  theme_nothing(legend = TRUE) 

# when alpha set to count then the more tweets, the less opacity
# FOURTH ATTEMPT
copenhagen_map +
  geom_bin2d(aes(x = longitude, y = latitude, fill = ..count..), 
           data = data, 
           stat = "bin2d",
           position = "identity",
           bins = 20,
           na.rm = TRUE, 
           show.legend = FALSE) +
  scale_fill_distiller("Tweets Count", palette = "RdBu") +
  theme_nothing(legend = TRUE) +
  guides(fill = guide_colorbar(barwidth = 1.5, barheight = 5))


# FIFTH ATTEMPT - set fill to log and edited opacity
copenhagen_map + 
  geom_bin2d(aes(x = longitude, y = latitude, fill = log(..count..), alpha = 1), 
             data = data, 
             stat = "bin2d",
             position = "identity",
             bins=10,
             na.rm = TRUE, 
             show.legend = FALSE) + 
  scale_fill_gradient("log(tweet count)",space="Lab", low = "#bcbddc", high = "#3f007d") + 
  theme_nothing(legend = TRUE) +
  guides(fill = guide_colorbar(barwidth = 1.5, barheight = 6))



# SIXTH ATTEMPT
copenhagen_map + 
  geom_bin2d(aes(x = longitude, y = latitude, fill = ..count.., alpha = ..count..), 
             data = data, 
             stat = "bin2d",
             position = "identity",
             bins=50,
             na.rm = TRUE, 
             show.legend = FALSE) + 
  scale_fill_distiller(palette = "Spectral", breaks = pretty_breaks(n = 5))+
  theme_nothing(legend = TRUE) 



# Diverging
# BrBG, PiYG, PRGn, PuOr, RdBu, RdGy, RdYlBu, RdYlGn, Spectral
# Qualitative
# Accent, Dark2, Paired, Pastel1, Pastel2, Set1, Set2, Set3
# Sequential
# Blues, BuGn, BuPu, GnBu, Greens, Greys, Oranges, OrRd, PuBu, PuBuGn, PuRd, Purples, RdPu, Reds, YlGn, YlGnBu, YlOrBr, YlOrRd

