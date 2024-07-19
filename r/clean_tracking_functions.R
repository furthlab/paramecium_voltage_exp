ret.poly<-function(dat){
  poly <- list( x = rep(c(dat$xmin, dat$xmax), each=2), y = c(dat$ymin, dat$ymax, dat$ymax, dat$ymin) )
  return(poly)
}
boundbox <- function(dat, ...){
  polygon(ret.poly(dat), ... )
}
cent.in.bb <- function(dat, cent){
  inside<-rep(FALSE, length(unique(dat$ID)))
  for(i in unique(dat$ID)){
    if( sum( sp::point.in.polygon(cent$x, cent$y, ret.poly(dat[dat$ID == i,])$x, ret.poly(dat[dat$ID == i,])$y) ) > 0 ){
      inside[which(unique(dat$ID) == i)] <- TRUE
    }
  }
  #out <- rbind(table(inside), round(100*prop.table(table(inside)),2) )
  #print( out )
  return(inside)
}

clean.bb <- function(dat, cent){
  dat$remove <- TRUE
  for(i in unique(dat$frame)){
    inside <- cent.in.bb( dat[dat$frame == i,], cent[cent$frame == i,] )
    dat$remove[dat$frame == i] <- !inside
  }
  return(dat)
}

plot.bb<-function(dat, cent, froi = 50){

  inside <- cent.in.bb(dat[dat$frame==froi,], cent[cent$frame %in% c(froi),])

  plot(cent$x[cent$frame %in% c(froi)], cent$y[cent$frame %in% c(froi)],type='n', xlim=c(0, 640), ylim=c(480, 0), ylab='', xlab='')

  for(i in unique(dat$ID[dat$frame==froi])){
    if(inside[which(unique(dat$ID[dat$frame==froi]) == i)]){
      boundbox(dat[dat$ID == i & dat$frame ==froi,], col='red')
    }else{
      boundbox(dat[dat$ID == i & dat$frame ==froi,], border='blue')
    }

  }

  points(cent$x[cent$frame %in% c(froi)], cent$y[cent$frame %in% c(froi)], pch=21, bg='orange')

}


get.velocity <- function(dat){
  dat$x <- (dat$xmin + dat$xmax)/2
  dat$y <- (dat$ymin + dat$ymax)/2

  dat$velocity <- NA

  for(i in unique(dat$ID)){
    df<-cbind(dat$x[dat$ID == i], dat$y[dat$ID == i], dat$frame[dat$ID == i])

    if(nrow(df) > 1){
      dt <- apply(df[,1:2], 2, diff)^2
      if(length(dt) > 2){
        vec <- sqrt( apply(dt , 1, sum) )
      }else{
        vec <- sqrt(sum(dt))
      }
      vec <- vec/diff(df[,3])

      dat$velocity[dat$ID == i] <- c(vec[1], vec)
    }
  }
  return(dat)
}


