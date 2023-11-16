get.ts <- function(log, event = 'CS', fps = 30){
  ts.on<-log$frame[which(log$stimulus == event & log$event == 'on')]
  ts.off<-log$frame[which(log$stimulus == event & log$event == 'off')]

  poli <- cbind(ts.on/fps, ts.off/fps)
  return(poli)
}

polygon.for.event <- function(log, event = 'CS', fps = 30, ylim = c(0,8), ...){
  poli<-get.ts(log, event, fps)

  for(i in 1:nrow(poli)){
    polygon(c(poli[i,1], poli[i,2],
              poli[i,2], poli[i,1]),
            rep(ylim, each=2), ...)
  }
}

plot.tracks<-function(dat, plot = TRUE, lwd = 4, ...){
  if(plot)
    plot(0, 0,type='n', xlim=c(0, 640), ylim=c(480, 0), ylab='', xlab='', asp=1)

  for(i in unique(dat$ID)){
    lines( (dat$xmin + dat$xmax)[dat$ID == i]/2,
           (dat$ymin + dat$ymax)[dat$ID == i]/2, col=i, lwd=lwd, ...)
  }
}

plot.shapes<-function(shape, plot = TRUE, ...){
  if(plot)
    plot(0, 0,type='n', xlim=c(0, 640), ylim=c(480, 0), ylab='', xlab='', asp=1)

  for(j in unique(shape$frame)){
  for(i in unique(shape$ID[shape$frame==j])){
    polygon(shape$x[shape$ID==i], shape$y[shape$ID==i], ...)
  }
  }
}


data.window <- function(vec, log, window = c(-5000, 5000), fps = 30, event = 'US', type = 'off'){
  poli<-get.ts(log, event, fps)
  if(type=='off'){
    ts <- as.integer(poli[,2]*fps)
  }else{
    ts <- as.integer(poli[,1]*fps)
  }

  window<-round(window/fps)

  window <- cbind(ts + window[1], ts + window[2])

  val <- list()
  val[[1]] <- vec[window[1,1]:window[1,2] ]

  for(i in 2:nrow(window))
    val[[i]] <- vec[window[i,1]:window[i,2] ]

  return(val)
}

plot.velocity<-function(vel, log){
vec <- tapply(vel$velocity, vel$frame, mean, na.rm=TRUE)

par(yaxs='i', xaxs='i')
xlim <- round(range(unique(vel$frame)/30) )
plot(unique(vel$frame)/30, vec,  ylim = c(0,8), type='n', las=1, ylab='Average velocity', xlab='Time (sec.)')

polygon.for.event(log, col='lightblue')
polygon.for.event(log, event='US', col='pink')


lines(unique(vel$frame)/30, vec)
lines(unique(vel$frame)/30, smooth.spline(vec)$y, col='red2', lwd=2)

par(xpd=TRUE)
arrows(xlim[1], 9.2, xlim[2], 9.2, length = 0.08)
polygon.for.event(log, event='US', col='pink', ylim=c(9.2, 9.6))
text(diff(xlim), 9, 'US', pos=4)

arrows(xlim[1], 10.2, xlim[2], 10.2, length = 0.08)
text(diff(xlim), 10, 'CS', pos=4)
polygon.for.event(log, col='lightblue', ylim=c(10.2, 10.6))
par(xpd=FALSE)

}
