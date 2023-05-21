import React, { useState, useEffect } from 'react';
import VideoStreamer from './video-streamer';
import VideoStat from './video-statist';

const object_of_interest = ['car', 'person'];
const timerange = { start: 0, end: 100 };

const VideoStreamers = ({param, urls}) => {
  const [visibleUrls, setVisibleUrls] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);


  const videosPerPage = 10;
  const [currentPage, setCurrentPage] = useState(0);

  const isOnlyVideos = param.videoalignment === 'video';
  const isStatistic = param.videoalignment === 'statistic';
  const isVideoAndStatistic = param.videoalignment === 'both';

  useEffect(() => {
    const handleScroll = () => {
      const isBottomOfPage =
        window.innerHeight + window.pageYOffset >= document.documentElement.scrollHeight;

      if (isBottomOfPage) {
        setCurrentPage((prevPage) => prevPage + 1);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  useEffect(() => {
    if (urls) {
      const startIndex = currentPage * videosPerPage;
      const endIndex = startIndex + videosPerPage;
      const newVisibleUrls = urls.slice(startIndex, endIndex);
      setVisibleUrls((prevVisibleUrls) => [...prevVisibleUrls, ...newVisibleUrls]);
    }
  }, [urls, currentPage]);



  if (error) {
    return <p>{error.message}</p>;
  }

  if (isLoading) {
    return <p>... Loading ...</p>;
  }

  if (isOnlyVideos || isStatistic) {
    return (
      <div className="row">
        {urls.map((camera) => (
          <VideoStat key={camera.url} camera={camera} timerange={timerange} object_of_interest={object_of_interest} />
        ))}
      </div>
    );
  } else if (isVideoAndStatistic) {
    return (
      <span>
        {visibleUrls.length > 0 &&
          visibleUrls.map((camera) => (
            <VideoStreamer
              key={camera.id}
              camera={camera}
              timerange={timerange}
              object_of_interest={object_of_interest}
            />
          ))}
      </span>
    );
  } else {
    return null;
  }
  
};

export default VideoStreamers;
