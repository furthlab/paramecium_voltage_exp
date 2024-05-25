dat<-read.table('/Users/danielfurth/Documents/GitHub/paramecium_behavior/shapes.csv', sep=',', header=TRUE)

dat<-read.table('./data/15voltSample03_2trials_shapes.csv', sep=',', header=TRUE)


plot(dat$x, dat$y, pch=16, cex=0.1, type='n', ylim=c(450, 0), xlim=c(0, 600))
dot<-data.frame(frame = integer(), id =integer(), dist = numeric())
for(i in min(dat$frame):max(dat$frame)){
  pol<-unique(dat$ID[dat$frame == i])
  for(j in pol){
    polygon(dat$x[dat$ID == j & dat$frame == i], dat$y[dat$ID == j & dat$frame == i])

    dist<-sum( sqrt(diff(dat$x[dat$ID == j & dat$frame == i])^2 + diff( dat$y[dat$ID == j & dat$frame == i])^2 ) )
    dot <- rbind(dot , data.frame(frame = i, id= j, dist= dist) )
  }
}

smooth.shapes <- data.frame(frame = integer(), ID =integer(), x = numeric(), y = numeric())
plot(dat$x, dat$y, pch=16, cex=0.1, type='n', ylim=c(450, 0), xlim=c(0, 600))

for(i in min(dat$frame):max(dat$frame)){
  pol<-unique(dat$ID[dat$frame == i])
  for(j in pol){

x<-dat$x[dat$ID == j & dat$frame == i]
y<-dat$y[dat$ID == j & dat$frame == i]

x <- c(x, x[1])
y <- c(y, y[1])

xx  <- seq(1, length(y), length.out = 100)

modX <-smooth.spline(seq_along(x), x, df=length(x)/3)
modY <-smooth.spline(seq_along(y), y, df=length(y)/3)

xNew <- predict(modX, xx)$y
yNew <- predict(modY, xx)$y
xNew <- c(xNew, xNew[1])
yNew <- c(yNew, yNew[1])

smooth.shapes<-rbind(smooth.shapes , data.frame(frame = i, ID = j, x = xNew, y = yNew) )

  }
}

i<-5
x<-smooth.shapes$x[smooth.shapes$ID == 12 & smooth.shapes$frame == i]
y<-smooth.shapes$y[smooth.shapes$ID == 12 & smooth.shapes$frame == i]

plot(dat$x, dat$y, pch=16, cex=0.1, type='n', ylim=c(450, 0), xlim=c(0, 600))
for(j in unique(smooth.shapes$frame))
  lapply(unique(smooth.shapes$ID), function(i){polygon(smooth.shapes$x[smooth.shapes$ID==i & smooth.shapes$frame == j],
                                                     smooth.shapes$y[smooth.shapes$ID==i& smooth.shapes$frame == j])})

smooth.shapes$normX <- NA
smooth.shapes$normY <- NA

for(j in unique(smooth.shapes$frame)){
  for(i in unique(smooth.shapes$ID[smooth.shapes$frame == i])){
    smooth.shapes$normX[smooth.shapes$frame == i & smooth.shapes$ID == j] <- smooth.shapes$x[smooth.shapes$frame == i & smooth.shapes$ID == j] - mean(smooth.shapes$x[smooth.shapes$frame == i & smooth.shapes$ID == j])
    smooth.shapes$normY[smooth.shapes$frame == i & smooth.shapes$ID == j] <- smooth.shapes$y[smooth.shapes$frame == i & smooth.shapes$ID == j] - mean(smooth.shapes$y[smooth.shapes$frame == i & smooth.shapes$ID == j])
  }
}


plot(dat$x, dat$y, pch=16, cex=0.1, type='n', ylim=c(-50, 50), xlim=c(-50, 50))
for(j in unique(smooth.shapes$frame)[1:100])
  lapply(unique(smooth.shapes$ID), function(i){polygon(smooth.shapes$normX[smooth.shapes$ID==i & smooth.shapes$frame == j],
                                                       smooth.shapes$normY[smooth.shapes$ID==i& smooth.shapes$frame == j],
                                                       border=rgb(0,0,0,0.02))})


X<-cbind(smooth.shapes$normX[smooth.shapes$ID==i & smooth.shapes$frame == j], smooth.shapes$normY[smooth.shapes$ID==i & smooth.shapes$frame == j])

pca<-prcomp(X)

dat2<-read.table('/Users/danielfurth/Documents/GitHub/paramecium_behavior/centroid.csv', sep=',', header=TRUE)

for(i in min(dat2$frame):max(dat2$frame) ) {
  points(dat2$x[dat2$frame==i], dat2$y[dat2$frame==i], pch=16, cex=0.15, col='red')
}

bb<-read.table('/Users/danielfurth/Documents/GitHub/paramecium_behavior/example_test.csv', sep=',', header=TRUE)

cent<-dat2
cent$newID <- NA

for(i in 1:nrow(bb)){

  polX<-c(bb$xmin[i], bb$xmax[i], bb$xmax[i], bb$xmin[i])
  polY<-c(bb$ymin[i], bb$ymin[i], bb$ymax[i], bb$ymax[i])

  polygon(polX, polY, col='green3')

  inside<-sp::point.in.polygon(dat2$x[dat2$frame==bb$frame[i]],
                       dat2$y[dat2$frame==bb$frame[i]],
                       polX,
                       polY)


  points(cent$x[cent$frame==bb$frame[i]][inside>0], cent$y[cent$frame==bb$frame[i]][inside>0], pch=16, col='blue')

  if( sum(inside!=0) > 1 ){
    points(cent$x[cent$frame==bb$frame[i]][inside>0], cent$y[cent$frame==bb$frame[i]][inside>0], pch=16, col='red')
    points(cent$x[cent$frame==bb$frame[i]][inside==2], cent$y[cent$frame==bb$frame[i]][inside==2], pch=16, col='orange')

    inside[which(inside==2)] <- 0

  }else{
    cent$newID[cent$frame==bb$frame[i]][inside==1] <- bb$ID[i]
  }

}

plot(cent$x, cent$y, pch=16, col=NA, ylim=c(480, 0), xlim=c(0,640))

for(i in unique(cent$newID)[-1]){
  lines(cent$x[which(cent$newID==i)], cent$y[which(cent$newID==i)], col=i, lwd=2)
}


points(cent$x[is.na(cent$newID)], cent$y[is.na(cent$newID)], pch=16, col='red')

speed <- numeric()
for(i in unique(cent$newID)[-1]){
  speed <- append(speed, sqrt(diff(cent$x[which(cent$newID==i)])^2 + diff(cent$y[which(cent$newID==i)])^2)/diff(cent$frame[which(cent$newID==i)])  )
}




