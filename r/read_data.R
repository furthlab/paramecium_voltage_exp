read.log <- function(file){

  log <- read.table(file, skip=1, header=TRUE, fill =TRUE, row.names=NULL)
  names(log) <- c('frame', 'time', 'stimulus', 'event', 'trial')
  log$frame <- as.integer(log$frame)
  log$time <- as.integer(log$time)
  log$trial <- as.integer(log$trial)
  return(log)

}

read.centroid <- function(file){
  cent <- read.table(file, sep=',', header=TRUE)

  q<-min(which(diff(cent$frame)[1:100]==1))

  cent2 <- cent[ (q+1):nrow(cent),c(4,1,2,3)]
  names(cent2) <- names(cent)
  cent<-rbind(cent[1:q,],  cent2)

  return(cent)

}

read.shapes <- function(file){
  shape <- read.table(file, sep=',', header=TRUE)

  q<-min(which(diff(shape$frame)==1))

  shape2 <- shape[ (q+1):nrow(shape),c(4,1,2,3)]
  names(shape2) <- names(shape)
  shape<-rbind(shape[1:q,],  shape2)

  return(shape)

}

write.output<-function(basename_string = "15000mVSample00", data.folder = 'data'){
  files <- dir(data.folder, full.names = TRUE)
  file <- files[basename(files) == paste0(basename_string,'.log')]
  log <- read.log(file)
  #load centroids and bounding boxes
  file <- files[ basename(files) == paste0(basename_string,'_centroid.csv') ]
  cent <- read.centroid(file)
  file <- files[basename(files) == paste0(basename_string,'.csv') ]
  dat <- read.table(file, sep=',', header=TRUE)

  dat <- clean.bb(dat, cent)
  dat <- dat[!dat$remove,]

  vel <- get.velocity(dat)

  write.table(log, file=paste0('processed/', basename_string,'_timestamps.csv'), sep=',', row.names = FALSE)
  write.table(vel, file=paste0('processed/', basename_string,'_behavior.csv'), sep=',', row.names = FALSE)

}
