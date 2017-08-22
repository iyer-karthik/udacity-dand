rm(list=ls())
library(dplyr)
library(ggplot2)
library(data.table)
library(gridExtra)
library(reshape2)
library(GGally)
library(ggcorrplot)
library(psych)

news <- read.csv("OnlineNewsPopularity.csv")

str(news) 

news <- data.table(news)

# Add a new column which tells what cetegory the news falls in
news[, topic := ifelse(data_channel_is_lifestyle == 1, "Lifestyle",
                ifelse(data_channel_is_entertainment == 1, "Entertainment",
                ifelse(data_channel_is_bus == 1 , "Business", 
                ifelse(data_channel_is_socmed == 1, "Social media",
                ifelse(data_channel_is_tech == 1, "Technology",
                ifelse(data_channel_is_world == 1, "World", "Other"))))))]

# Add a new column which tells what day the news article was published
news[ ,day_of_publication := ifelse(weekday_is_monday == 1, "Monday",
                             ifelse(weekday_is_tuesday == 1, "Tuesday",
                             ifelse(weekday_is_wednesday == 1 , "Wednesday", 
                             ifelse(weekday_is_thursday == 1, "Thursday",
                             ifelse(weekday_is_friday == 1, "Friday",
                             ifelse(weekday_is_saturday == 1, "Saturday",
                             ifelse(weekday_is_sunday == 1, "Sunday", NA)))))))]

news <- na.omit(news)

describe(news$shares)
summary(news$shares)

grid.arrange(news %>%
               filter(shares > 0) %>%
               ggplot(aes(x = shares)) + 
               geom_histogram(bins = 50, fill = 'brown') + 
               scale_x_log10()+
               xlab('Number of shares') + 
               ylab('Count'),
             ggplot(aes(x = 1,y=shares),
                    data=news) + 
               geom_boxplot(fill ='brown') + 
               scale_y_log10() +
               xlab('') +
               ylab('Number of shares') +
               stat_summary(fun.y = "mean", 
                            geom = "point", 
                            color = "blue", 
                            shape = 8, 
                            size = 4),
             ncol=2)

ggplot(aes(factor(topic)), 
       data = news) +
  geom_bar( ) + 
  xlab('Topic')


ggplot(aes(factor(topic), 
           shares), 
       data = news) +
  geom_jitter(alpha = .05)  + 
  geom_boxplot( alpha = .5,color = 'blue')+ 
  stat_summary(fun.y = "mean", 
               geom = "point", 
               color = "red", 
               shape = 8, 
               size = 4)  +
  scale_y_log10() + 
  xlab('Topic') + 
  ylab('Number of shares') + 
  geom_hline(yintercept = median(news$shares))


news %>%
  group_by(topic) %>%
  summarize(median_shares = median(shares),
            avg_shares = mean(shares),
            sd_shares = sd(shares))

merge(news %>%
        group_by(topic) %>%
        summarize(total_shares = n()),
      news %>%
        group_by(topic) %>%
        filter(shares > 10000) %>%
        summarize(high_shares = n()),
      by = 'topic') %>%
  mutate(high_shares_percentage = total_shares/high_shares)

news %>%
  ggplot(aes(x = n_tokens_content)) + 
  geom_histogram(binwidth = 200, fill = 'cornflowerblue') + 
  facet_wrap(~topic) + 
  xlab('Number of words in content') 

ggplot(aes(factor(topic), 
           n_tokens_content), 
       data = news) +
  geom_jitter(alpha = .05)  + 
  geom_boxplot( alpha = .5,color = 'blue')+ 
  stat_summary(fun.y = "mean", 
               geom = "point", 
               color = "red", 
               shape = 8, 
               size = 4)  +
  xlab('Topic') + 
  ylab('Number of words') + 
  geom_hline(yintercept = median(news$n_tokens_content))

news %>% 
  filter(n_tokens_content == 0 & num_imgs == 0 & num_videos == 0) %>%
  group_by(topic) %>%
  summarize(avg_shares = median(shares),
            total_count = n())

news_non_zero_words <- news %>%
  filter(n_tokens_content > 0)

ggplot(aes(factor(topic), 
           average_token_length), 
       data = news_non_zero_words) +
  geom_jitter(alpha = .05)  + 
  geom_boxplot( alpha = .5,color = 'blueviolet')+ 
  stat_summary(fun.y = "mean", 
               geom = "point", 
               color = "red", 
               shape = 8, 
               size = 4)  +
  xlab('Topic') + 
  ylab('Average word length') + 
  geom_hline(yintercept = median(news$average_token_length))

news %>%
  group_by(topic) %>%
  filter(average_token_length > 5 & n_tokens_content > 0) %>%
  summarize(Total = n())

my_box_plot <- function (df, x, y, fillcolor){
  
  'plots box plots by topic
  df - data frame
  y - y axis variable as a string
  x - x axis variable (categorical) as a string.
  fillcolor - color name as a string'
  
  plot <- ggplot(aes(x = get(x),
                     y = get(y)),
                 data = df) + 
    stat_boxplot(fill = fillcolor) + 
    theme(text = element_text(size = 10),
          axis.text.x = element_text(angle = 90, hjust=1))
  plot
  
}

news_non_empty_title <- news %>%
  filter(n_tokens_title > 0)
# Consider only those news articles which have non empty titles.
# Conclusions will be more robust then.

grid.arrange(my_box_plot(df = news_non_empty_title,
                         x = 'topic',
                         y = 'title_subjectivity',
                         fillcolor = 'cyan3') + 
               ylab('Title Subjectivity') + 
               xlab('Topic'), 
             my_box_plot(df = news_non_empty_title,
                         x = 'topic',
                         y = 'title_sentiment_polarity',
                         fillcolor = 'aquamarine') + 
               ylab('Title Sentiment polarity') + 
               xlab('Topic'), 
             ncol=2)

grid.arrange(my_box_plot(df = news_non_zero_words,
                         x = 'topic',
                         y = 'global_subjectivity',
                         fillcolor = 'beige') +
               ylab('Article Subjectivity') + 
               xlab('Topic'), 
             my_box_plot(df = news_non_zero_words,
                         x = 'topic',
                         y ='global_sentiment_polarity',
                         fillcolor = 'springgreen') +
               ylab('Article Sentiment') + 
               xlab('Topic'),
             ncol=2)

grid.arrange(my_box_plot(df = news_non_zero_words,
                         x = 'topic',
                         y = 'global_rate_positive_words',
                         fill = 'green') + 
               ylab('Rate of positive words') + 
               xlab('Topic'), 
             my_box_plot(df = news_non_zero_words,
                         x = 'topic',
                         y = 'global_rate_negative_words',
                         fill = 'red') + 
               ylab('Rate of negative words') + 
               xlab('Topic'), 
             ncol=2)

grid.arrange(news %>%
               ggplot(aes(x = num_imgs)) +
               geom_histogram(binwidth = 5, fill = ' brown1') + 
               xlab('Number of images'),
             news %>%
               ggplot(aes(x = num_videos)) +
               geom_histogram(binwidth = 1, fill = ' brown1') + 
               xlab('Number of videos'),
             ncol=2)

news  %>%
  group_by(topic) %>%
  summarize(avg_images = median(num_imgs),
            avg_videos = median(num_videos),
            total = n())

ggplot(aes(factor(day_of_publication)), 
       data = news) +
  geom_bar() + 
  xlab('Day of the week')

ggplot(aes(factor(day_of_publication), 
           shares), 
       data = news) +
  geom_jitter(alpha = .05)  + 
  geom_boxplot( alpha = .5,color = 'blue')+ 
  stat_summary(fun.y = "mean", 
               geom = "point", 
               color = "black", 
               shape = 21, 
               size = 4)  +
  scale_y_log10() + 
  xlab('Day of the week') + 
  ylab('Number of shares') + 
  geom_hline(yintercept = median(news$shares))

bivariate_plots_columns <- c("num_imgs",
                             "num_videos",
                             "n_tokens_content")

corr <- cor(select(news %>%
                     filter(n_tokens_title >0),
                   one_of(bivariate_plots_columns)))

ggcorrplot(corr, 
           lab = TRUE,
           outline.col = "white",
           ggtheme = ggplot2::theme_gray,
           colors = c("#6D9EC1", "white", "#E46726"))

my_scatterplot <- function(df, x, y, fill_variable){
  
  'plots scatterplot
  df - data frame
  y - y axis variable as a string
  x - x axis variable  as a string.
  fill - variable to compare, as a string'
  
  plot <- ggplot(aes(x = get(x),
                     y = get(y),
                     fill = get(fill_variable)),
                 data = df) 
  plot
}

grid.arrange(my_scatterplot(df = news_non_zero_words %>%
                              filter(n_tokens_title > 0,
                                     shares <= quantile(shares, 0.99)),
                            x = 'global_subjectivity',
                            y = 'title_subjectivity',
                            fill_variable = 'shares') +
               geom_point(alpha = 0.05, shape = 21) + 
               scale_fill_continuous(low = 'plum1', high = 'purple4') +
               xlab('Article Subjectivity') +
               ylab('Title Subjectivity') + 
               labs(fill = 'Shares') +
               theme_dark(), 
             my_scatterplot(df = news_non_zero_words %>%
                              filter(n_tokens_title > 0,
                                     shares <= quantile(shares, 0.99)),
                            x = 'global_sentiment_polarity',
                            y = 'title_sentiment_polarity',
                            fill_variable = 'shares')+
               geom_point(alpha = 0.05, shape = 21) + 
               scale_fill_continuous(low = 'white', high = 'steelblue') +
               xlab('Article sentiment polarity') +
               ylab('Title sentiment polarity') + 
               labs(fill = 'Shares') + 
               theme_dark(), 
             ncol=2)

grid.arrange(my_scatterplot(df = news_non_zero_words %>%
                              filter(n_tokens_title > 0,
                                     shares > 10000),
                            x = 'global_subjectivity',
                            y = 'title_subjectivity',
                            fill_variable = 'shares')+
               geom_point(alpha = 0.1, shape = 21) + 
               scale_fill_continuous(low = 'plum1', high = 'purple4') +
               xlab('Article Subjectivity') +
               ylab('Title Subjectivity') + 
               labs(fill = 'Shares') +
               ggtitle('Articles with > 10000 shares') +
               theme_dark(), 
             my_scatterplot(df = news_non_zero_words %>%
                              filter(n_tokens_title > 0,
                                     shares > 10000),
                            x = 'global_sentiment_polarity',
                            y = 'title_sentiment_polarity',
                            fill_variable = 'shares') +
               geom_point(alpha = 0.1, shape = 21) + 
               scale_fill_continuous(low = 'white', high = 'steelblue') +
               xlab('Article sentiment polarity') +
               ylab('Title sentiment polarity') + 
               labs(fill = 'Shares') + 
               ggtitle('Articles with > 10000 shares') + 
               theme_dark(), 
             ncol=2)

my_scatterplot(df = news_non_zero_words %>%
                 filter(shares <= quantile(shares,0.99)),
               x = 'global_rate_positive_words',
               y = 'global_rate_negative_words',
               fill_variable = 'shares')+
  geom_point(alpha = 0.08, shape = 21) + 
  scale_fill_continuous(low = 'blue', high = 'red') +
  xlab('Positive word rate') +
  ylab('Negative word rate') + 
  labs(fill = 'Shares') + 
  xlim(-0.05, 0.15) + 
  ylim(-0.05, 0.10) + 
  theme_dark()

my_scatterplot(df = news_non_zero_words %>%
                 filter(shares > 10000),
               x = 'global_rate_positive_words',
               y = 'global_rate_negative_words',
               fill_variable = 'shares') +
  geom_point(alpha = 0.1, shape = 21) + 
  scale_fill_continuous(low = 'blue', high = 'red') +
  xlab('Positive word rate') +
  ylab('Negative word rate') + 
  labs(fill = 'Shares') + 
  ggtitle('Articles with > 10000 shares') +
  xlim(-0.05, 0.15) + 
  ylim(-0.05, 0.10) + 
  theme_dark()

my_scatterplot(df = news_non_zero_words %>%
                 filter(shares > 10000),
               x = 'avg_positive_polarity',
               y = 'avg_negative_polarity',
               fill_variable = 'shares')+
  geom_point(alpha = 0.1, shape = 21) + 
  scale_fill_continuous(low = 'blue', high = 'red') +
  xlab('Average positive polarity') +
  ylab('Average negative polarity') + 
  labs(fill = 'Shares') + 
  ggtitle('Articles with > 10000 shares') + 
  theme_dark()

news %>%
  filter(shares <= quantile(shares, 0.99)) %>%
  ggplot(aes(x = num_imgs, y = num_videos)) + 
  geom_tile(aes(fill = shares)) +
  scale_fill_gradientn(colours = 
                         colorRampPalette(c('azure','coral4'))(100)) +
  labs(fill = 'Shares') + 
  xlab('Number of images') + 
  ylab('Number of videos') +
  theme_dark()

news %>%
  filter(shares <= quantile(shares, 0.99), 
         n_tokens_content > 0, 
         n_non_stop_unique_tokens < 1) %>%
  ggplot(aes(x = average_token_length, 
             y = n_non_stop_unique_tokens,
             fill=shares)) + 
  geom_point(alpha = 0.08, shape = 21) +
  scale_fill_gradient(low = 'blue', high = 'red') +
  labs(fill = 'Shares') + 
  xlab('Average word length') + 
  ylab('Rate of non stop words')+
  theme_dark()

dim(news %>%
      filter (n_tokens_content > 0 & shares > 10000 & n_tokens_title > 0))

my_fn <- function(data, mapping, ...){
  p <- ggplot(data = data, mapping = mapping) + 
    geom_point(alpha = 0.05)
  p
}

ggpairs(select(news_non_empty_title %>%
                 filter(shares <= quantile(shares, 0.99)),
               one_of(c("title_subjectivity",
                        'title_sentiment_polarity',
                        'shares'))), 
        columnLabels = c('Title subjectivity',
                         'Title sentiment polarity',
                         'Shares'),
        lower = list(continuous = my_fn))

ggpairs(select(news_non_zero_words,
               one_of(c("avg_negative_polarity",
                        'avg_positive_polarity',
                        'global_rate_negative_words',
                        'global_rate_positive_words'))), 
        columnLabels = c('Avg -ve polarity',
                         'Avg +ve polarity',
                         'Rate of -ve words',
                         'Rate of +ve words'),
        lower = list(continuous = my_fn))