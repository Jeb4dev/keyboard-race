import React, { useEffect } from 'react';
import { Heading } from '@chakra-ui/react';
import { useSocket } from '../sockets/useSocket';

interface StopDialogProps {
  time: number;
  count: number;
  errors: number;
}

export const formatTime = (time: number) => {
  const timeInSeconds = Math.floor(time / 1000);
  const minutes = Math.floor(timeInSeconds / 60);
  const seconds = timeInSeconds - minutes * 60;
  return [minutes, seconds].map((v) => (v < 10 ? `0${v}` : v)).join(':');
};

function StopDialog({ time, count, errors }: StopDialogProps) {
  const { socket } = useSocket();
  const speed = (count / Math.floor(time / 1000)) * 60;
  const errorsSpeed = (errors / Math.floor(time / 1000)) * 60;
  useEffect(() => {
    socket?.emit('sv_get_race_statistics', {
      wpm: Math.ceil(speed),
      epm: errorsSpeed,
      accuracy: errors / count,
      time,
      ranking: 1,
    });
  }, []);
  return (
    <>
      <Heading textAlign="center" fontSize="3xl">
        You've finished race in {formatTime(time)} with speed
      </Heading>
      <Heading textAlign="center" fontSize="6xl">
        {Math.ceil(speed)} words per minute
      </Heading>
    </>
  );
}

export default StopDialog;
